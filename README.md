# Znail

![Znail Logo](/artwork/znail_x10.png)

Znail is a network emulator inteded to run on a Raspberry Pi.
Equipped with two network interfaces, the Raspberry Pi acts as a network bridge.
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

The easiest way to get started with Znail is to [download](https://github.com/znailnetem/znail/releases/latest) a Rasbian image with Znail pre-installed.

The image can then be [installed](https://www.raspberrypi.org/documentation/installation/installing-images/README.md) on a Raspberry Pi.

# Generating a Custom Image

A virtual machine is used to build the image.
`Vagrant` and the `vagrant-scp` plugin is required.

To set up the environment on recent Ubuntu systems, run the following commands:

    sudo apt update
    sudo apt install vagrant
    vagrant plugin install vagrant-scp

To generate an image:

    make image

The resulting image can be found in the `dist/image` directory.

# Development

The Python environment requires that the `pip` tool is installed.

To set up the development environment on recent Ubuntu systems, run the following commands:

    sudo apt update
    sudo apt install python3-pip python3-venv

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
