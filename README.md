# ArPiRobot-Toolchain

Scripts and tools used to build C / C++ cross compiler toolchains for the raspberry Pi used with ArPiRobot robots.

## Target Systems

Note: armv6, armv7, armv8 are 32-bit arm. aarch64 is 64-bit arm. Newer systems are backwards compatible with older architectures. For example, a Pi 3 (armv8 / aarch64) can run a program built for a Pi zero (armv6), however a Pi zero (armv6) cannot run a program built for a Pi 3 (armv8 / aarch64).

| Architecture    | Raspberry PI's                                             |
| --------------- | ---------------------------------------------------------- |
| armv6           | Pi 1B, Pi 1A, Pi Zero, Pi Zero W                           |
| armv7           | Pi 2                                                       |
| armv8 / aarch64 | Pi 3B, Pi 3B+, Pi 3A+, Pi 4B, Pi Zero 2 W                  |

crosstool-ng has sample configurations for various versions of the Pi. The prebuilt toolchains here are compatible with the Pi zero, therefore are armv6.

## Requirements
- Linux (x86_64)
- Native (x86_64 linux) compiler (gcc)
    - Install from distribution packages
- Crosstool-ng
    - Last tested using commit `584e57e888fd652ff6228c1dbdff18556149c7cb`. Tested on Dec 17, 2021
    ```sh
    git clone https://github.com/crosstool-ng/crosstool-ng
    cd crosstool-ng

    # Could checkout a specific tag for stable release
    # However, often urls are updated in master branch when things move locations
    # As such, often using master is necessary

    # Install deps (change if not debian based distro)
    sudo apt install build-essential autoconf bison flex texinfo help2man gawk libtool libtool-bin libtool-doc libncurses5-dev

    ./bootstrap
    ./configure --prefix=/usr/local

    # Install any dependencies that the configure script needs

    make -j
    sudo make install
    ```

## Building for Linux x86_64 Host
 
- Load sample configuration. Change `armv6-rpi-linux-gnueabi` to something else if desired.

```sh
mkdir ~/rpi_cross_build
cd ~/rpi_cross_build
ct-ng armv6-unknown-linux-gnueabi
ct-ng menuconfig
```

- In the `C Compiler` section select the same version of gcc as the raspios version you are targeting uses (`gcc --version`). This can just be something close. It doesn't need to be the exact same version. It can actually be a much newer version. Just make sure the version of gcc you are using is compatible with the glibc version you need.

- In the `C Library` section select the same version of glibc as the raspios version you are targeting uses (`ldd --version`)

- In the `Binary Utilities` section select the same version of binutils as the image you are targeting (`ld -v`)

- In the `Operating System` section select the same version of linux (kernel) as the raspios version you are targeting uses. Select the minimum kernel version (for example, for buster use 4.19). Table on wikipedia is helpful [https://en.wikipedia.org/wiki/Raspberry_Pi_OS#Release_history](https://en.wikipedia.org/wiki/Raspberry_Pi_OS#Release_history)

- In the `Paths and misc options` section make sure download tool is set to either wget or curl (not none) and make sure forbid downloads is disabled.

- In the `Paths and misc options` disable "render the toolchain readonly"

- In `Paths and misc options` add the following build compiler flags `-Wno-error=missing-attributes`

- Save the configuration and exit.

- Start the build. This will take a little while.

```
ct-ng build
```

## Building for Windows x86_64 Host (using mingw-w64)

TODO

## Building for OSX x86_64 Host (using osxcross)

TODO


## Withoug crosstool-ng???

[https://preshing.com/20141119/how-to-build-a-gcc-cross-compiler/](https://preshing.com/20141119/how-to-build-a-gcc-cross-compiler/)

[http://www.ifp.illinois.edu/~nakazato/tips/xgcc.html](http://www.ifp.illinois.edu/~nakazato/tips/xgcc.html)

This method is not tested / used. This is just here in case of issues in the future that prevent using crosstool-ng.
