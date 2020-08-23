# Because we want to be able use 'test' in the name of things this
# is used to make what nosetests considers unittest classes/modules/methods
# more narrowly defined
UNIT_TEST_PATTERN = '^Test|^test_|\.test_|\.test\.'


test:
	nosetests $(if $(filter $(COVERAGE),y),--with-coverage --cover-package $(ROOT_PACKAGE) --cover-inclusive --cover-erase $(if $(filter $(COVERAGE_XML_REPORT),y),--cover-xml)) $(ROOT_PACKAGE)
	@$(if $(filter $(COVERAGE),y),mv .coverage .coverage-$(1))


.PHONY: static
static:
	@flake8 $(ROOT_PACKAGE)
	@pydocstyle $(ROOT_PACKAGE) --ignore=D1,D202,D203,D204,D212 --explain
	@yapf --style .yapf --diff $(FORMAT_SOURCES)
	@isort --multi-line 2 --check-only --dont-skip '__init__.py' --line-width 100 $(FORMAT_SOURCES)
