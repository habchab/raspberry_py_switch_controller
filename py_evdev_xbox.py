#!/usr/bin/env python
# SPDX-FileCopyrightText: 2023 habchab
# SPDX-License-Identifier: GPL-3.0-only

from evdev import InputDevice, categorize, ecodes
import struct
from enum import Enum

class XBoxState(Enum):
    SYNC        = (0, 0     )
    ABS_HAT0X   = (3, 0x10  )
    ABS_HAT0Y   = (3, 0x11  )
    ABS_X       = (3, 0x00  )
    ABS_Y       = (3, 0x01  )
    ABS_Z       = (3, 0x02  )
    ABS_RX      = (3, 0x03  )
    ABS_RY      = (3, 0x04  )
    ABS_RZ      = (3, 0x05  )
    KEY_RECORD  = (1, 167   )
    BTN_A       = (1, 0x130 )
    BTN_B       = (1, 0x131 )
    BTN_X       = (1, 0x133 )
    BTN_Y       = (1, 0x134 )
    BTN_TL      = (1, 0x136 )
    BTN_TR      = (1, 0x137 )
    BTN_SELECT  = (1, 0x13a )
    BTN_START   = (1, 0x13b )
    BTN_MODE    = (1, 0x13c )
    BTN_THUMBL  = (1, 0x13d )
    BTN_THUMBR  = (1, 0x13e )

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class XBoxController:

    stick_deadzone = 0.1

    def __init__(self):
        self.state = dict.fromkeys(XBoxState.list(), 0)
        self.ZL_last = 0
        self.ZR_last = 0

    def update(self, event):
        self.state[(event.type, event.code)] = event.value

    def apply_deadzone(self, x_16b):
        x_f = x_16b * 2**-15
        sign = -1 if x_f < 0 else 1
        if abs(x_f) < XBoxController.stick_deadzone:
            x_d = 0
        else:
            x_d = (x_f - sign * XBoxController.stick_deadzone)
        x_s = x_d / (1 - XBoxController.stick_deadzone)
        x_8b = round(x_s * 2**7)
        if x_8b == 0x80:
            x_8b = 0x7F
        return x_8b + 0x80

    def to_pokken(self):
        buttons = (0 |
            ( self.state[XBoxState.BTN_X.value]      <<  0) | # Y
            ( self.state[XBoxState.BTN_A.value]      <<  1) | # B
            ( self.state[XBoxState.BTN_B.value]      <<  2) | # A
            ( self.state[XBoxState.BTN_Y.value]      <<  3) | # X
            ( self.state[XBoxState.BTN_TL.value]     <<  4) | # L
            ( self.state[XBoxState.BTN_TR.value]     <<  5) | # R
            ((self.state[XBoxState.ABS_Z.value]>0)   <<  6) | # ZL
            ((self.state[XBoxState.ABS_RZ.value]>0)  <<  7) | # ZR
            ( self.state[XBoxState.BTN_SELECT.value] <<  8) | # MINUS
            ( self.state[XBoxState.BTN_START.value]  <<  9) | # PLUS
            ( self.state[XBoxState.BTN_THUMBL.value] << 10) | # L3
            ( self.state[XBoxState.BTN_THUMBR.value] << 11) | # R3
            ( self.state[XBoxState.BTN_MODE.value]   << 12) | # HOME
            ( self.state[XBoxState.KEY_RECORD.value] << 13) ) # CAPTURE
        case= (self.state[XBoxState.ABS_HAT0X.value], self.state[XBoxState.ABS_HAT0Y.value])
        if   case == ( 0,-1): hat = 0
        elif case == ( 1,-1): hat = 1
        elif case == ( 1, 0): hat = 2
        elif case == ( 1, 1): hat = 3
        elif case == ( 0, 1): hat = 4
        elif case == (-1, 1): hat = 5
        elif case == (-1, 0): hat = 6
        elif case == (-1,-1): hat = 7
        elif case == ( 0, 0): hat = 8
        else: hat = 8
        lx  = self.apply_deadzone(self.state[XBoxState.ABS_X.value])
        ly  = self.apply_deadzone(self.state[XBoxState.ABS_Y.value])
        rx  = self.apply_deadzone(self.state[XBoxState.ABS_RX.value])
        ry  = self.apply_deadzone(self.state[XBoxState.ABS_RY.value])
        pokken_state = struct.pack('HbBBBBb', buttons, hat, lx, ly, rx, ry, 0)
        return pokken_state


def main():
    import sys
    con_file    = '/dev/input/event' + (sys.argv[1] if len(sys.argv) > 1 else '0')
    gamepad     = InputDevice(con_file)
    controller  = XBoxController()
    for event in gamepad.read_loop():
        controller.update(event)
        if event.type == 0 and event.code == 0:
            sys.stdout.buffer.write( controller.to_pokken() )
            sys.stdout.flush()

if __name__ == "__main__":
    main()
