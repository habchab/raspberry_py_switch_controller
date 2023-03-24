#!/usr/bin/env python
# SPDX-FileCopyrightText: 2023 habchab
# SPDX-License-Identifier: GPL-3.0-only

import time, math, struct
import numpy as np
from enum import Enum, Flag

class SpinlockDelay:

    def __init__(self):
        self.time_unit = 1  # ms
        self.reset_time()

    def set_time_unit(self, t_ms):
        self.time_unit = t_ms

    def get_time(self):
        return math.floor(time.perf_counter_ns() / (self.time_unit * 1e6))

    def reset_time(self):
        self.now = self.get_time()

    def delay(self, duration=0):
        duration_in_ms = duration * self.time_unit
        if duration_in_ms > 50:  # minimum time to use time.sleep()
            time.sleep(0.001 * (duration_in_ms - 50))
        t_stop = self.now + duration
        self.now += duration
        t_flr = self.get_time()
        while t_flr < t_stop:
            t_flr = self.get_time()


class PokkenControllerButtons(Flag):
    IDLE    = 0
    Y       = 1 <<  0
    B       = 1 <<  1
    A       = 1 <<  2
    X       = 1 <<  3
    L       = 1 <<  4
    R       = 1 <<  5
    ZL      = 1 <<  6
    ZR      = 1 <<  7
    MINUS   = 1 <<  8
    PLUS    = 1 <<  9
    L3      = 1 << 10
    R3      = 1 << 11
    HOME    = 1 << 12
    CAPTURE = 1 << 13

class PokkenControllerHat(Enum):
    N   = 0
    NE  = 1
    E   = 2
    SE  = 3
    S   = 4
    SW  = 5
    W   = 6
    NW  = 7
    Z   = 8

class PokkenController:

    def __init__(self):
        self.idle()

    def idle(self):
        self.state_button   = PokkenControllerButtons.IDLE
        self.state_hat      = PokkenControllerHat.Z
        self.state_stick_l  = (0.0, 0.0)
        self.state_stick_r  = (0.0, 0.0)
        return self

    def press_button(self, buttons):
        self.state_button |= buttons
        return self

    def press_hat(self, hat):
        self.state_hat = hat
        return self

    def press(self, action):
        if action in PokkenControllerButtons:
            self.press_button(action)
        elif action in PokkenControllerHat:
            self.press_hat(action)
        return self

    def press_hat(self, hat):
        self.state_hat = hat
        return self

    def tilt_stick_l(self, stick_l):
        self.state_stick_l = stick_l
        return self

    def tilt_stick_r(self, stick_r):
        self.state_stick_r = stick_r
        return self

    def float_to_stick_value(self, x):
        s = round(0x80 * (x+1))
        s = np.clip(s, 0x00, 0xff)
        if s == 0x100:
            s = 0xff
        return int(s)

    def do(self):
        button  = self.state_button.value
        hat     = self.state_hat.value
        lx      = self.float_to_stick_value(self.state_stick_l[0])
        ly      = self.float_to_stick_value(self.state_stick_l[1])
        rx      = self.float_to_stick_value(self.state_stick_r[0])
        ry      = self.float_to_stick_value(self.state_stick_r[1])
        self.idle()
        return struct.pack('HBBBBBB', button, hat, lx, ly, rx, ry, 0)


def main():
    spinlock = SpinlockDelay()
    pc = PokkenController()

    spinlock.reset_time()
    for i in range(10):
        spinlock.delay(100)
        pokken_state = pc.tilt_stick_l((1, 0)).press(PokkenControllerButtons.L3).tilt_stick_r((0, 1)).do()
        print('{:.7f} : {}'.format(time.time(), pokken_state))

if __name__ == "__main__":
    main()
