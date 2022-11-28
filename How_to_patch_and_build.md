Using instructions from baptiste (https://linuxmusicians.com/viewtopic.php?p=150112#p150112)

### From the kernel source directory
patch -p1 < ../snd-usb-audio-printk-6.0.3.patch

### Prepare the build
make mrproper
make olddefconfig
make prepare
make scripts
cd sound/usb
cp /usr/src/linux-headers-$(uname -r)/Module.symvers .

### Build
make -C /lib/modules/`uname -r`/build M=$PWD

### Backup old module
sudo mv /usr/lib/modules/$(uname -r)/kernel/sound/usb/snd-usb-audio.ko /usr/lib/modules/$(uname -r)/kernel/sound/usb/snd-usb-audio.ko.bkp

### Install new module
sudo cp sound/usb/snd-usb-audio.ko /usr/lib/modules/$(uname -r)/kernel/sound/usb
