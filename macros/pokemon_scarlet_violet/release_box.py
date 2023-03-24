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


def release():
    # Select Pokemon.
    write_for(200, pc.press(BTN.A).do())
    write_for(200, pc.idle().do())
    # Go to Release.
    write_for(100, pc.press(HAT.W).do())
    write_for(100, pc.press(HAT.N).do())
    # Release.
    write_for(200, pc.press(BTN.A).do())
    write_for(500, pc.idle().do())
    # Do you want to release?
    write_for(100, pc.press(HAT.N).do())
    write_for(200, pc.press(BTN.A).do())
    write_for(1200, pc.idle().do())
    # Released!
    write_for(200, pc.press(BTN.A).do())
    write_for(400, pc.idle().do())


snake = [HAT.E] * 5 + [HAT.S] + \
        [HAT.W] * 5 + [HAT.S] + \
        [HAT.E] * 5 + [HAT.S] + \
        [HAT.W] * 5 + [HAT.S] + \
        [HAT.E] * 5

reset_pos_zigzag = [HAT.W, HAT.N] * 4 + [HAT.W]
def reset_position():
    for move in reset_pos_zigzag:
        write_for(100, pc.press(move).do())
    write_for(100, pc.idle().do())


def release_box():
    for move in snake:
        release()
        write_for(100, pc.press(move).do())
        write_for(100, pc.idle().do())
    reset_position()


with open('/dev/hidg0', 'wb') as f:
    try:
        spinlock.reset_time()
        release_box()
    except KeyboardInterrupt:
        pass
    finally:
        write_for(0, pc.idle().do())
