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


with open('/dev/hidg0', 'wb') as f:
    try:
        spinlock.reset_time()
        for __ in range(700):
            for hat in [HAT.N, HAT.E, HAT.S, HAT.W]:
                write_for(16.66666, pc.press(hat).do())
    except KeyboardInterrupt:
        pass
    finally:
        write_for(0, pc.idle().do())
