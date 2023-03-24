#!/usr/bin/env python
# SPDX-FileCopyrightText: 2023 habchab
# SPDX-License-Identifier: GPL-3.0-only

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).absolute().parent.parent.parent))

from pokken_controller import (
    SpinlockDelay,
    PokkenController,
    PokkenControllerButtons as BTN,
    PokkenControllerHat as HAT,
)

spinlock = SpinlockDelay()
pc = PokkenController()

def write_for(duration, b):
    f.write(b)
    f.flush()
    spinlock.delay(duration)


ls_diamond = [
    (-1, -1),
    ( 1, -1),
    ( 1,  1),
    (-1,  1),
]
ls_octagon = [
    (-1, -1),
    ( 0, -1),
    ( 1, -1),
    ( 1,  0),
    ( 1,  1),
    ( 0,  1),
    (-1,  1),
    (-1,  0),
]

def boxes_open():
    write_for(200, pc.press(BTN.X).do())
    write_for(500, pc.idle().do())
    write_for(100, pc.press(BTN.A).do())
    write_for(3000, pc.idle().do())

def boxes_place(column, start_col=0):
    print('Right to column.')
    for col in range(column-start_col):
        write_for(100, pc.press(HAT.E).do())
        write_for(100, pc.idle().do())
    print('Selecting column.')
    write_for(100, pc.press(BTN.MINUS).do())
    write_for(100, pc.idle().do())
    for row in range(4-1):
        write_for(100, pc.press(HAT.S).do())
        write_for(100, pc.idle().do())
    write_for(100, pc.press(BTN.A).do())
    write_for(100, pc.idle().do())
    print('Left to party.')
    for col in range(column+1):
        write_for(100, pc.press(HAT.W).do())
        write_for(100, pc.idle().do())
    for row in range(2):
        write_for(100, pc.press(HAT.S).do())
        write_for(100, pc.idle().do())
    write_for(100, pc.press(BTN.A).do())
    write_for(100, pc.idle().do())

def boxes_return(column=0):
    print('Left to party.')
    write_for(100, pc.press(HAT.W).do())
    write_for(100, pc.idle().do())
    for row in range(2):
        write_for(100, pc.press(HAT.S).do())
        write_for(100, pc.idle().do())
    print('Selecting party.')
    write_for(100, pc.press(BTN.MINUS).do())
    write_for(100, pc.idle().do())
    for row in range(4-1):
        write_for(100, pc.press(HAT.S).do())
        write_for(100, pc.idle().do())
    write_for(100, pc.press(BTN.A).do())
    write_for(100, pc.idle().do())
    for row in range(2):
        write_for(100, pc.press(HAT.N).do())
        write_for(100, pc.idle().do())
    print('Right to column.')
    for col in range(column+1):
        write_for(100, pc.press(HAT.E).do())
        write_for(100, pc.idle().do())
    write_for(100, pc.press(BTN.A).do())
    write_for(100, pc.idle().do())

def boxes_close():
    write_for(200, pc.press(BTN.B).do())
    write_for(1500, pc.idle().do())
    write_for(200, pc.press(BTN.B).do())
    write_for(500, pc.idle().do())


def run_around():
    for lap in range(41):
        print('Main lap {}/41.'.format(lap))
        for ls in ls_octagon:
            write_for(100, pc.tilt_stick_l(ls).tilt_stick_r((1/8, 1)).press(BTN.L3).do())
            write_for(150, pc.tilt_stick_l(ls).tilt_stick_r((1/8, 1)).do())
    for egg in range(4):
        for lap in range(4):
            print('Secondary lap {}/4'.format(lap))
            for ls in ls_octagon:
                write_for(100, pc.tilt_stick_l(ls).tilt_stick_r((1/8, 1)).press(BTN.L3).do())
                write_for(150, pc.tilt_stick_l(ls).tilt_stick_r((1/8, 1)).do())
        print('Laps finished.')
        write_for(200, pc.press(BTN.A).do())
        print('Waiting 14 sec.')
        write_for(13800, pc.idle().do())
        print('Pressing B.')
        write_for(200, pc.press(BTN.B).do())
        write_for(1800, pc.idle().do())
        print('Egg done.')
    write_for(1000, pc.idle().do())
    print('Run done.')

def hatch_eggs():
    boxes_open()
    boxes_place(0)
    boxes_close()
    for col in range(0, 5):
        run_around()
        boxes_open()
        boxes_return(col)
        boxes_place(col+1, col)
        boxes_close()
    run_around()
    boxes_open()
    boxes_return(5)
    boxes_close()


def just_run_around():
    with open('/dev/hidg0', 'wb') as f:
        try:
            spinlock.reset_time()
            run_around()
        except KeyboardInterrupt:
            pass
        write_for(0, pc.idle().do())


# Start with eggs in party already.
with open('/dev/hidg0', 'wb') as f:
    try:
        spinlock.reset_time()
        for col in range(0, 5):
            run_around()
            boxes_open()
            boxes_return(col)
            boxes_place(col+1, col)
            boxes_close()
        run_around()
        boxes_open()
        boxes_return(5)
    except KeyboardInterrupt:
        pass
    write_for(0, pc.idle().do())


def spam_a():
    for a_press in range(600):
        write_for(100, pc.press(BTN.A).do())
        write_for(100, pc.idle().do())

# with open('/dev/hidg0', 'wb') as f:
#     try:
#         spinlock.reset_time()
#         for minute_4 in range(32//4):
#             print('minute {}.'.format(minute_4 * 4))
#             write_for(4*60*1000, pc.idle().do())
#             for a_press in range(5*20):
#                 write_for(100, pc.press(BTN.A).do())
#                 write_for(100, pc.idle().do())
#             for b_press in range(5*5):
#                 write_for(100, pc.press(BTN.B).do())
#                 write_for(100, pc.idle().do())
#     except KeyboardInterrupt:
#         pass
#     write_for(0, pc.idle().do())
