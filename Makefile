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

##################################################################
##################################################################

include maketools/environment.mk
include maketools/help.mk
include maketools/doc.mk
include maketools/pypi.mk
include maketools/test.mk
include maketools/version.mk
include maketools/image.mk

test: test_local
static: static_local

.PHONY: check
check: SHELL := $(NODE_local_SHELL)
check: .SHELLFLAGS := $(NODE_local_SHELLFLAGS)
check: prepare_node_local static test
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
run: SHELL := $(NODE_local_SHELL)
run:
	SHUTDOWN_COMMAND=echo IPTABLES_COMMAND=echo TC_COMMAND=echo HUB_CTRL_COMMAND=echo SYSTEMCTL_COMMAND=echo HOSTS_FILE=/dev/null znail -p 8080 -d

venv: prepare_node_local

.PHONY: format
format: SHELL := $(NODE_local_SHELL)
format: .SHELLFLAGS := $(NODE_local_SHELLFLAGS)
format: prepare_node_local
	@yapf --style .yapf --in-place --parallel $(FORMAT_SOURCES)
	@isort -j8 --multi-line 2 --apply --dont-skip '__init__.py' --line-width 100 $(FORMAT_SOURCES)

.PHONY: clean
clean: cleandoc cleanimage
	rm -rf build/
	rm -rf dist/
	rm -f $(ROOT_PACKAGE)/version.py
	rm -f .benchmark

.PHONY: cleanup
cleanup: clean cleanvenv cleannodes
	rm -rf .venv
