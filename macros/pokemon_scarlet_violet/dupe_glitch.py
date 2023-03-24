#!/usr/bin/env python
# SPDX-FileCopyrightText: 2023 habchab
# SPDX-License-Identifier: GPL-3.0-only

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).absolute().parent.parent.parent))

import itertools
from pokken_controller import (
    SpinlockDelay,
    PokkenController,
    PokkenControllerButtons as BTN,
    PokkenControllerHat as HAT,
)

spinlock = SpinlockDelay()
pc = PokkenController()

def write_for(f, duration, b):
    f.write(b)
    f.flush()
    spinlock.delay(duration)


dupe_cmds = [
    [   300 , 150, HAT.W ], # Start on "Boxes", left to Koraidon.
    [   400 , 200, BTN.A ], # Select Koraidon.
    [   150 , 150, HAT.W ], #
    [   200 , 200, HAT.N ], # Go to "Return to ride form"
    [  1600 , 150, BTN.A ], # "Do you want Koraidon to change into its ride form?"
    [   300 , 150, BTN.A ], # Acknowledge text box.
    [  2700 , 150, BTN.A ], # Select Yes.
    [   400 , 150, BTN.B ], # "Koraidon is ready for travel!"
    [   200 , 200, HAT.N ], #
    [   200 , 200, HAT.E ], #
    [  2700 , 150, BTN.A ], # Up and right to boxes.
    [   300 , 150, BTN.X ], #
    [   300 , 150, BTN.X ], # Battle Teams
    [   700 , 200, BTN.L ], # Left from Box 1 to Koraidon Box.
    [   500 , 250, BTN.A ], # Select Koraidon.
    [   150 , 150, HAT.W ], #
    [   200 , 100, HAT.N ], #
    [   200 , 100, HAT.N ], # "Put away held item"
    [   400 , 150, BTN.A ], #
    [  2300 , 150, BTN.B ], # Back to Main Menu.
]

tm_swap_cmds = [
    [   300 , 200, HAT.N ], # Start on "Boxes".
    [  2700 , 200, BTN.A ], # Up to bag.
    [   400 , 200, HAT.E ], #
    [   400 , 200, HAT.E ], #
    [   400 , 200, HAT.E ], #
    [   400 , 200, HAT.E ], #
    [   400 , 200, HAT.E ], # Right to TM column.
    [   400 , 200, HAT.S ], #
    [   400 , 200, BTN.A ], # Select next TM.
    [   400 , 200, HAT.S ], #
    [   800 , 200, BTN.A ], # Give to Pokemon.
    [   400 , 200, HAT.S ], #
    [  1000 , 200, BTN.A ], # Select second pokemon, Koraidon.
    [  1000 , 200, BTN.A ], # Swap? Confirm.
    [   800 , 200, BTN.B ], #
    [   800 , 200, BTN.B ], # Back to menu.
    [   400 , 200, HAT.S ], # Hover "Boxes".
]

def do_cmds(f, cmds, iters=1):
    for i, c in itertools.product(range(iters), cmds):
        write_for(f, c[1], pc.press(c[2]).do())
        if c[0] <= c[1]:
            continue
        write_for(f, c[0], pc.idle().do())


def main():
    with open('/dev/hidg0', 'wb') as f:
        try:
            spinlock.reset_time()
            do_cmds(f, dupe_cmds, 990)
        except KeyboardInterrupt:
            pass
        finally:
            write_for(f, 200, pc.press(BTN.HOME).do())
            write_for(f, 0, pc.idle().do())

def dupe_all_tms():
    with open('/dev/hidg0', 'wb') as f:
        try:
            spinlock.reset_time()
            for tm in range(171):
                print('TM offset {}'.format(tm))
                do_cmds(f, dupe_cmds, 8)
                do_cmds(f, tm_swap_cmds, 1)
        except KeyboardInterrupt:
            pass
        finally:
            write_for(f, 200, pc.press(BTN.HOME).do())
            write_for(f, 0, pc.idle().do())


if __name__ == "__main__":
    # dupe_all_tms()
    main()