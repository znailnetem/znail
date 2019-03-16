vagrant:
	vagrant up

image: vagrant pypi
	mkdir -p dist/image
	vagrant rsync
	vagrant ssh -c "sudo /bin/bash -c 'cp -r /vagrant/image/* /root/pi-gen'"
	vagrant ssh -c "sudo /bin/bash -c 'cd /root/pi-gen && ./build.sh'"
	vagrant ssh -c "sudo /bin/bash -c \"cp -r /root/pi-gen/deploy /vagrant/deploy && chown vagrant:vagrant -R /vagrant/deploy/\""
	vagrant scp 'default:/vagrant/deploy/*.info' dist/image
	vagrant scp 'default:/vagrant/deploy/*.zip' dist/image

cleanimage:
	vagrant destroy -f
