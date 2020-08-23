
.venv: requirements.txt requirements-dev.txt setup.py
	python3 -m venv .venv
	.venv/bin/pip3 install --upgrade setuptools pip wheel
	.venv/bin/pip3 install -r requirements-dev.txt -r requirements.txt
	.venv/bin/pip3 install -e .

cleanvenv:
	-rm -rf .venv/*
	-rmdir .venv
	rm -rf *.egg-info/


# The BASH_ENV variable tells bash where to find its rc file. If the rc file
# exists, it is sourced by bash on startup.
#
# Lets use this feature to automatically activate the virtual environment.
BASH_ENV := .venv/bin/activate
export BASH_ENV
