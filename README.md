# ArPiRobot-Toolchain

## Prebuilt Toolchain Downloads

See the [Releases Page](./releases). 

Each toolchain is built with the intent of being used with a specific version of the Raspberry Pi OS. This version is not dependent on specific releases, but on the debian version on which it is based (eg. Stretch, Buster, Bullseye). Each toolchain is built with the same version of glibc, binutils, and a similar version of gcc to what is used in the targeted version of Raspberry Pi OS.

All prebuilt toolchains are compatible with all Raspberry Pi's (at time of writing), meaning they target the `armv6` architecture. This is necessary for compatability with the Pi Zero W. Code generated targeting `armv6` should also work on newer Pi's (meaning the prebuilt toolchains can be used with a Pi Zero W, Pi 3A+, Pi 4, etc).

## Target System(s)

The target system is the system the toolchain generates code for.

The toolchains are built to target the Raspberry Pi(s), or more generally, an Arm Linux system. The specifics of each toolchain depend on which version of the Pi they are intended to work with. Using a toolchain built specifically for the version of the Pi you are using will result in the best performance, however by targeting an older architecture, the same toolchain can be used with more Pis.

There are two types of toolchains that can be built: 32-bit (`armv#`) and 64-bit (`aarch64`). As the ArPiRobot images are 32-bit images, the 64-bit toolchains are not generally useful.

| Raspberry Pi           | Architecture(s)     | CPU              |
| ---------------------- | ------------------- | ---------------- |
| Pi 1B & 1B+ & 1A+      | armv6 w/ FPU        | ARM1176JZFS      |
| Pi 2B                  | armv7               | Cortex-A7        |
| Pi 3B & 3B+ & 3A+      | armv8 / aarch64     | Cortex-A53       |
| Pi 4B                  | armv8 / aarch64     | Cortex-A72       |
| Pi Zero & Zero W       | armv6 w/ FPU        | ARM1176JZFS      |
| Pi Zero 2 W            | armv8 / aarch64     | Cortex-A53       |


## Host Systems

The host system is the system that the toolchain runs on.

Three different toolchains are often built (each with diffent hosts).

- One to use on 64-bit Linux systems (host = `x86_64-unknown-linux-gnu` or `x86_64-pc-linux-gnu`)
- One to use on 64-bit Windows systems (host = `x86_64-w64-mingw32` if using MinGW not Cygwin or MSYS2)
- One to use on 64-bit macOS systems (host = `x86_64-apple-darwin#.#.#` ???)

## Build System

The build system is the system that is building the toolchain. Often this will be the same as the host system, but it does not have to be.

The toolchains are built on a Linux system (x86_64). When building a cross compiler toolchain, the binutils version and glibc version should be the same as that of the targeted system. This often means that to build the cross compiler toolchain, it is necessary to build older versions of `binutils` and `glibc` (and `gcc`). Sometimes, newer versions of `gcc` will not build older versions of `binutils` or `glibc` without some changes to compilation flags. These changes are often difficult to determine. As such, it is best to use a build system (Linux system on which you are doing the build) that has a version of `gcc`, `glibc`, and `binutils` similar to the ones used on the target. Since Raspberry Pi OS is debian based, it is often easiest to use the same version of debian to build the cross toolchain as the target system. 

For example, to build a cross compiler for Raspberry Pi OS Buster (glibc 2.28, binutils 2.31.1, gcc 8.3.0) it is best to use Debian Buster to build the toolchains (debian buster has the same glibc, binutils, and gcc versions).

In contrast, if attempting to build the cross toolchain for Raspberry Pi OS buster on Ubuntu 20.04 (gcc 9.3.0) issues are encountered building `binutils` 2.31.1 due to a change in `gcc`.

This does not mean you have to fully install a specific version of Debian just for building the toolchain. You can use a container, virtual machine, or chroot environment. A chroot environment is easy to setup using `debootstrap` and `schroot` (on debian based systems, `sudo apt install schroot debootstrap`).

Append to `/etc/schroot/schroot.conf`
```
[buster]
description=Debian 10
type=directory
directory=/srv/chroot/buster
users=marcus
groups=root
root-groups=root
```

Then run
```sh
sudo mkdir -p /srv/chroot/buster
debootstrap --arch amd64 buster /srv/chroot/buster http://deb.debian.org/debian/

sudo schroot -c buster
apt install sudo
exit
schroot -c buster
# You will be in a debian buster chroot environment with access to your home directory. Type exit to exit.
```

## Crosstool-ng

The cross compilers are built using [crosstool-ng](). Crosstool-ng provides several sample configurations, including ones for each version of the Pi. These are used as a base configuration for the toolchain that will be built.

Base configurations (from samples, `ct-ng list-samples`)

