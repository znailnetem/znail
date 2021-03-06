
.PHONY: help
help:
	@echo
	@echo "Usage make <target> <args> -jN"
	@echo ""
	@echo " Environment:"
	@echo ""
	@echo "  venv             Create virtualenv and install all dependencies"
	@echo "                   Run 'source activate' to enable the environment"
	@echo " Utilities:"
	@echo ""
	@echo "  format           Automatically format all Python source code"
	@echo ""
	@echo " Testing:"
	@echo "  check            Run all tests in the local environment"
	@echo "  test             Run all unit tests"
	@echo "  static           Run static analysis"
	@echo ""
	@echo " Set the COVERAGE variable to 'y' to get a code coverage report."
	@echo " For example: make COVERAGE=y check"
	@echo ""
	@echo " Packaging:"
	@echo ""
	@echo "  pypi             Build PyPi packages"
	@echo "  image            Build a Raspberry Pi image"
	@echo ""
	@echo " Clean:"
	@echo ""
	@echo "  clean            Cleans all temporary files and build output"
	@echo "  cleanup          Cleans all temporary files and build output"
	@echo "                   removes venvs and marks containers for rebuilding"
	@echo "  cleanvenv        Removes all venvs"
	@echo ""
	@echo " If you find that a high level target is taking too long to build,"
	@echo " try using the -j flag to run targets in parallel."
	@echo ""
