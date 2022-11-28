mkdir system_info && cd system_info

# Kernel
uname -r > kernel.txt

# USB Devices
lsusb -vvvv > lsusb.txt

# Motu device
lsusb | grep "07fd" > motu_device.txt

# PCI devices
lspci -vvvk > lspci.txt

cd ..
