#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2023 habchab
# SPDX-License-Identifier: GPL-3.0-only

device=/dev/hidg0

if [[ ! -e $device ]]; then
    echo "Device $device doesn't exist" 1>&2
    exit 0
fi

cd /sys/kernel/config/usb_gadget/pokkencon/
echo "" > UDC

rm configs/c.1/hid.usb0
rmdir configs/c.1/strings/0x409/
rmdir configs/c.1/
rmdir functions/hid.usb0/
rmdir strings/0x409/

cd ..
rmdir pokkencon/
