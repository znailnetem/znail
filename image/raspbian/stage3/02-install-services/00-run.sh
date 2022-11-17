#!/bin/bash -e

install -v -m 644 files/locale "${ROOTFS_DIR}/etc/default/locale"
install -v -m 644 files/modules "${ROOTFS_DIR}/etc/modules"

install -v -m 644 files/znail.service "${ROOTFS_DIR}/etc/systemd/system/"
rm -f "${ROOTFS_DIR}"/etc/systemd/system/multi-user.target.wants/znail.service
ln -s /etc/systemd/system/znail.service "${ROOTFS_DIR}"/etc/systemd/system/multi-user.target.wants/znail.service

install -v -m 644 files/update-network-interfaces.service "${ROOTFS_DIR}/etc/systemd/system/"
rm -f "${ROOTFS_DIR}"/etc/systemd/system/multi-user.target.wants/update-network-interfaces.service
ln -s /etc/systemd/system/update-network-interfaces.service "${ROOTFS_DIR}"/etc/systemd/system/multi-user.target.wants/update-network-interfaces.service

install -v -m 700 files/update-network-interfaces "${ROOTFS_DIR}/usr/local/bin"

rm -f "${ROOTFS_DIR}"/etc/systemd/system/multi-user.target.wants/ssh.service
ln -s /lib/systemd/system/ssh.service "${ROOTFS_DIR}"/etc/systemd/system/multi-user.target.wants/ssh.service

grep -qxF "dtoverlay=pi3-disable-wifi" "${ROOTFS_DIR}/boot/config.txt" || echo "dtoverlay=pi3-disable-wifi" >> "${ROOTFS_DIR}/boot/config.txt"
grep -qxF "dtoverlay=pi3-disable-bt" "${ROOTFS_DIR}/boot/config.txt" || echo "dtoverlay=pi3-disable-bt" >> "${ROOTFS_DIR}/boot/config.txt"
