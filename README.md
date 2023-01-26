# ArPiRobot-Toolchain


## Prebuilt Toolchain Downloads

See the [Releases Page](https://github.com/ArPiRobot/ArPiRobot-Toolchain/releases). 


## Build Setup

It is **highly** recommended to build on an older Linux system (older glibc) so the Linux native compiler will be able to run on most modernish Linux distributions. At time of writing, it is recommended to build on Ubuntu 18.04 (bionic). This can be done with a chroot environment, container, or virtual machine.

### Schroot Setup (on a more recent x64 Ubuntu system)

```sh
sudo apt install debootstrap schroot
sudo debootstrap --arch=amd64 bionic bionic/
```

Then add the following to `/etc/schroot/chroot.d/bionic.conf`. Change USERNAME as needed.

```
[bionic]
description=Ubuntu 18.04 (bionic)
type=directory
directory=/srv/chroot/bionic
users=marcus
root-groups=root
profile=desktop
personality=linux
```

On more recent Ubuntu / debian systems, `yescrypt` is used, but this is not supported in older systems (bionic included). Thus change `/etc/pam.d/common-password` by modifying `yescrypt` to be `sha512`. Failing to do so will prevent `sudo` from working in the chroot environment.


### Install crosstool-ng

*In the build environment (chroot, vm, container, etc)*

```sh
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo add-apt-repository multiverse
sudo apt install git build-essential autoconf bison flex  \
    texinfo help2man gawk libtool libtool-bin git \
    libncurses5-dev wget unzip zip
wget https://github.com/crosstool-ng/crosstool-ng/releases/download/crosstool-ng-1.24.0/crosstool-ng-1.24.0.tar.bz2
tar --extract --bzip2 -f crosstool-ng-1.24.0.tar.bz2
cd crosstool-ng-1.24.0
./bootstrap
./configure --prefix=/usr/local
make -j
sudo make install
```


### Required to Build for Linux x64 Host

*In the build environment (chroot, vm, container, etc)*

```sh
sudo apt install build-essential
```

### Required to Build for Windows x64 Host

*In the build environment (chroot, vm, container, etc)*

```sh
sudo apt install mingw-w64
```

### Required to Build for macOS x64 Host

*In the build environment (chroot, vm, container, etc)*

Requires [osxcross](https://github.com/tpoechtrager/osxcross). Download the macOS SDK following the project's instructions (tested with SDK 11.1). Then run the following. *Note: It is recommended to clone to ~/osxcross-bionic since this is the build used for the bionic chroot*.

```sh
# Install build dependencies
apt install clang llvm llvm-dev cmake git patch python3 libssl-dev lzma-dev libxml2-dev libgmp-dev libmpfr-dev libmpc-dev

# Build osxcross
./build.sh

# Build gcc and binutils targeting macos
# Generally, it is best to build the same versions of these components 
# as are used on the build system (in this case Ubuntu bionic).
GCC_VERSION=7.3.0 ./build_gcc.sh
BINUTILS_VERSION=2.30 ./build_binutils.sh


# Add osxcross to path (add the following to either bashrc or profile)
# Change $HOME/osxcross-bionic to whatever path you cloned osxcross to
if [ "$SCHROOT_ALIAS_NAME" = "bionic" ]; then
    PATH=$PATH:$HOME/osxcross-bionic/target/bin/:$HOME/osxcross-bionic/target/binutils/bin
fi
```


## Building

In the build environment run the following and follow the script's directions / prompts

```sh
sudo apt install python3
./build.py
```
