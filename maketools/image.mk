
#image: vagrant pypi
#	mkdir -p dist/image
#	vagrant rsync
#	vagrant ssh -c "sudo /bin/bash -c 'cp -r /vagrant/image/* /root/pi-gen'"
#	vagrant ssh -c "sudo /bin/bash -c 'cd /root/pi-gen && ./build.sh'"
#	vagrant ssh -c "sudo /bin/bash -c \"cp -r /root/pi-gen/deploy /vagrant/deploy && chown vagrant:vagrant -R /vagrant/deploy/\""
#	vagrant scp 'default:/vagrant/deploy/*.info' dist/image
#	vagrant scp 'default:/vagrant/deploy/*.zip' dist/image


build/pi-gen:
	mkdir -p build
	cd build && git clone --branch 2020-02-13-raspbian-buster https://github.com/RPi-Distro/pi-gen.git

image: pypi build/pi-gen
	mkdir -p dist/image
	rm -rf build/pi-gen/stage3 build/pi-gen/stage4 build/pi-gen/stage5
	cp -r image/* build/pi-gen/
	cd build/pi-gen && sudo ./build.sh
