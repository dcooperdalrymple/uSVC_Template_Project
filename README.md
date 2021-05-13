# uSVC Template Project
Interested in developing for the uSVC but don't want to mess around with Windows or Microchip Studio? This template gives you the tools to easily develop for the SAMD21 chip on the uSVC while staying comfortable in a properly configured Linux shell.

## Requirements

### Arm Embedded Toolchain
To build this project, you must have the [GNU Arm Embedded Toolchain](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm) installed. Details on this process can be found on the [arm website](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads).

### uChipGameMapEditor
To use the Map Editor, it is required that you have JDK installed. See the [uChipGameMapEditor repository](https://github.com/next-hack/uChipGameMapEditor) and this [next-hack post](https://next-hack.com/index.php/2020/09/18/uchip-game-map-editor/) for more details.

In the future, I may convert some of the included utilities into Python to make the process of packaging up your project's .usc file easier.

### BOSSA Flash Programming Utility
The utility used to debug your program on the uSVC, [BOSSA](https://www.shumatech.com/web/products/bossa), is included in this repository as the CLI version, bossac. If you have compatibility issues with this executable, you may want to try recompiling it from the source on [ShumaTech's repository](https://github.com/shumatech/BOSSA). To compile only the bossac version with less requirements, use the command `make bossac` in the repository's root folder.

### uSVC USC Packager
This repository includes a Python 3 port of the uChipGameMapEditor .USC packaging utility. This allows you to package up your game's binary into a handy .usc file for SD card loading from the bootloader using the command line.

In order to use this utility, you will need to have any version of Python 3 installed (3.9.2 recommended). You can do this on Debian/Ubuntu using `sudo apt-get update || sudo apt-get install python3.9` (more details can be found [here](https://docs.python-guide.org/starting/install3/linux/)).

You will also need to install [Pillow](https://pillow.readthedocs.io/en/stable/installation.html) for image processing using [pip](https://pip.pypa.io/en/stable/installing/). You can do this using `python3 -m pip install --upgrade pip || python3 -m pip install --upgrade Pillow`.

If any other Python modules are not included in your environment, the program should tell you when executed.

## Compilation & Debugging

### Compiling the Program
Compiling this project is simple using the provided Makefile. Just call `make` in the root folder of this repository to build the entire project.

### Debugging on the uSVC
To debug this project on your uSVC console, plug the device's uChip port (the micro USB connector on the front of the device) into your computer. To start the uChip in bootloader mode, click the reset button twice and the led should begin a slow pulsing cycle. You may need to update the port specified in the Makefile depending on your computer's device configuration. You can call `sudo make list` to attempt to display the attached device's serial port and update the PORT variable (should be something like ttyACM0). Once you have everything ready, use `make debug` to send the program over to your device. If the process went successfully, the uSVC's led will begin flashing on and off every second, but the VGA output should only be displaying a black screen.

### Packing your Game
Using the makefile and the USC Packager python utility, packaging up your game into a .usc file should be very easy. All you will have to do is run `make || make package` in the root directory. Your .usc file should then be located in the `release` directory. You can then copy this file to your SD card and run it from a uSVC with the bootloader installed. You can read more about this process on [next-hack.com](https://next-hack.com/index.php/2021/05/02/usvc-tutorial-8-how-to-run-usvc-games-from-sd-card/).

## Writing Your Game
For more information on how to get starting developing for the uSVC, please visit the [next-hack.com website](https://next-hack.com/index.php/category/usvc/) for tutorials and more detailed information.

## Contributions
The uSVC kernel and Template files (main, usvc_config.h, Device_Startup) are provided by [next-hack](https://next-hack.com/) from their [uSVC repository](https://github.com/next-hack/uSVC/tree/master/software/uSVC_Template_Project). The [BOSSA flash programming utility](https://www.shumatech.com/web/products/bossa) included (specifically bossac) is compiled from ShumaTech's [source code repository](https://github.com/shumatech/BOSSA) version 1.9.1.
