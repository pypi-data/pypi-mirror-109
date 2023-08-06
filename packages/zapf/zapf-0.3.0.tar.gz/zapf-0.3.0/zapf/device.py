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

"""Basic device abstraction for PILS devices."""

import time
from collections import namedtuple
from struct import calcsize

from zapf import ApiError, SpecError
from zapf.spec import FIRST_FLOAT_PARAM, FLOAT32_MAX, FLOAT64_MAX, ParamCMDs, \
    ParamControl, Parameters, PLCStatus, StatusStruct16, StatusStruct32
from zapf.util import UncasedMap

START16 = PLCStatus.START << 12
START32 = PLCStatus.START << 28


class Device:
    """Base class for all specific PILS devices.

    :param number: The device number within the PLC (1-N).
    :param name: The device name.  This is not currently used by Zapf.
    :param addr: The base device address.
    :param typecode: The device's typecode.
    :param info: The "additional info" dictionary returned by the `.Scanner`.
    :param io: A `.PlcIO` instance to use for communication with the PLC.
    :param log: A `logging.Logger` to use for device related logging.
    """

    @classmethod
    def class_for(cls, typecode):
        return TYPECODE_MAP.get(typecode, (None,))[0]

    valuetype = None

    def __init__(self, number, name, addr, typecode, info, io, log):
        self.number = number
        self.name = name
        self.typecode = typecode
        self.device_kind = typecode >> 8
        self.total_size = 2 * (typecode & 0xff)
        self.info = info
        self.params = info['params']
        self.funcs = info['funcs']

        typeinfo = TYPECODE_MAP[typecode]
        self.value_fmt = typeinfo.value_fmt
        self.value_size = calcsize(self.value_fmt)
        self.status_size = typeinfo.status_size
        self.num_values = typeinfo.num_values
        self.num_params = typeinfo.num_params

        self.addr = addr
        next_addr = addr + self.num_values*self.value_size
        if typeinfo.has_target:
            self.target_addr = next_addr
            next_addr += self.num_values*self.value_size
        else:
            self.target_addr = None
        if self.status_size:
            self.status_addr = next_addr
        else:
            self.status_addr = None
        if typeinfo.has_pctrl:
            self.pctrl_addr = self.status_addr + self.status_size
        else:
            self.pctrl_addr = None
        if typeinfo.num_params:
            self.param_addr = self.status_addr + self.status_size + 2
        else:
            self.param_addr = None

        self.log = log
        self.io = io
        self._init()
        self.io.register_cache_range(self.addr, self.total_size)

    def read_status(self):
        """Read the status information of the device.

        This is a tuple of ``(state, reason, aux, error_id)``.

        ``state`` is the 4-bit state (see `.PLCStatus` for possible values).
        ``reason`` is the 4-bit reason code (see `.ReasonMap`).  ``aux``
        contains the up to 24 AUX bits.  ``error_id`` is a device-defined
        16-bit integer.

        For devices that do not have an error ID field, it is returned as zero.
        """
        if self.status_addr is None:
            if self.target_addr and self.read_value() != self.read_target():
                return (PLCStatus.BUSY, 0, 0, 0)
            return (PLCStatus.IDLE, 0, 0, 0)
        if self.status_size == 2:
            s = StatusStruct16(self.io.read_u16(self.status_addr))
            return (s.STATE, s.REASON, s.AUX, 0)
        elif self.status_size == 4:
            s = StatusStruct32(self.io.read_u32(self.status_addr))
            return (s.STATE, s.REASON, s.AUX, 0)
        elif self.status_size == 6:
            value, err_id = self.io.read_fmt(self.status_addr, 'IH')
            s = StatusStruct32(value)
            return (s.STATE, s.REASON, s.AUX, err_id)
        raise SpecError('invalid status_size')

    def change_status(self, initial_states=(), final_state=0):
        """Change the state of the device.

        Since :ref:`not all state transitions are allowed <pils:state-graph>`,
        you can list the allowed states in *initial_states*.  If that list is
        given and the current state is not contained, ``False`` is returned.
        Else the *final_state* is written and ``True`` is returned.

        If the device does not have a status, ``False`` is always returned.
        """
        if self.status_addr is None:
            return False
        if initial_states:
            state = self.read_status()[0]
            if state not in initial_states:
                return False
        else:
            status = StatusStruct16()
        status.STATE = final_state
        if self.status_size == 2:
            self.io.write_u16(self.status_addr, int(status))
        else:
            self.io.write_u32(self.status_addr, int(status) << 16)
        return True

    # to implement:

    def _init(self):
        raise NotImplementedError

    def get_limits(self):
        """Return the limits of the device's data type.

        This is not the same as the limits from the device's meta info
        (absmin/absmax), but only depends on the value type (int16/float32/...)
        """
        raise NotImplementedError

    def read_value(self):
        """Read the main value of the device.

        The type of the returned value differs depending on the device type:

        * int for discrete devices
        * float for analog devices
        * list of float for vector devices
        """
        raise NotImplementedError

    def read_target(self):
        """Read the target of the device.

        The returned value is of the same type as `read_value`.

        If the device is read-only and has no target, `.ApiError` is raised.
        """
        raise ApiError('reading target of a read-only device')

    def change_target(self, value):
        """Change the target of the device.

        This will atomically write the new target (whose type must be the same
        as returned by `read_value`) and set the state to `START`.

        If the device is read-only and has no target, `.ApiError` is raised.
        """
        raise ApiError('writing target of a read-only device')

    def list_params(self):
        """Return a list of the names of the device's :ref:`parameters
        <pils:parameters-functions>`.

        If the device supports no parameters, an empty list is returned.
        """
        return []

    def get_param(self, name):
        """Read the given parameter.

        The type of the parameter depends on the parameter index, it can be
        int or float.

        The return value is a tuple of ``(param_cmd, value)`` where
        ``param_cmd`` represents the reply of the parameter state machine,
        see `.ParamCMDs`.

        If the device supports no parameters, `.ApiError` is raised.
        """
        raise ApiError('reading parameter of a device without params')

    def set_param(self, name, value):
        """Set the given parameter.

        The type of the parameter depends on the parameter index, it can be
        int or float.

        The return value is a tuple of ``(param_cmd, value)`` where
        ``param_cmd`` represents the reply of the parameter state machine,
        see `.ParamCMDs`, and ``value`` is the read-back value of the
        parameter (which might differ from the written value due to clamping,
        rounding or other correction the PLC makes).

        If the device supports no parameters, `.ApiError` is raised.
        """
        raise ApiError('writing parameter of a device without params')

    def list_funcs(self):
        """Return a list of the names of the device's `special functions
        <pils:parameters-functions>`.

        If the device supports no special functions, an empty list is returned.
        """
        return []

    def exec_func(self, name, value=None):
        """Execute the given special function with an argument.

        The return value is a tuple of ``(param_cmd, value)`` where
        ``param_cmd`` represents the reply of the parameter state machine,
        see `.ParamCMDs`, and ``value`` is the return value of the function.

        If the device supports no special functions, `.ApiError` is raised.
        """
        raise ApiError('executing function of a device without functions')


