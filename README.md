# Raspberry Pi Nintendo Switch controller

Nintendo Switch controller emulated with Raspberry Pi, usb_gadget, and Python. Macro capable.
The USB descriptor used is an extension of the Pokken controller's descriptor.

## Setup
1. Enable usb_gadget on Raspberry Pi 4 or Raspberry Pi Zero W.

        echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
        echo "dwc2" | sudo tee -a /etc/modules
        echo "libcomposite" | sudo tee -a /etc/modules
        sudo reboot now

1. Optional: Install chrony for that sweet millisecond accuracy.

        sudo apt install chrony

1. Create USB Gadget: /dev/hidg0

        sudo ./create_pokken_controller.sh

## Xbox Controller Passthrough to Nintendo Switch
Controller passthrough is available with evdev.

    sudo apt install pip
    pip3 install evdev

Read Xbox controller data from /dev/input/event0 (default) and convert to Pokken controller data.

    ./py_evdev_xbox.py >/dev/hidg0

Note, scripts can run concurrently, but inputs from the controller may only be useful during pauses.

## Xbox Controller over LAN (Educational)
The controller data can be streamed over LAN with e.g. netcat.

On the Raspberry Pi connected to the Nintendo Switch:

    nc -klu -p44329 >/dev/hidg0

On the system with the controller plugged in (might need to add argument to select device event#):

    ./py_evdev_xbox.py | nc -u raspberrypi 44329

Wi-Fi drops occasional UDP packets, so this isn't practical.
SSH can probably be used but might incur weird latency issues.
Ethernet had the best performance, of course.

## References
1. https://github.com/FeralAI/MPG
1. https://github.com/progmem/Switch-Fightstick
1. https://github.com/mzyy94/nscon
    1. https://www.mzyy94.com/blog/2020/03/20/nintendo-switch-pro-controller-usb-gadget/
    1. https://gist.github.com/mzyy94/60ae253a45e2759451789a117c59acf9#file-add_procon_gadget-sh
    1. https://gist.github.com/mzyy94/02bcd9d843c77896803c4cd0c4d9b640#file-procon_audio-sh
1. https://github.com/omakoto/raspberry-switch-control
1. https://github.com/milador/RaspberryPi-Joystick
1. https://github.com/KawaSwitch/Poke-Controller
1. https://github.com/larsks/systemd-usb-gadget/blob/master/remove-gadget.sh
