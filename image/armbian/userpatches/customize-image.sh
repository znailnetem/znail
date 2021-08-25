#!/bin/bash

# arguments: $RELEASE $LINUXFAMILY $BOARD $BUILD_DESKTOP
#
# This is the image customization script

# NOTE: It is copied to /tmp directory inside the image
# and executed there inside chroot environment
# so don't reference any files that are not already installed

# NOTE: If you want to transfer files between chroot and host
# userpatches/overlay directory on host is bind-mounted to /tmp/overlay in chroot
# The sd card's root path is accessible via $SDCARD variable.

RELEASE=$1
LINUXFAMILY=$2
BOARD=$3
BUILD_DESKTOP=$4
OVERLAY="/tmp/overlay"

EnableKernelModules() {
	echo "sch_netem" >> /etc/modules
	echo "br_netfilter" >> /etc/modules
}

ConfigureNetwork() {
	install -v -m 700 "${OVERLAY}/update-network-interfaces" "/usr/local/bin"
	install -v -m 644 "${OVERLAY}/update-network-interfaces.service" "/etc/systemd/system/"
	rm -f "/etc/systemd/system/multi-user.target.wants/update-network-interfaces.service"
	ln -s "/etc/systemd/system/update-network-interfaces.service" "/etc/systemd/system/multi-user.target.wants/update-network-interfaces.service"
	# nanopi-r2s board support installs a udev rule to rename eth1 -> lan0.
	# We don't need that.
	rm -f "/etc/udev/rules.d/70-rename-lan.rules"
}

FixupHaveged() {
	# https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=866306
	sed -i -e 's/DAEMON_ARGS="\?\([^"]*\)"\?/DAEMON_ARGS="\1 -d 16"/g' "/etc/default/haveged"
}

InstallZnail() {
	install -d "/opt/znail"
	install -v -m 600 "${OVERLAY}/requirements.txt" "/opt/znail/requirements.txt"
	install -v -m 600 -D -t "/opt/znail" "${OVERLAY}"/*.whl
	pushd "/opt/znail"
	python3 -m venv venv
	source "venv/bin/activate"
	pip3 install wheel
	pip3 install -r requirements.txt
	pip3 install *.whl
	popd
	install -v -m 644 "${OVERLAY}/znail.service" "/etc/systemd/system/"
	rm -f "/etc/systemd/system/multi-user.target.wants/znail.service"
	ln -s "/etc/systemd/system/znail.service" "/etc/systemd/system/multi-user.target.wants/znail.service"
	rm -f "/usr/local/bin/hub-ctrl"
	install -v -m 775 "${OVERLAY}/hub-ctrl" "/usr/local/bin/hub-ctrl"
}

EnableKernelModules "$@"
ConfigureNetwork "$@"
FixupHaveged "$@"
InstallZnail "$@"
