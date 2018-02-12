# Znail

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
* Emulate a disconnect (by powering down one of its network interfaces)
* Override answers to DNS queries (by redirecting DNS traffic to its internal DNS server)
* Redirect IP traffic from one host to another
* Not apply any of the above for certain hosts using a whitelist

Znail can be managed in one of two ways, using its web interface or its REST API.

# Development

The Python environment requires that the `pip` and `pipenv` tools are installed.

To set up the development environment on recent Ubuntu systems, run the following commands:

    sudo apt update
    sudo apt install python3-pip
    sudo pip3 install "pipenv==9.0.2"

# License

Copyright Zenterio AB, 2018, 2019

Distributed under the terms of the Apache License 2.0.