- `armv6-unknown-linux-gnueabihf`  for supporting Pi 1 and Zero / Zero W and newer (there is also a `armv6-unknown-linux-gnueabi` version with hardware floating point operations disabled). Despite the name, the config file uses `rpi` instead of `unknown`
- `armv7-pi2-linux-gnueabihf` for supporting Pi 2 and newer
- `armv8-pi3-linux-gnueabihf` for supporting Pi 3 and newer (32-bit)
- `armv8-pi4-linux-gnueabihf` for supporting Pi 4 and newer (32-bit)
- `aarch64-pi3-linux-gnueabihf` for supporting Pi 3 and newer (64-bit)
- `aarch64-pi4-linux-gnueabihf` for supporting Pi 4 and newer (64-bit)

## Build Requirements


## Setup to Build toolchains

*From this point forward, run commands in the build environment (chroot, container, vm, etc).*

Download, build and install `crosstool-ng`. Generally, it is best to use the version from the master branch. The latest stable release (`1.24.0`) at time of writing uses dead urls to download required components. This process was tested on December 17, 2021 using crosstool-ng commit `584e57e888fd652ff6228c1dbdff18556149c7cb`.

```sh
sudo apt install git build-essential autoconf bison flex  \
    texinfo help2man gawk libtool libtool-bin git \
    libncurses5-dev wget unzip
git clone https://github.com/crosstool-ng/crosstool-ng.git
cd crosstool-ng
./bootstrap
./configure --prefix=/usr/local
make -j
sudo make install
```

Make sure `ct-ng` works

```sh
ct-ng list-samples
```

## Build Toolchain for Linux x86_64 Host

Configure crosstool-ng using sample configuration as a base.

```sh
mkdir ~/rpi_crossbuild
cd ~/rpi_crossbuild
ct-ng [base_config_name]
ct-ng menuconfig
```

Change some settings
- Paths and misc options:
    - Disable Render toolchain read-only
- Target Options:
    - ~~Floating point = hardware (FPU)~~ This should be done by default if using the `hf` version of the sample configs
- Operating System
    - Change kernel version to match the minimum kernel version used in the targeted raspios version (or something lower)
- Binary Utilities
    - Change version to match version used on target raspios verison (`ld -version`)
- C-library
    - Change glibc version to match version used on target raspios version (`ldd --version`)
- C compiler
    - Generally, the version of gcc does not matter, however it is usually kept to be the same major version as what is provided as the native compiler for the raspios version targeted (`gcc --version`). You can usually build newer versions of gcc, but it is more likely to run into issues.

Once done, save the configuration (default filename `.config`) and exit.

Build the toolchain. On a laptop with an i5-8250U, 16BG RAM, SATA SSD this took approximately 30 minutes.

```sh
ct-ng build.12    # Number is passed to make -j
```

## Build Toolchain for Windows x86_64 Host

Install mingw-w64 package. This provides a cross compiler to generate binaries for 64-bit windows on a 64-bit linux system.

```sh
sudo apt install mingw-w64
```

Configure crosstool-ng using sample configuration as a base.

```sh
mkdir ~/rpi_crossbuild
cd ~/rpi_crossbuild
ct-ng [base_config_name]
ct-ng menuconfig
```

Change some settings
- Paths and misc options:
    - Disable Render toolchain read-only
- Target Options:
    - ~~Floating point = hardware (FPU)~~ This should be done by default if using the `hf` version of the sample configs
- Toolchain Options:
    - Toolchain type: Type = Canadian
    - Build System:
        - Tuple = x86_64-unknown-linux-gnu
    - Host System:
        - Tuple = x86_64-w64-mingw32
        - Tools prefix = x86_64-w64-mingw32-
- Operating System
    - Change kernel version to match the minimum kernel version used in the targeted raspios version. For example, raspios buster could have a kernel as old as 4.19 (though usually has a newer kernel). Regardless, 4.19 is used. Targeting older kernels is also acceptable.
- Binary Utilities
    - Change version to match version used on target raspios verison (`ld -version`)
- C-library
    - Change glibc version to match version used on target raspios version (`ldd --version`)
- C compiler
    - Generally, the version of gcc does not matter, however it is usually kept to be the same major version as what is provided as the native compiler for the raspios version targeted (`gcc --version`). You can usually build newer versions of gcc, but it is more likely to run into issues.

Once done, save the configuration (default filename `.config`) and exit.

Build the toolchain. On a laptop with an i5-8250U, 16BG RAM, SATA SSD this took approximately 60 minutes.

```sh
ct-ng build.12    # Number is passed to make -j
```


## Build Toolchain for macOS x86_64 Host

TODO: Can this be done using osxcross?
