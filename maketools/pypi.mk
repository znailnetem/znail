pypi: bdist sdist

bdist:
	python3 setup.py bdist_wheel

sdist:
	python3 setup.py sdist

package: pypi