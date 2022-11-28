##Enable debug logging

Summarized notes based on the Instructions provided by AudioNarwhal (https://linuxmusicians.com/viewtopic.php?p=150148#p150148)

###Check to see if dynamic debug is enabled

    cat /boot/config-$(uname -r) | grep DYNAMIC_DEBUG

Success looks like....
    CONFIG_DYNAMIC_DEBUG=y
    CONFIG_DYNAMIC_DEBUG_CORE=y

TODO: Link to instructions on how to enable and rebuild the kernel

###Check to see if debugfs is mounted
    mount | grep debugfs

###Success looks like...
    debugfs on /sys/kernel/debug type debugfs (rw,nosuid,nodev,noexec,relatime) 

###Mount if not already mounted
    sudo mount -t debugfs none /sys/kernel/debug

This directory should exist....
    sudo ls /sys/kernel/debug/dynamic_debug

###Enable dynamic debug logging for snd-usb-audio and xhci_hcd
    sudo sh -c 'echo "module snd_usb_audio +p" > /sys/kernel/debug/dynamic_debug/control'
    sudo sh -c 'echo "module xhci_hcd +p" > /sys/kernel/debug/dynamic_debug/control'

###Eliminate exrta noisy logging. 
    sudo cat /sys/kernel/debug/dynamic_debug/control | grep "asked for" | grep -Po "xhci-ring.c:\K[[:digit:]]*"

###Replace the "line 2538 and 2531 with whatever numbers from the previous step.
    sudo sh -c 'echo "file xhci-ring.c line 2538 -p" > /sys/kernel/debug/dynamic_debug/control'
    sudo sh -c 'echo "file xhci-ring.c line 2531 -p" > /sys/kernel/debug/dynamic_debug/control'

### View logs
    sudo dmesg -w