class DiscreteDevice(Device):
    """Base class used for discrete devices."""

    def _init(self):
        pass

    def get_limits(self):
        if self.value_size == 2:
            return (-2**15, 2**15 - 1)
        elif self.value_size == 4:
            return (-2**31, 2**31 - 1)
        elif self.value_size == 8:
            return (-2**63, 2**63 - 1)
        raise SpecError('invalid value_size')

    def read_value(self):
        return self.io.read_fmt(self.addr, self.value_fmt)[0]

    def read_target(self):
        if self.target_addr is None:
            raise ApiError('reading target of a read-only device')
        return self.io.read_fmt(self.target_addr, self.value_fmt)[0]

    def change_target(self, value):
        if self.target_addr is None:
            raise ApiError('writing target of a read-only device')
        if self.status_addr is None:
            self.io.write_fmt(self.target_addr, self.value_fmt, value)
        elif self.value_size == 2:
            self.io.write_fmt(self.target_addr, self.value_fmt + 'H',
                              value, START16)
        else:
            self.io.write_fmt(self.target_addr, self.value_fmt + 'I',
                              value, START32)


class SimpleDiscreteIn(DiscreteDevice):
    """Class for :ref:`pils:dev-simplediscreteinput`,
    :ref:`pils:dev-simplediscrete32input`,
    :ref:`pils:dev-simplediscrete64input`."""


class SimpleDiscreteOut(DiscreteDevice):
    """Class for :ref:`pils:dev-simplediscreteoutput`,
    :ref:`pils:dev-simplediscrete32output`,
    :ref:`pils:dev-simplediscrete64output`."""


