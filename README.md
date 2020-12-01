# bdsim.micropython

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/43713e0b78f547e8912ff05c9350cffb)](https://app.codacy.com/app/callumjhays/bdsim.micropython?utm_source=github.com&utm_medium=referral&utm_content=callumjhays/bdsim.micropython&utm_campaign=Badge_Grade_Dashboard)

[![Python](https://img.shields.io/badge/Python-3.6%2B-red.svg)](https://www.python.org/downloads/)

[![saythanks](https://img.shields.io/badge/say-thanks-ff69b4.svg)](https://saythanks.io/to/callumjhays)

BDSim port in micropython for the ESP32

# Installation

`numpy` doesn't exist/work for micropython, but is required by `bdsim`. Instead we use `ulab`, which provides a subset of the `numpy` API for use on micropython devices. `ulab` must be compiled from C code with the micropython firmware - it cannot be packaged by `upip`.

## On Ports with `ulab` pre-installed

If `ulab` is already installed you your target micropython device, `bdsim.micropython` may be installed through `upip`. While quick and easy to install, this method stores `bdsim` code in RAM rather than ROM - which is not ideal for resource-limited devices.

For devices with internet access:

```python
# run on micropython device
>> import upip
>> upip.install('bdsim.micropython') # install it
>> import bdsim, bdsim.micropython
>> bd = bdsim.BlockDiagram() # use it
```

For devices without internet access, `bdsim.micropython` can instead be cross-installed and then transferred into the root device directory. Follow the [Micropython Docs](https://docs.micropython.org/en/latest/reference/packages.html#cross-installing-packages) on how to achieve this, substituting `bdsim.micropython` for the package name used in the tutorial.

## Pre-Built Firmware

We (should) provide pre-built versions of micropython with `ulab` and other frozen modules required by `bdsim.micropython` for ports included in the [Official MicroPython Repository](https://github.com/micropython/micropython/tree/master/ports). We (should) provide two versions per supported port; with both minimum required and full `ulab` features/submodules.

## Building Firmware Manually

These commands assume to be run on linux with access to required dependencies. Please see [The MicroPython README for more information](https://github.com/micropython/micropython#external-dependencies).

### For ESP32

```bash
BUILD_DIR=~/bdsim-firmware-build # specify build dir
git clone https://github.com/micropython/micropython $BUILD_DIR/micropython
cd $BUILD_DIR/micropython
git checkout v1.13 # choose micropython version - note v1.12 is incompatible with ulab
git submodule update --init
cd $BUILD_DIR/micropython/mpy-cross && make # build cross-compiler (required)

make ESPIDF= # will display supported ESP-IDF commit hashes
# output should look like: """
# ...
# Supported git hash (v3.3): 9e70825d1e1cbf7988cf36981774300066580ea7
# Supported git hash (v4.0) (experimental): 4c81978a3e2220674a432a588292a4c860eef27b
# """

# choose an esp-idf version
ESPIDF_VER=9e70825d1e1cbf7988cf36981774300066580ea7

# Download and prepare the SDK
git clone https://github.com/espressif/esp-idf.git $BUILD_DIR/esp-idf
cd $BUILD_DIR/esp-idf
git checkout $ESPIDF_VER
git submodule update --init --recursive # get idf submodules
pip install -r ./requirements.txt # install python reqs
```

Next, install the ESP32 compiler. If using an ESP-IDF version >= 4.x (chosen by `$ESPIDF_VER` above), this can be done by running `./install.sh`. Otherwise, (for version 3.x) run:

```bash
# for 64 bit linux
curl https://dl.espressif.com/dl/xtensa-esp32-elf-linux64-1.22.0-80-g6c4433a-5.2.0.tar.gz | tar xvz

# for 32 bit
curl https://dl.espressif.com/dl/xtensa-esp32-elf-linux32-1.22.0-80-g6c4433a-5.2.0.tar.gz | tar xvz

# see https://docs.espressif.com/projects/esp-idf/en/v3.3.2/get-started for more info
```

Next, download `ulab`'s source code and configure required features:

```bash
git clone https://github.com/v923z/micropython-ulab $BUILD_DIR/ulab

# you can look through and enable/disable ulab features by editing $BUILD_DIR/ulab/code/ulab.h
# the default enables all features
```

Finally, build the firmware:

```bash
cd $BUILD_DIR/micropython/ports/esp32
# temporarily add esp32 compiler to path
export PATH=$BUILD_DIR/xtensa-esp32-elf/bin:$PATH
export ESPIDF=$BUILD_DIR/esp-idf # req'd by Makefile
export BOARD=GENERIC # options are dirs in ./boards
export USER_C_MODULES=$BUILD_DIR/ulab

make submodules && make all
```

Plug in your ESP32. Now flash it:

```bash
make erase && make deploy
```
