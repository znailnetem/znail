image_local := dummy


# Defines targets required to create a node.
#
# A node is some target that can be used to run shell commands, for example the
# local host system or a Docker container.
#
# $(1) - Name of the node
# $(2) - Path to the executable used to build the node
# $(3) - Path to the executable used to execute commands on the node
define NODE

NODE_$(1)_SHELL := $(3)
NODE_$(1)_SHELLFLAGS := $(DOCKER_REGISTRY)/$(image_$(1)) latest

./docker/markers/docker_node_$(1)_built.marker: SHELL := $(2)
./docker/markers/docker_node_$(1)_built.marker: .SHELLFLAGS := $(DOCKER_REGISTRY)/$(image_$(1)) latest $(image_$(1))
./docker/markers/docker_node_$(1)_built.marker: $(wildcard docker/Dockerfile.$(1))
	@./docker/markers/docker_node_$(1)_built.marker

build_nodes: ./docker/markers/docker_node_$(1)_built.marker

cleannode_$(1):
	rm -f ./docker/markers/docker_node_$(1)_built.marker

cleannodes: cleannode_$(1)

endef


# Defines targets required to prepare a node for use.
#
# $(1) - Name of the node
define TEST_NODE

./docker/markers/docker_node_$(1)_venv.marker: SHELL := $$(NODE_$(1)_SHELL)
./docker/markers/docker_node_$(1)_venv.marker: .SHELLFLAGS := $$(NODE_$(1)_SHELLFLAGS)
./docker/markers/docker_node_$(1)_venv.marker: ./docker/markers/docker_node_$(1)_built.marker requirements.txt requirements-dev.txt setup.py
	python3 -m venv .venv
	pip3 install --upgrade setuptools pip wheel
	pip3 install -r requirements-dev.txt -r requirements.txt
	pip3 install -e .
	touch $$@

prepare_node_$(1): ./docker/markers/docker_node_$(1)_venv.marker
prepare_nodes: prepare_node_$(1)

cleanvenv_$(1): SHELL := $$(NODE_$(1)_SHELL)
cleanvenv_$(1): .SHELLFLAGS := $$(NODE_$(1)_SHELLFLAGS)
cleanvenv_$(1):
	-rm -rf .venv/*
	-rmdir .venv
	rm -rf *.egg-info/
	rm -f ./docker/markers/docker_node_$(1)_venv.marker

cleanvenv: cleanvenv_$(1)

endef


# The BASH_ENV variable tells bash where to find its rc file. If the rc file
# exists, it is sourced by bash on startup.
#
# Lets use this feature to automatically activate the virtual environment.
BASH_ENV := .venv/bin/activate
export BASH_ENV


LOCAL_BUILD := ./maketools/local/build.sh
LOCAL_RUN := ./maketools/local/run.sh
LOCAL_TEST_NODES := local

TEST_NODES := $(LOCAL_TEST_NODES)


$(eval $(foreach __node,$(LOCAL_TEST_NODES),$(call NODE,$(__node),$(LOCAL_BUILD),$(LOCAL_RUN))))
$(eval $(foreach __node,$(LOCAL_TEST_NODES),$(call TEST_NODE,$(__node))))

$(eval $(foreach __node,$(DOCKER_BUILD_NODES),$(call NODE,$(__node),$(DOCKER_BUILD),$(DOCKER_RUN))))
$(eval $(foreach __node,$(DOCKER_TEST_NODES),$(call NODE,$(__node),$(DOCKER_BUILD),$(DOCKER_RUN))))
$(eval $(foreach __node,$(DOCKER_TEST_NODES),$(call TEST_NODE,$(__node))))
$(eval $(foreach __node,$(DOCKER_NODES), $(call DOCKER_DEBUG,$(__node))))
