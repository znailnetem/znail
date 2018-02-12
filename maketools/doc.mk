
.PHONY: doc html pdf
doc:
html:
pdf:

# 1 - directory in doc
define MACRO_DOC_TARGETS
$(eval __$(1)_docs := $(shell find doc/$(1) -type f))
html: $(1)_html
pdf: $(1)_pdf
$(1): $(1)_html $(1)_pdf
doc: $(1)
$(1)_html: doc/build/$(1)/html/index.html
doc/build/$(1)/html/index.html: SHELL := $(NODE_local_SHELL)
doc/build/$(1)/html/index.html: .SHELLFLAGS := $(NODE_local_SHELLFLAGS)
doc/build/$(1)/html/index.html: prepare_node_local $(__$(1)_docs) $(ROOT_PACKAGE)/version.py
	@sphinx-build -E -a -b html doc/$(1) doc/build/$(1)/html
	@touch doc/build/$(1)/index.html
$(1)_pdf: doc/build/$(1)/pdf/$(1).pdf
doc/build/$(1)/pdf/$(1).pdf: SHELL := $(NODE_local_SHELL)
doc/build/$(1)/pdf/$(1).pdf: .SHELLFLAGS := $(NODE_local_SHELLFLAGS)
doc/build/$(1)/pdf/$(1).pdf: prepare_node_local $(__$(1)_docs) $(ROOT_PACKAGE)/version.py
	@sphinx-build -E -a -b latex doc/$(1) doc/build/$(1)/pdf
	@cd doc/build/$(1)/pdf && make all-pdf
ifeq ($(1),user_guide)
doc/build/$(1)/html/index.html:
doc/build/$(1)/pdf/$(1).pdf:

endif

endef

$(eval $(call MACRO_DOC_TARGETS,$(filter-out build plantuml.8057.jar,$(notdir $(wildcard doc/*)))))

.PHONY: cleandoc
cleandoc:
	rm -rf doc/build/
