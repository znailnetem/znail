# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "debian/buster64"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = 5000
    vb.cpus = 4

    vb.customize ["modifyvm", :id, "--nictype1", "virtio" ]
    vb.customize ["modifyvm", :id, "--nictype2", "virtio" ]
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y coreutils quilt parted qemu-user-static debootstrap zerofree zip dosfstools bsdtar libcap2-bin grep rsync xz-utils file git curl

    cd /root
    git clone --branch 2019-07-10-raspbian-buster https://github.com/RPi-Distro/pi-gen.git

    cd pi-gen

    # What stages to run is configurable using the STAGE_LIST config option.
    # While stage selection does seem to work using this option,
    # copying the rootfs from the previous step seems to break.
    #
    # Fix by removing unused stages:
    rm -rf stage3 stage4 stage5
  SHELL
end
