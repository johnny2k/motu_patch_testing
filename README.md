# motu_patch_testing
Tools, tests, and build scripts to help test Motu patches and firmware. 

### Scripts (bin)

Various scripts are in bin. Some will require modifying to work on various systems.

* collect_system_info.sh - Creates a directory with text files to contain data about the system (uname, lsusb. lspci, moto USB string)
* enable_audio_debug.sh - Shortcut to enabling audio debugging. Might need to change line numbers on your system. Read the comments for more info.
* motu-setup.sh - Uses curl to set vendor mode, sample rate, buffer size, safety offset. Set IP in the script before using.
* motu-setup.py - More advanced setup using python. Allows storing of parameters in a config-file. Also automatically retreives correct UID.
* motu-status.sh - Get configuration info from the device. Set IP in the script before using.
* patch_and_build.sh - Mostly a reference for how to build but could be made into a more robust build script

### Tests

This contains various configurations to test, common manual tests, and some automated tests.