class DiscreteIn(DiscreteDevice):
    """Class for :ref:`pils:dev-discreteinput`,
    :ref:`pils:dev-discrete32input`, :ref:`pils:dev-discrete64input`."""


class DiscreteOut(DiscreteDevice):
    """Class for :ref:`pils:dev-discreteoutput`,
    :ref:`pils:dev-discrete32output`, :ref:`pils:dev-discrete64output`."""


class Keyword(DiscreteDevice):
    """Class for :ref:`pils:dev-keyword`, :ref:`pils:dev-keyword32`,
    :ref:`pils:dev-keyword64`."""

    def _init(self):
        self.target_addr = self.addr

    def get_limits(self):
        if self.value_size == 2:
            return (0, 2**16 - 1)
        elif self.value_size == 4:
            return (0, 2**32 - 1)
        elif self.value_size == 8:
            return (0, 2**64 - 1)
        raise SpecError('invalid value_size')


class StatusWord(Keyword):
    """Class for :ref:`pils:dev-statusword`, :ref:`pils:dev-extstatusword`."""

    def _init(self):
        Keyword._init(self)
        self.status_addr = self.addr


class AnalogDevice(Device):
    """Base class for analog valued devices (except vector devices)."""

    def _init(self):
        pass

    def get_limits(self):
        if self.value_size == 4:
            return (-FLOAT32_MAX, FLOAT32_MAX)
        elif self.value_size == 8:
            return (-FLOAT64_MAX, FLOAT64_MAX)
        raise SpecError('invalid value_size')

    def read_value(self):
        if self.value_size == 4:
            return self.io.read_f32(self.addr)
        elif self.value_size == 8:
            return self.io.read_f64(self.addr)
        raise SpecError('invalid value_size')

    def read_target(self):
        if self.target_addr is None:
            raise ApiError('reading target of a read-only device')
        if self.value_size == 4:
            return self.io.read_f32(self.target_addr)
        elif self.value_size == 8:
            return self.io.read_f64(self.target_addr)
        raise SpecError('invalid value_size')

    def change_target(self, value):
        if self.target_addr is None:
            raise ApiError('writing target of a read-only device')
        if self.status_addr is None:
            if self.value_size == 4:
                self.io.write_f32(self.target_addr, value)
            elif self.value_size == 8:
                self.io.write_f64(self.target_addr, value)
        elif self.value_size == 4:
            if self.status_size == 2:
                self.io.write_f32_u16(self.target_addr, value, START16)
            else:
                self.io.write_f32_u32(self.target_addr, value, START32)
        elif self.value_size == 8:
            self.io.write_fmt(self.target_addr, 'dI', value, START32)


class SimpleAnalogIn(AnalogDevice):
    """Class for :ref:`pils:dev-simpleanaloginput`,
    :ref:`pils:dev-simpleanalog64input`."""


class SimpleAnalogOut(AnalogDevice):
    """Class for :ref:`pils:dev-simpleanalogoutput`,
    :ref:`pils:dev-simpleanalog64output`."""


class AnalogIn(AnalogDevice):
    """Class for :ref:`pils:dev-analoginput`, :ref:`pils:dev-analog64input`."""


class AnalogOut(AnalogDevice):
    """Class for :ref:`pils:dev-analogoutput`,
    :ref:`pils:dev-analog64output`."""


class RealValue(AnalogDevice):
    """Class for :ref:`pils:dev-realvalue`, :ref:`pils:dev-realvalue64`."""

    def _init(self):
        self.target_addr = self.addr


