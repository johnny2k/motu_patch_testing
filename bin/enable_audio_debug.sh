#!/bin/bash

sudo sh -c 'echo "module snd_usb_audio +p" > /sys/kernel/debug/dynamic_debug/control'
sudo sh -c 'echo "module xhci_hcd +p" > /sys/kernel/debug/dynamic_debug/control'

# Line numbers might be different on your system check with this command ...
# sudo cat /sys/kernel/debug/dynamic_debug/control | grep "asked for" | grep -Po "xhci-ring.c:\K[[:digit:]]*"
sudo sh -c 'echo "file xhci-ring.c line 2538 -p" > /sys/kernel/debug/dynamic_debug/control'
sudo sh -c 'echo "file xhci-ring.c line 2531 -p" > /sys/kernel/debug/dynamic_debug/control'

# Clear logs before a test if you want.
#sudo dmesg -C

# Watch the logs
#sudo dmesg -w
