# Because we want to be able use 'test' in the name of things this
# is used to make what nosetests considers unittest classes/modules/methods
# more narrowly defined
UNIT_TEST_PATTERN = '^Test|^test_|\.test_|\.test\.'


# Defines targets for running tests on a node.
#
# Runs tests in a local virtual Python environment.
#
# $(1) - Name of the node
define TEST

.PHONY: test_$(1)
test_$(1): SHELL := $$(NODE_$(1)_SHELL)
test_$(1): .SHELLFLAGS := $$(NODE_$(1)_SHELLFLAGS)
test_$(1): prepare_node_$(1)
# Fix coverage
	nosetests $$(if $$(filter $$(COVERAGE),y),--with-coverage --cover-package $(ROOT_PACKAGE) --cover-inclusive --cover-erase $$(if $$(filter $$(COVERAGE_XML_REPORT),y),--cover-xml)) $(ROOT_PACKAGE)
	@$$(if $$(filter $$(COVERAGE),y),mv .coverage .coverage-$(1))

test_all: test_$(1)

.PHONY: static_$(1)
static_$(1): SHELL := $(NODE_local_SHELL)
static_$(1): .SHELLFLAGS := $(NODE_local_SHELLFLAGS)
static_$(1): prepare_node_local
	@flake8 $(ROOT_PACKAGE)
	@pydocstyle $(ROOT_PACKAGE) --ignore=D1,D202,D203,D204,D212 --match-dir='^((?!generated|syntaxerror).)*$$$$' --explain
	@yapf --style .yapf --diff $$(FORMAT_SOURCES)
	@isort --multi-line 2 --check-only --dont-skip '__init__.py' --line-width 100 $$(FORMAT_SOURCES)

# For more information about pydocstyle, please see:
# http://www.pydocstyle.org/en/2.1.1/error_codes.html
# https://www.python.org/dev/peps/pep-0257/

static_all: static_$(1)

endef

$(eval $(foreach __node,$(TEST_NODES),$(call TEST,$(__node))))