class FlatParams:
    def _init(self):
        if self.num_params != len(self.params):
            raise SpecError('mismatch between parameter count between '
                            'typecode and parameter indices from indexer '
                            f'({self.num_params}/{len(self.params)})')
        # sort params from indexer by index
        pars_indices = sorted((Parameters[par], par) for par in self.params)
        self.param_map = UncasedMap(*(
            (par[1], (self.param_addr + i * self.value_size, par[0]))
            for (i, par) in enumerate(pars_indices)
        ))

    def list_params(self):
        return self.param_map.init_keys()

    def get_param(self, name):
        (addr, idx) = self.param_map.get(name, (None, None))
        if addr:
            if idx < FIRST_FLOAT_PARAM:
                if self.value_size == 4:
                    return ParamCMDs.DONE, self.io.read_u32(addr)
                else:
                    return ParamCMDs.DONE, self.io.read_u64(addr)
            else:
                if self.value_size == 4:
                    return ParamCMDs.DONE, self.io.read_f32(addr)
                else:
                    return ParamCMDs.DONE, self.io.read_f64(addr)
        return ParamCMDs.ERR_NO_IDX, None

    def set_param(self, name, value):
        (addr, idx) = self.param_map.get(name, (None, None))
        if addr:
            if idx < FIRST_FLOAT_PARAM:
                if self.value_size == 4:
                    self.io.write_u32(addr, int(value))
                    return ParamCMDs.DONE, self.io.read_u32(addr)
                else:
                    self.io.write_u64(addr, int(value))
                    return ParamCMDs.DONE, self.io.read_u64(addr)
            else:
                if self.value_size == 4:
                    self.io.write_f32(addr, value)
                    return ParamCMDs.DONE, self.io.read_f32(addr)
                else:
                    self.io.write_f64(addr, value)
                    return ParamCMDs.DONE, self.io.read_f64(addr)
        return ParamCMDs.ERR_NO_IDX, None


class FlatIn(FlatParams, AnalogDevice):
    """Class for :ref:`pils:dev-flatinput`, :ref:`pils:dev-flat64input`."""


class FlatOut(FlatParams, AnalogDevice):
    """Class for :ref:`pils:dev-flatoutput`, :ref:`pils:dev-flat64output`."""


class ParamInterface:
    param_timeout = 1

    def _init(self):
        self.param_map = UncasedMap(*((p, Parameters[p]) for p in self.params))
        self.func_map = UncasedMap(*((p, Parameters[p]) for p in self.funcs))
        self.param_sm = ParamControl()

    def update_param_sm(self):
        self.param_sm(self.io.read_u16(self.pctrl_addr))

    def wait_sm_available(self):
        self.update_param_sm()
        timesout = time.time() + self.param_timeout
        while not self.param_sm.available:
            self.update_param_sm()
            if time.time() > timesout:
                return False
        return True

    def set_param_value(self, idx, value):
        if idx < FIRST_FLOAT_PARAM:
            if self.value_size == 4:
                self.io.write_u32(self.param_addr, int(value))
            else:
                self.io.write_u64(self.param_addr, int(value))
        else:
            if self.value_size == 4:
                self.io.write_f32(self.param_addr, value)
            else:
                self.io.write_f64(self.param_addr, value)

    def set_param_value_and_cmd(self, cmd, sub, idx, value):
        self.param_sm.CMD = cmd
        self.param_sm.SUB = sub
        self.param_sm.IDX = idx
        if idx < FIRST_FLOAT_PARAM:
            if self.value_size == 4:
                self.io.write_fmt(self.pctrl_addr, 'HI',
                                  int(self.param_sm), int(value))
            else:
                self.io.write_fmt(self.pctrl_addr, 'HQ',
                                  int(self.param_sm), int(value))
        else:
            if self.value_size == 4:
                self.io.write_u16_f32(self.pctrl_addr,
                                      int(self.param_sm), value)
            else:
                self.io.write_fmt(self.pctrl_addr, 'Hd',
                                  int(self.param_sm), value)

    def set_param_cmd(self, cmd, sub, idx):
        self.param_sm.CMD = cmd
        self.param_sm.SUB = sub
        self.param_sm.IDX = idx
        self.io.write_u16(self.pctrl_addr, int(self.param_sm))

    def get_param_value(self, idx):
        if idx < FIRST_FLOAT_PARAM:
            if self.value_size == 4:
                return self.io.read_u32(self.param_addr)
            else:
                return self.io.read_u64(self.param_addr)
        else:
            if self.value_size == 4:
                return self.io.read_f32(self.param_addr)
            else:
                return self.io.read_f64(self.param_addr)

    def list_params(self):
        return self.param_map.init_keys()

    def get_param(self, name, subdev=0):
        idx = self.param_map.get(name)
        if idx:
            if self.wait_sm_available():
                self.set_param_cmd(ParamCMDs.DO_READ, subdev, idx)
                # now wait until setting parameter is finished and
                # return read-back-value
                if self.wait_sm_available():
                    return self.param_sm.CMD, self.get_param_value(idx)
            return ParamCMDs.ERR_RETRY, None
        return ParamCMDs.ERR_NO_IDX, None

    def set_param(self, name, value, subdev=0):
        idx = self.param_map.get(name)
        if idx:
            if self.wait_sm_available():
                self.set_param_value_and_cmd(ParamCMDs.DO_WRITE,
                                             subdev, idx, value)
                # now wait until setting parameter is finished and
                # return read-back-value
                if self.wait_sm_available():
                    return self.param_sm.CMD, self.get_param_value(idx)
            return ParamCMDs.ERR_RETRY, None
        return ParamCMDs.ERR_NO_IDX, None

    def list_funcs(self):
        return self.func_map.init_keys()

    def exec_func(self, name, value=None, subdev=0):
        idx = self.func_map.get(name)
        if idx:
            self.update_param_sm()
            if self.param_sm.CMD == ParamCMDs.BUSY and \
               self.param_sm.SUB == subdev and \
               self.param_sm.IDX == idx:
                self.set_param_value(idx, value)
                if self.wait_sm_available():
                    return self.param_sm.CMD, self.get_param_value(idx)
                return self.param_sm.CMD, self.get_param_value(idx)  # still BUSY
            if self.wait_sm_available():
                self.set_param_value_and_cmd(ParamCMDs.DO_WRITE,
                                             subdev, idx, value or 0)
                # now wait until setting parameter is finished and return
                # read-back-value
                if self.wait_sm_available():
                    return self.param_sm.CMD, self.get_param_value(idx)
                return self.param_sm.CMD, self.get_param_value(idx)  # still BUSY
            return ParamCMDs.ERR_RETRY, None
        return ParamCMDs.ERR_NO_IDX, None


