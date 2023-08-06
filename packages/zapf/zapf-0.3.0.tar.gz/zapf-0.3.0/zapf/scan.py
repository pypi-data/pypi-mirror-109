# *****************************************************************************
# PILS PLC client library
# Copyright (c) 2019-2021 by the authors, see LICENSE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Module authors:
#   Georg Brandl <g.brandl@fz-juelich.de>
#
# *****************************************************************************

"""Support for scanning the indexer and creating devices."""

from collections import namedtuple

from zapf import spec
from zapf.device import Device
from zapf.io import PlcIO

DeviceInfo = namedtuple('DeviceInfo', 'number name addr typecode info')


class Scanner:
    """
    :param io_or_proto: A connection URI string, a `.PlcIO` instance or
        a `.Protocol` instance.
    :param log: The `logging.Logger` instance to use for this object and
        all derived objects (e.g. devices).

    **Connection URIs** can have the following forms:

    ``ads://host[:port]/amsnetid:amsport``
        Connection to a Beckhoff PLC using the ADS protocol.  The TCP port is
        48898 by default.  The AMS NetID and AMS port are specific to the PLC.
        Note that an AMS router entry must be set on the PLC in order to
        connect.

        Example: ``ads://192.168.201.2/5.18.77.4.1.1:851``

    ``modbus://host[:port]/slaveno``
        Connection to a host that supports the Modbus/TCP protocol.  The TCP
        port is 502 by default.

        Example: ``modbus://192.168.201.2/0``

    ``tango://dbhost:dbport/tango/device/name``
        Connection to a `Tango <https://tango-controls.org>`_ device which in
        turn connects to the PLC.

        The Tango device interface must conform to the `Profibus
        <https://forge.frm2.tum.de/entangle/defs/entangle-master/profibus/>`_
        Entangle interface specification.

        Example: ``tango://192.168.201.2:10000/box/plc/ads``
    """
    def __init__(self, io_or_proto, log):
        self.log = log
        if isinstance(io_or_proto, PlcIO):
            self.io = io_or_proto
        else:
            self.io = PlcIO(io_or_proto, log)

    def get_plc_data(self):
        """Establish communication with the indexer and return an object
        containing the metadata.

        The following attributes are defined on this object:

        ``magicstr``
            The PLC :ref:`magic number <pils:magic>`, converted to a string,
            that identifies the PILS protocol revision.  Example: `'2015_02'`.
        ``indexer_addr``
            The byte address of the indexer data structure, relative to the
            common data area.
        ``indexer_size``
            The size of the indexer in bytes.
        ``num_devices``
            The number of devices present.  This information is provided
            optionally by PILS, and can be 0.  In this case, the number of
            devices is found by finding the first device number where the
            indexer returns empty information.
        ``plc_name``
            The "PLC name" string as reported by the PLC.
        ``plc_version``
            The "PLC version" string as reported by the PLC.
        ``plc_author``
            The "PLC author" string as reported by the PLC.

        Can raise `.SpecError` if the PLC does not conform to a supported PILS
        version, or returns invalid information.
        """
        self.io.indexer.detect_plc()
        return self.io.indexer

    def scan_devices(self):
        """Scan the PLC and yield information about devices.

        For each device found in the PLC, this will yield a namedtuple with the
        following items:

        * ``number``: device number (1 to N)
        * ``name``: device name
        * ``addr``: device byte address
        * ``typecode``: device :ref:`type code <pils:type-codes>`
        * ``info``: additional information: a dictionary, see below

        Additional information contains at least the following keys:

        * ``lowlevel``: bool, if the device is marked "low level"
        * ``unit``: string, the unit of the main device value
        * ``absmin`` and ``absmax``: float, the limits of the main value
        * ``params``: a list of parameter names if the device has params
        * ``funcs``: a list of special function names if the device has such
        * ``aux_strings``: a list of 24 strings containing the interpretation
          of the up to 24 freely definable bits in the device status.
          Strings that are not defined are empty.

        Upon further extension of PILS, additional keys can appear.
        """

        # ensure we can talk to the indexer
        self.io.indexer.detect_plc()

        # check which method we need to scan
        method = getattr(self, '_scan_' + self.io.indexer.magicstr, None)
        if not method:
            raise RuntimeError('Magic %s is supported, but no scanner method '
                               'available' % self.io.indexer.magicstr)

        yield from method()

    def get_device(self, devinfo):
        """Return a device object for the given devinfo, as yielded by
        `scan_devices`.

        This will return a `.Device` object of the correct subclass for the
        device's typecode, or ``None`` if the typecode is not supported.
        """
        devcls = Device.class_for(devinfo.typecode)
        if devcls is None:
            self.log.warning('type code %#x is not supported, skipping',
                             devinfo.typecode)
            return None
        else:
            return devcls(devinfo.number, devinfo.name, devinfo.addr,
                          devinfo.typecode, devinfo.info, self.io, self.log)

    def get_devices(self):
        """Scan the PLC and yield device objects.

        Short form of calling `get_device` for each device returned by
        `scan_devices`.
        """
        for data in self.scan_devices():
            yield self.get_device(data)

    def _scan_2015_02(self):
        indexer = self.io.indexer
        next_addr = indexer.indexer_addr + indexer.indexer_size

        for devnum in range(1, 256):
            info = indexer.query_infostruct(devnum)
            typecode, size, addr, unit, flags, absmin, absmax, name = info

            # gone past last device?
            if typecode == 0:
                break

            # if there is not valid data in the infostruct, query individually
            if size + addr + flags == 0 and not name:
                size = indexer.query_word(devnum, spec.INFO_SIZE)
                if not size:
                    size = 2 * (typecode & 0xff)
                addr = indexer.query_word(devnum, spec.INFO_ADDR)
                if not addr:
                    addr = next_addr
                unit = indexer.query_unit(devnum, spec.INFO_UNIT)
                flags = None
                lowlevel = False
                absmin = -spec.FLOAT32_MAX
                absmax = spec.FLOAT32_MAX
            else:
                lowlevel = (flags & 0x80000000) != 0

            # this might be empty even if a valid infostruct was present,
            # e.g. if the full name didn't fit behind the 20 previous bytes
            if not name:
                name = indexer.query_string(devnum, spec.INFO_NAME)

            # extract info about parameters and special functions
            devclass = typecode >> 13
            parameters = []
            functions = []
            if devclass in (1, 2):
                if devclass == 1:  # FlatDevices: a list of indices
                    plist = indexer.query_bytes(devnum, spec.INFO_PARAMS)
                    param_ids = [p for p in plist if p]
                else:  # ParamDevices: a bitmap of indices
                    param_ids = indexer.query_bitmap(devnum, spec.INFO_PARAMS)
                param_ids.sort()  # ... which *should* be unnecessary
                for p in param_ids:
                    if spec.is_function(p):
                        functions.append(spec.Parameters[p])
                    else:
                        parameters.append(spec.Parameters[p])

            # extract AUX string labels
            aux_strings = [''] * 24
            if flags is None:  # old way, stop reading the first empty one
                for idx in range(24):
                    aux_string = indexer.query_string(devnum,
                                                      spec.INFO_AUX1 + idx)
                    aux_strings[idx] = aux_string.strip()
                    if not aux_string:
                        break
            else:  # new way, only read the relevant (flagged ones)
                for idx in range(24):
                    if flags & (1 << idx):
                        aux_string = indexer.query_string(devnum,
                                                          spec.INFO_AUX1 + idx)
                        aux_strings[idx] = aux_string.strip()

            info = dict(lowlevel=lowlevel, unit=unit,
                        absmin=absmin, absmax=absmax,
                        params=parameters, funcs=functions,
                        aux_strings=aux_strings)
            self.log.info('found device %s at addr %s with type %#x',
                          name, addr, typecode)
            yield DeviceInfo(devnum, name, addr, typecode, info)

            next_addr = addr + size
