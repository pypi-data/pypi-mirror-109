#  -*- coding: utf-8 -*-
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

import logging
import struct

import pytest

from zapf import CommError
from zapf.device import TYPECODE_MAP, typecode_description
from zapf.io import PlcIO
from zapf.proto.sim import SimProtocol
from zapf.scan import Scanner

from test import testplc


def prettify(data):
    if len(data) == 2:
        val = struct.unpack('H', data)[0]
        return f'{val} {val:#x}'
    elif len(data) == 4:
        val_i = struct.unpack('I', data)[0]
        val_f = struct.unpack('f', data)[0]
        return f'{val_i} {val_i:#x} {val_f}'
    elif len(data) == 8:
        val_i = struct.unpack('Q', data)[0]
        val_f = struct.unpack('d', data)[0]
        return f'{val_i} {val_i:#x} {val_f}'
    return ''


class TestProtocol(SimProtocol):
    OFFSETS = [0, 0x10000]  # allow trying a failing offset

    def read(self, addr, length):
        try:
            data = super().read(addr, length)
        except Exception as err:
            self.log.warning(f'R {addr:#x} {length} !! {err}')
            raise CommError(f'read failed: {err}') from err
        else:
            self.log.debug(f'R {addr:#x} {length} -> {data} {prettify(data)}')
            return data

    def write(self, addr, data):
        try:
            super().write(addr, data)
        except Exception as err:
            self.log.warning(f'W {addr:#x} {data} {prettify(data)} !! {err}')
            raise CommError(f'write failed: {err}') from err
        else:
            self.log.debug(f'W {addr:#x} {data} {prettify(data)} ok')


@pytest.fixture(scope='module')
def plc_io():
    proto = TestProtocol(testplc.Main, logging.getLogger('simplc'))
    proto.connect()

    yield PlcIO(proto, logging.root)

    proto.disconnect()


# preselect implemented typecodes from BIG TABLE
tcm = [(t, dinfo) for (t, dinfo) in TYPECODE_MAP.items()
       if dinfo.num_values in [0, 1, 2, 8, 16]
       if dinfo.num_params in [0, 1, 8, 16]]

# slice defined typcodes into smaller sets for the specific tests
# These slices are tied to the corresponding tests in test_device
# we split into:
# * readable devices (single value) (contains devices with target too),
# * devices with a target (single value)
# * devices with flat parameters
# * devices with param interface
# * vector devices
TC_READABLE_DEVICES = [t for (t, dinfo) in tcm if dinfo.num_values == 1]
TC_TARGET_DEVICES = [t for (t, dinfo) in tcm if dinfo.num_values == 1
                     if (dinfo.has_target or (t >> 8) in [0x14, 0x15])]
TC_FLAT_DEVICES = [t for (t, dinfo) in tcm if dinfo.num_values == 1
                   if dinfo.num_params >= 1 if not dinfo.has_pctrl]
TC_PARAM_DEVICES = [t for (t, dinfo) in tcm if dinfo.num_params >= 1
                    if dinfo.has_pctrl]
TC_VECTOR_DEVICES = [t for (t, dinfo) in tcm if dinfo.num_values >= 2]


# Scan testplc only once for implemented devices
CACHED_DEVLIST = []


# pylint: disable=redefined-outer-name, inconsistent-return-statements
def filter_tc(plc_io, tc):
    """find a zapf-device with the requested typecode"""
    if not CACHED_DEVLIST:
        CACHED_DEVLIST[:] = Scanner(plc_io, plc_io.log).get_devices()
    # find the dev with typecode
    for d in CACHED_DEVLIST:
        if d.typecode == tc:
            return d, TYPECODE_MAP[tc]
    pytest.fail(f'typecode 0x{tc:04x} not implemented in testplc')


@pytest.fixture(scope='module', params=TC_READABLE_DEVICES,
                ids=typecode_description)
# pylint: disable=redefined-outer-name
def plc_readable_device(plc_io, request):
    return filter_tc(plc_io, request.param)


@pytest.fixture(scope='module', params=TC_TARGET_DEVICES,
                ids=typecode_description)
# pylint: disable=redefined-outer-name
def plc_target_device(plc_io, request):
    return filter_tc(plc_io, request.param)


@pytest.fixture(scope='module', params=TC_FLAT_DEVICES,
                ids=typecode_description)
# pylint: disable=redefined-outer-name
def plc_flat_device(plc_io, request):
    return filter_tc(plc_io, request.param)


@pytest.fixture(scope='module', params=TC_PARAM_DEVICES,
                ids=typecode_description)
# pylint: disable=redefined-outer-name
def plc_param_device(plc_io, request):
    return filter_tc(plc_io, request.param)


@pytest.fixture(scope='module', params=TC_VECTOR_DEVICES,
                ids=typecode_description)
# pylint: disable=redefined-outer-name
def plc_vector_device(plc_io, request):
    return filter_tc(plc_io, request.param)


@pytest.fixture(scope='function', autouse=True)
def log_fixture(caplog):
    caplog.set_level(logging.INFO)
