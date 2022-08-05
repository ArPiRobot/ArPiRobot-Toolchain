# ArPiRobot-Toolchain

## Prebuilt Toolchain Downloads

See the [Releases Page](https://github.com/ArPiRobot/ArPiRobot-Toolchain/releases). 

Download the correct toolchain for your system. Raspberry Pi's use the `armv6` toolchain. Nvidia Jetson's use the `aarch64` toolchain.

## Setup to Build

**Recommended build system:** Debian buster (use VM, container, or chroot)

**Install crosstool-ng**

The cross compilers are built using [crosstool-ng](https://crosstool-ng.github.io/). 

*From this point forward, run commands in the build environment (chroot, container, vm, etc).*

Download, build and install `crosstool-ng`. Generally, it is best to use the version from the master branch as stable releases sometimes have dead urls.

```sh
sudo apt install git build-essential autoconf bison flex  \
    texinfo help2man gawk libtool libtool-bin git \
    libncurses5-dev wget unzip zip
git clone https://github.com/crosstool-ng/crosstool-ng.git
cd crosstool-ng
cp -r ../samples/* ./samples/
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
ct-ng ./[CONFIG_NAME].config
ct-ng menuconfig
```

Change some settings

- Paths and misc options:
    - Disable Render toolchain read-only
- Binary Utilities
    - Change version to match ones listed above
- C-library
    - Change glibc version to match ones listed above
- C compiler
    - Change glibc version to match ones listed above

Once done, save the configuration (default filename `.config`) and exit.

Build the toolchain.

```sh
ct-ng build.12    # Number is passed to make -j
```

Create archive with toolchain

```sh
pushd ~/x-tools/
rm $CONFIG/build.log.bz2
rm -r $CONFIG/$CONFIG/debug-root/
cd $CONFIG
tar -czvf ../$CONFIG_Linux_x64.tar.gz $CONFIG/
popd
cp ~/x-tools/$CONFIG_Linux_x64.tar.gz .
```

## Build Toolchain for Windows x86_64 Host

Install mingw-w64 package. This provides a cross compiler to generate binaries for 64-bit windows on a 64-bit linux system.

```sh
sudo apt install mingw-w64
```

Configure crosstool-ng using sample configuration as a base.

```sh
ct-ng ./[CONFIG_NAME].config
ct-ng menuconfig
```

Change some settings
- Paths and misc options:
    - Disable Render toolchain read-only
- Toolchain Options:
    - Toolchain type: Type = Canadian
    - Build System:
        - Tuple = x86_64-unknown-linux-gnu
    - Host System:
        - Tuple = x86_64-w64-mingw32
        - Tools prefix = x86_64-w64-mingw32-
- Binary Utilities
    - Change version to match ones listed above
- C-library
    - Change glibc version to match ones listed above
- C compiler
    - Change glibc version to match ones listed above

Once done, save the configuration (default filename `.config`) and exit.

```sh
ct-ng build.12    # Number is passed to make -j
```

Create archive with toolchain

```sh
pushd ~/x-tools/
rm $CONFIG/build.log.bz2
rm -r $CONFIG/$CONFIG/debug-root/
cd $CONFIG
tar -czvf ../$CONFIG_Windows_x64.tar.gz $CONFIG/
popd
cp ~/x-tools/$CONFIG_Windows_x64.tar.gz .
```


## Build Toolchain for macOS x86_64 Host

Build osxcross as a cross compiler targeting macOS (x86_64)
- Build [osxcross](https://github.com/tpoechtrager/osxcross) following the project's instructions
- Make sure to also build gcc. Build the same version of gcc as the system you are building on uses natively (`gcc --version`).
- You also need to build binutils (`BINUTILS_VERSION=2.32.1 ./build_binutils`). Once again, best to make the version the same as the version uses on the build system
- Tested using macOS 10.15 SDK targeting darwin 19. Minimum targeted version of macOS = 10.9

Add osxcross executables to the path

```sh
export PATH=$PATH:$HOME/osxcross-buster/target/bin:$HOME/osxcross-buster/target/binutils/bin

# Or, if using the schroot method, add the following to ~/.bashrc
if [ "$SCHROOT_ALIAS_NAME" == "buster" ]; then
    export PATH=$PATH:~/osxcross-buster/target/bin:$HOME/osxcross-buster/target/binutils/bin
fi
```

Configure crosstool-ng using sample configuration as a base.

```sh
ct-ng ./[CONFIG_NAME].config
ct-ng menuconfig
```

Change some settings
- Paths and misc options:
    - Disable Render toolchain read-only
- Toolchain Options:
    - Toolchain type: Type = Canadian
    - Build System:
        - Tuple = x86_64-unknown-linux-gnu
    - Host System:
        - Tuple = x86_64-apple-darwin19 (output of `o64-gcc -dumpmachine`)
        - Tools prefix = x86_64-apple-darwin19- (same as above, but with hyphen at the end)
- Binary Utilities
    - Change version to match ones listed above
- C-library
    - Change glibc version to match ones listed above
- C compiler
    - Change glibc version to match ones listed above

Once done, save the configuration (default filename `.config`) and exit.

```sh
ct-ng build.12    # Number is passed to make -j
```


Create archive with toolchain

```sh
pushd ~/x-tools/
rm $CONFIG/build.log.bz2
rm -r $CONFIG/$CONFIG/debug-root/
cd $CONFIG
tar -czvf ../$CONFIG_Windows_x64.tar.gz $CONFIG/
popd
cp ~/x-tools/$CONFIG_Windows_x64.tar.gz .
```


## Making Archives Installable w/ Deploy Tool

Add a file `what.txt` to the archive root with the content `toolchain/config` where `config` is the name of the config used to build the toolchain.

