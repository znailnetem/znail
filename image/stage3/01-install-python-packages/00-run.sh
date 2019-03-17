#!/bin/bash -e

install -d /opt/znail
install -v -m 600 /vagrant/requirements.txt "${ROOTFS_DIR}/opt/znail/requirements.txt"
install -v -m 600 /vagrant/dist/pypi/*.whl "${ROOTFS_DIR}/opt/znail"

ln -s /opt/znail/venv/lib/python3.5/site-packages/znail/netem/data/hub-ctrl "${ROOTFS_DIR}"/usr/local/bin/hub-ctrl

on_chroot << EOF
pushd /opt/znail
source venv/bin/activate
pip3 install -r requirements.txt
pip3 install *.whl
popd
EOF