class ParamIn(ParamInterface, AnalogDevice):
    """Class for :ref:`pils:dev-paraminput`, :ref:`pils:dev-param64input`."""


class ParamOut(ParamInterface, AnalogDevice):
    """Class for :ref:`pils:dev-paramoutput`, :ref:`pils:dev-param64output`."""


class VectorDevice(Device):
    """Base class for Vector devices."""

    def _init(self):
        pass

    def get_limits(self):
        if self.value_size == 4:
            return (-FLOAT32_MAX, FLOAT32_MAX)
        elif self.value_size == 8:
            return (-FLOAT64_MAX, FLOAT64_MAX)
        raise SpecError('invalid value_size')

    def read_value(self):
        if self.value_size == 4:
            return self.io.read_f32s(self.addr, self.num_values)
        elif self.value_size == 8:
            return self.io.read_f64s(self.addr, self.num_values)
        raise SpecError('invalid value_size')


class VectorIn(ParamInterface, VectorDevice):
    """Class for :ref:`pils:dev-vectorinput`, :ref:`pils:dev-vector64input`."""


class VectorOut(ParamInterface, VectorDevice):
    """Class for :ref:`pils:dev-vectoroutput`,
    :ref:`pils:dev-vector64output`."""

    def read_target(self):
        if self.value_size == 4:
            return self.io.read_f32s(self.target_addr, self.num_values)
        elif self.value_size == 8:
            return self.io.read_f64s(self.target_addr, self.num_values)
        raise SpecError('invalid value_size')

    def change_target(self, value):
        if self.value_size == 4:
            self.io.write_f32s_u16(self.target_addr, value, START16)
        elif self.value_size == 8:
            self.io.write_f64s_u32(self.target_addr, value, START32)


# Note: has_target means that a target field is there, not that the device
# is considered read-only.
Type = namedtuple(
    'Type',
    'devcls value_fmt num_values has_target status_size num_params has_pctrl')


