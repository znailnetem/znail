
build/pi-gen:
	mkdir -p build
	cd build && git clone --branch 2020-02-13-raspbian-buster https://github.com/RPi-Distro/pi-gen.git

image: pypi build/pi-gen
	mkdir -p dist/image
	rm -rf build/pi-gen/stage3 build/pi-gen/stage4 build/pi-gen/stage5
	cp -r image/* build/pi-gen/
	cd build/pi-gen && sudo ./build.sh
