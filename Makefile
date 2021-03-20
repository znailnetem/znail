VERSION_NUMBER := 0.6.0
ROOT_PACKAGE := znail

ifdef BUILD_NUMBER
	VERSION_STRING := ${VERSION_NUMBER}+${BUILD_NUMBER}
endif

ifndef BUILD_NUMBER
	VERSION_STRING := ${VERSION_NUMBER}
endif

PYTHON := python3
PY_SOURCES := $(shell find $(ROOT_PACKAGE) -type f -name '*.py')
FORMAT_SOURCES := $(shell find $(ROOT_PACKAGE) -name '*.py' -not -path '*__pycache__*')
OUTPUT_DIR=output

_first: help

include maketools/environment.mk
include maketools/help.mk
include maketools/pypi.mk
include maketools/test.mk
include maketools/version.mk
include maketools/image.mk


.PHONY: check
check: venv static test
ifeq ($(filter $(COVERAGE),y),y)
	@echo
	@echo Combined coverage for unit and system tests
	@cp .coverage-local .coverage-local-copy
	COVERAGE_FILE=.coverage-all coverage combine .coverage-local-copy
	COVERAGE_FILE=.coverage-all coverage report -m --rcfile=.coveragerc
  ifeq ($(filter $(COVERAGE_XML_REPORT),y),y)
	COVERAGE_FILE=.coverage-all coverage xml -o coverage-all.xml --rcfile=.coveragerc
  endif
endif

.PHONY: package
package: check doc

run: venv
run:
	SHUTDOWN_COMMAND=echo IPTABLES_COMMAND=echo TC_COMMAND=echo HUB_CTRL_COMMAND=echo SYSTEMCTL_COMMAND=echo HOSTS_FILE=/dev/null znail -p 8080 -d

venv: .venv

.PHONY: format
format:
	@black -l120 $(FORMAT_SOURCES)

.PHONY: clean
clean: cleanimage
	rm -rf build/
	rm -f $(ROOT_PACKAGE)/version.py
	rm -f .benchmark

.PHONY: cleanup
cleanup: clean cleanvenv
	rm -rf dist/
