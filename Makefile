PATH := $(HOME)/.local/bin:$(PATH)

PYTHON_VERSION ?= 3.12
SHELL := /bin/bash

UV ?= uv
UV_RUN ?= uv run
UV_PYTHON_PREFERENCE ?= only-managed
RUN ?= $(UV_RUN)


REQUIRED_UV_VERSION ?= 0.7.3
bootstrap:
	@INSTALLED_UV_VERSION=$$(uv --version 2>/dev/null | awk '{print $$2}' || echo "0.0.0"); \
    DETECTED_UV_VERSION=$$(printf '%s\n' "$(REQUIRED_UV_VERSION)" "$$INSTALLED_UV_VERSION" | sort -V | head -n1); \
	if [ "$$DETECTED_UV_VERSION" != "$(REQUIRED_UV_VERSION)" ]; then \
		uv self update $(REQUIRED_UV_VERSION) || curl -LsSf https://astral.sh/uv/$(REQUIRED_UV_VERSION)/install.sh | sh; \
	fi
	@echo $(PYTHON_VERSION) > .python-version
.PHONY: bootstrap

install install-python: bootstrap
	@$(UV) sync --python-preference=$(UV_PYTHON_PREFERENCE)
.PHONY: install-python install

sync_extra_args ?=
sync: bootstrap check-git-configuration
	@$(UV) sync --python-preference=$(UV_PYTHON_PREFERENCE) --frozen $(sync_extra_args)
.PHONY: sync

lock: bootstrap
ifdef update_all
	@$(UV) sync -U $(sync_extra_args)
else
	@$(UV) sync $(sync_extra_args)
endif
.PHONY: lock

update: bootstrap check-git-configuration
	@$(MAKE) lock update_all=1
.PHONY: update

preview:
	$(RUN) pelican --autoreload --listen --port 4369
.PHONY: preview

build:
	$(RUN) pelican content
.PHONY: build
