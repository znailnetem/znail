#!/bin/bash -e

install -v -m 600 /vagrant/requirements.txt "${ROOTFS_DIR}/root/requirements.txt"
install -v -m 600 /vagrant/dist/pypi/*.whl "${ROOTFS_DIR}/root/"

on_chroot << EOF
pip3 uninstall --yes znail || true
pip3 install -r /root/requirements.txt
pip3 install /root/*.whl
rm -f /root/requirements.txt /root/*.whl
EOF
