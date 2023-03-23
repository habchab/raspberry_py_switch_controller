#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2023 habchab
# SPDX-License-Identifier: GPL-3.0-only
#
# Original script from https://gist.github.com/mzyy94/60ae253a45e2759451789a117c59acf9#file-add_procon_gadget-sh
#
# Modified script from https://github.com/omakoto/raspberry-switch-control/blob/1703e6c1f0c98e564c74745f45d1831a1fc08253/scripts/switch-controller-gadget
#
# Switch descriptor data from https://github.com/FeralAI/MPG/blob/b009f021e9fb033bac79dfd6c7547539d80d28f1/src/descriptors/SwitchDescriptors.h
#   Copyright (c) 2021 Jason Skuby (mytechtoybox.com)

device=/dev/hidg0

if [[ -e $device ]]; then
    echo "Device $device already exists" 1>&2
    exit 0
fi

set -e

cd /sys/kernel/config/usb_gadget/
mkdir -p pokkencon
cd pokkencon
echo 0x0f0d > idVendor
echo 0x0092 > idProduct
echo 0x0100 > bcdDevice
echo 0x0200 > bcdUSB

mkdir -p strings/0x409/
echo "000000000001" > strings/0x409/serialnumber
echo "HORI CO.,LTD." > strings/0x409/manufacturer
echo "POKKEN CONTROLLER" > strings/0x409/product

mkdir -p configs/c.1/strings/0x409/
echo "" > configs/c.1/strings/0x409/configuration
echo 500 > configs/c.1/MaxPower
echo 0x80 > configs/c.1/bmAttributes

mkdir -p functions/hid.usb0
echo 0 > functions/hid.usb0/protocol
echo 0 > functions/hid.usb0/subclass
echo 64 > functions/hid.usb0/report_length
echo 05010905A101150025013500450175019510050919012910810205012507463B017504950165140939814265009501810126FF0046FF0009300931093209357508950481020600FF0920950181020A212695089102C0 | xxd -r -ps > functions/hid.usb0/report_desc

ln -s functions/hid.usb0 configs/c.1/

ls /sys/class/udc > UDC

chmod 666 $device

ls -l $device
