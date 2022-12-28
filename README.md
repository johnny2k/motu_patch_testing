# motu_patch_testing
Tools, tests, and build scripts to help test Motu patches and firmware. 

### Scripts (bin)
Various scripts are in bin. Some will require modifying to work on various systems.

* collect_system_info.sh - Creates a directory with text files to contain data about the system (uname, lsusb. lspci, moto USB string)
* enable_audio_debug.sh - Shortcut to enabling audio debugging. Might need to change line numbers on your system. Read the comments for more info.
* motu-setup.sh - Uses curl to set vendor mode, sample rate, buffer size, safety offset. Set IP in the script before using.
* motu-setup.py - More advanced setup using python. Allows storing of parameters in an automatically generated config-file (no need for manual editing). Also automatically retreives correct UID.
* motu-status.sh - Get configuration info from the device. Set IP in the script before using.
* patch_and_build.sh - Mostly a reference for how to build but could be made into a more robust build script


### Link collection
1. #### Background infos:
   - ##### MOTU joins Linux discussion and provides insight:
     - https://linuxmusicians.com/viewtopic.php?p=149520#p149520
     - https://linuxmusicians.com/viewtopic.php?p=149554#p149554

2. #### Kernel patches
   - ##### MOTU shares an experimental Linux kernel Patch (based of vanilly 6.0.3):
     - https://linuxmusicians.com/viewtopic.php?p=150091#p150091
   - ##### Step-by-step guide for an out-of-tree module build (to be simplified soon):
     - https://linuxmusicians.com/viewtopic.php?p=150112#p150112

3. #### Experimental firmware from MOTU (works with and without the kernel patch above)
   - ##### (27 Nov 2022) 1.4.3+92494 (only UltraLite AVB and Stage-B16):
     - https://linuxmusicians.com/viewtopic.php?p=150411#p150411 
   - ##### (23 Dec 2022) 1.4.4+92559 (UltraLite AVB, Stage-B16, 828ES and 8PreES):
     - https://linuxmusicians.com/viewtopic.php?p=151326#p151326
   - ##### (27 Dec 2022) 1.4.5+92559 (UltraLite AVB, Stage-B16, 828ES and 8PreES):
     - https://linuxmusicians.com/viewtopic.php?p=151436#p151436
   - ##### (28 Dec 2022) 1.4.5+92559 (UltraLite-mk4):
     - https://linuxmusicians.com/viewtopic.php?p=151478#p151478

4. #### Debugging guides
   - ##### MOTU shares instructions for dynamic debugging
     - https://linuxmusicians.com/viewtopic.php?p=150148#p150148
   - ##### MOTU shares a diagnostic tool
     - https://linuxmusicians.com/viewtopic.php?p=151399#p151399

### Tests
This contains various configurations to test, common manual tests, and some automated tests.
