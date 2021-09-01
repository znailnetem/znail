# Znail

![Znail Logo](/artwork/znail_x10.png)

Znail is a network emulator inteded to run on a computer with two network interfaces.
Equipped with two network interfaces, Znail acts as a network bridge.
Znail can then control network traffic passing through the bridge.

With a system under test connected to the network through this bridge,
Znail can help you answer question about how that system behaves under various network conditions.

# Features

* Emulate packet delay
* Emulate packet loss
* Emulate packet duplication
* Emulate packet reordering
* Emulate packet corruption
* Control packet rate
* Capture network packets
* Emulate a disconnect (by powering down one of its network interfaces)
* Override answers to DNS queries (by redirecting DNS traffic to its internal DNS server)
* Redirect IP traffic from one host to another
* Not apply any of the above for certain hosts using a whitelist

Znail can be managed in one of two ways, using its web interface or its REST API.

# Getting Started

The easiest way to get started with Znail is to [download](https://github.com/znailnetem/znail/releases/latest) an image with Znail pre-installed.

The image can then be installed on a suitable target system, for example a [Raspberry Pi](https://www.raspberrypi.org/documentation/installation/installing-images/README.md)
or a [NanoPi R2S](https://docs.armbian.com/User-Guide_Getting-Started/#how-to-prepare-a-sd-card).

## Raspberry Pi

The default SSH username for the pre-built image is `pi` and the password is `raspberry`.

## NanoPi R2S

The default SSH username for the pre-built image is `root` and the password is `1234`.

# Generating Custom Images

To set up the environment on an Ubuntu 20.04 system, run the following commands:

    sudo apt update
    sudo apt install -y coreutils quilt parted qemu-user-static debootstrap zerofree zip dosfstools bsdtar libcap2-bin grep rsync xz-utils file git curl

To generate an image:

    make image

The resulting images can be found in the `dist/image` directory.

Generating the different images can take quite some time.
If you are looking to only build one specific kind of image more narrow `make` targets are available.
See `make help` for more information.

# Development

The Python environment requires that the `pip` tool is installed.

To set up the development environment on an Ubuntu 20.04 system, run the following commands:

    sudo apt update
    sudo apt install -y python3-pip python3-venv

To build and activate the virtual Python environment:

    source ./activate

To automatically format the code:

    make format

To run tests and static code analysis:

    make check

More information about what targets the build system provides:

    make help

# Special Thanks

Special thanks to Alice Persson for contributing the Znail logotype.

# License

Distributed under the terms of the Apache License 2.0.