TYPECODE_MAP = {
    0x1201: Type(SimpleDiscreteIn,  'h', 1, False, 0, 0, False),
    0x1202: Type(SimpleDiscreteIn,  'i', 1, False, 0, 0, False),
    0x1204: Type(SimpleDiscreteIn,  'q', 1, False, 0, 0, False),
    0x1302: Type(SimpleAnalogIn,    'f', 1, False, 0, 0, False),
    0x1304: Type(SimpleAnalogIn,    'd', 1, False, 0, 0, False),
    0x1401: Type(Keyword,           'H', 1, False, 0, 0, False),
    0x1402: Type(Keyword,           'I', 1, False, 0, 0, False),
    0x1404: Type(Keyword,           'Q', 1, False, 0, 0, False),
    0x1502: Type(RealValue,         'f', 1, False, 0, 0, False),
    0x1504: Type(RealValue,         'd', 1, False, 0, 0, False),
    0x1602: Type(SimpleDiscreteOut, 'h', 1, True,  0, 0, False),
    0x1604: Type(SimpleDiscreteOut, 'i', 1, True,  0, 0, False),
    0x1608: Type(SimpleDiscreteOut, 'q', 1, True,  0, 0, False),
    0x1704: Type(SimpleAnalogOut,   'f', 1, True,  0, 0, False),
    0x1708: Type(SimpleAnalogOut,   'd', 1, True,  0, 0, False),
    0x1801: Type(StatusWord,        'H', 1, False, 2, 0, False),
    0x1802: Type(StatusWord,        'I', 1, False, 4, 0, False),
    0x1a02: Type(DiscreteIn,        'h', 1, False, 2, 0, False),
    0x1a04: Type(DiscreteIn,        'i', 1, False, 4, 0, False),
    0x1a08: Type(DiscreteIn,        'q', 1, False, 6, 0, False),
    0x1b03: Type(AnalogIn,          'f', 1, False, 2, 0, False),
    0x1b04: Type(AnalogIn,          'f', 1, False, 4, 0, False),
    0x1b08: Type(AnalogIn,          'd', 1, False, 6, 0, False),
    0x1e03: Type(DiscreteOut,       'h', 1, True,  2, 0, False),
    0x1e06: Type(DiscreteOut,       'i', 1, True,  4, 0, False),
    0x1e0c: Type(DiscreteOut,       'q', 1, True,  6, 0, False),
    0x1f05: Type(AnalogOut,         'f', 1, True,  2, 0, False),
    0x1f06: Type(AnalogOut,         'f', 1, True,  4, 0, False),
    0x1f0c: Type(AnalogOut,         'd', 1, True,  6, 0, False),

    0x4006: Type(ParamIn,           'f', 1, False, 2, 1, True),
    0x400c: Type(ParamIn,           'd', 1, False, 6, 1, True),
    0x5008: Type(ParamOut,          'f', 1, True,  2, 1, True),
    0x5010: Type(ParamOut,          'd', 1, True,  6, 1, True),
}

for n in range(16):
    fin32  = 0x2000 | (n << 8) | (6 + 2*n)
    fin64  = 0x2000 | (n << 8) | (12 + 4*n)
    fout32 = 0x3000 | (n << 8) | (8 + 2*n)
    fout64 = 0x3000 | (n << 8) | (16 + 4*n)
    TYPECODE_MAP[fin32]  = Type(FlatIn,  'f', 1, False, 2, n+1, False)
    TYPECODE_MAP[fin64]  = Type(FlatIn,  'd', 1, False, 6, n+1, False)
    TYPECODE_MAP[fout32] = Type(FlatOut, 'f', 1, True,  2, n+1, False)
    TYPECODE_MAP[fout64] = Type(FlatOut, 'd', 1, True,  6, n+1, False)

    if n == 0:
        continue

    vin32  = 0x4000 | (n << 8) | (6 + 2*n)
    vin64  = 0x4000 | (n << 8) | (12 + 4*n)
    vout32 = 0x5000 | (n << 8) | (8 + 4*n)
    vout64 = 0x5000 | (n << 8) | (16 + 8*n)
    TYPECODE_MAP[vin32]  = Type(VectorIn,  'f', n+1, False, 2, 1, True)
    TYPECODE_MAP[vin64]  = Type(VectorIn,  'd', n+1, False, 6, 1, True)
    TYPECODE_MAP[vout32] = Type(VectorOut, 'f', n+1, True,  2, 1, True)
    TYPECODE_MAP[vout64] = Type(VectorOut, 'd', n+1, True,  6, 1, True)


def typecode_description(typecode):
    typeinfo = TYPECODE_MAP[typecode]
    name = typeinfo.devcls.__name__
    valuesize = calcsize(typeinfo.value_fmt)
    if typeinfo.num_params > 0 and not typeinfo.has_pctrl:
        name += f'/{typeinfo.num_params}'
    if typeinfo.num_values > 1:
        name += f'/{typeinfo.num_values}'
    if typecode in (0x1b03, 0x1f05):
        name += ' (32 bit, legacy)'
    else:
        name += f' ({valuesize*8} bit)'
    return name
