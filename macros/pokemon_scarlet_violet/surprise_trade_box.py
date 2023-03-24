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


def boxes_navigate(row, col):
    if row > 4:
        raise ValueError('Row cannot be more than 4.')
    if col > 5:
        raise ValueError('Col cannot be more than 5.')
    while row > 0 or col > 0:
        if col > 0:
            write_for(100, pc.press(HAT.E).do())
            col -= 1
        else:
            write_for(100, pc.idle().do())
        if row > 0:
            write_for(100, pc.press(HAT.S).do())
            row -= 1
        else:
            write_for(100, pc.idle().do())
    write_for(100, pc.idle().do())


def surprise_trade(rows=5, cols=6):
    from itertools import product
    for row, col in product(reversed(range(rows)), reversed(range(cols))):
        print('Trading pokemon ({}, {}).'.format(row, col))
        # Go to pokemon.
        boxes_navigate(row, col)
        # Select.
        write_for(200, pc.press(BTN.A).do())
        write_for(500, pc.idle().do())
        # Trade it. Wait for "Communicating".
        write_for(200, pc.press(BTN.A).do())
        write_for(3000, pc.idle().do())
        # Save progress and start trading.
        write_for(200, pc.press(BTN.A).do())
        write_for(1200, pc.idle().do())
        # Accept.
        write_for(200, pc.press(BTN.A).do())
        write_for(1000, pc.idle().do())
        write_for(200, pc.press(BTN.A).do())
        write_for(5000, pc.idle().do())
        # Open menu.
        write_for(200, pc.press(BTN.X).do())
        write_for(1000, pc.idle().do())
        # Poke Portal. Wait for Surprise Trade to occur.
        write_for(200, pc.press(BTN.A).do())
        write_for(11000, pc.idle().do())
        # Surprise Trade.
        write_for(200, pc.press(BTN.A).do())
        write_for(29000, pc.idle().do())
        # Begin another surprise trade?
        write_for(200, pc.press(BTN.A).do())
        write_for(3000, pc.idle().do())


with open('/dev/hidg0', 'wb') as f:
    try:
        spinlock.reset_time()
        surprise_trade()
    except KeyboardInterrupt:
        pass
    finally:
        write_for(0, pc.idle().do())
