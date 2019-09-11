pypi: bdist sdist

dist_pypi_directory:
	mkdir -p dist/pypi

bdist: dist_pypi_directory znail/version.py
	python3 setup.py bdist_wheel
	mv dist/*.whl dist/pypi

sdist: dist_pypi_directory znail/version.py
	python3 setup.py sdist
	mv dist/*.tar.gz dist/pypi

package: pypi
