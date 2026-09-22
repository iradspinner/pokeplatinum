# Keep this list in alphabetical order for ease of reference.
.PHONY:           \
	all           \
	check         \
	clean         \
	configure     \
	distclean     \
	debug         \
	format        \
	meson         \
	purge         \
	release       \
	rom           \
	setup_debug   \
	setup_release \
	skrew         \
	skrewrm       \
	skrewup       \
	target        \
	update

ROM_REVISION ?= 1

SUBPROJ_DIR := subprojects

MESON_VER := 1.12.0
MESON_DIR := $(SUBPROJ_DIR)/meson-$(MESON_VER)
MESON_PY  := $(MESON_DIR)/meson.py

# Platinum Oxide: the build's Python is pinned rather than inherited from PATH.
# This machine's system Python intermittently returns wrong answers from pure
# string work, and `make rom` runs Python about 227 times to generate event
# data, map matrices and the encounter archives, so the build is exposed to it.
# tools/oxide/oxide-python resolves the pinned interpreter and explains why.
# Two things have to happen for it to cover the build. PYTHON runs meson
# itself. But meson records each generator script as the command, not an
# interpreter plus the script, so ninja runs each one's `#!/usr/bin/env
# python3` shebang; the pinned interpreter's directory therefore goes first on
# PATH for every recipe below, which is what makes the shebang resolve to it
# (the 2026-09-22 QA pass found the build on the system Python without this).
# Override with OXIDE_PYTHON=/path/to/python, or set MESON to bypass this.
# Note the wrapper is not a fix for this machine's fault: see the QA outcome at
# the top of docs/oxide/tracker.md.
PYTHON ?= tools/oxide/oxide-python
OXIDE_PYTHON_DIR := $(dir $(shell $(PYTHON) --path 2>/dev/null))
ifneq ($(OXIDE_PYTHON_DIR),)
  export PATH := $(OXIDE_PYTHON_DIR):$(PATH)
endif

MESON ?= $(PYTHON) $(MESON_PY)
NINJA ?= ninja
GIT ?= git

BUILD ?= build

UNAME_R := $(shell uname -r)
UNAME_S := $(shell uname -s)
CWD := $(shell pwd)

# Check for Windows-drive access
ifneq (,$(findstring Microsoft,$(UNAME_R)))
  ifneq (,$(filter /mnt/%,$(realpath $(CWD))))
    WSL_ACCESSING_WINDOWS := 0
  else
    WSL_ACCESSING_WINDOWS := 1
  endif
else
  WSL_ACCESSING_WINDOWS := 1
endif

# Set up the compiler toolchain dependency
SKREW_GET := tools/devtools/get_metroskrew.sh
SKREW_VER := 0.1.3
SKREW_DIR := tools/metroskrew

ifneq (,$(findstring Linux,$(UNAME_S)))
  ifeq (0,$(WSL_ACCESSING_WINDOWS))
    NATIVE := native.ini
    CROSS := cross.ini
    SKREW_SYS := windows
    SKREW_EXE := $(SKREW_DIR)/bin/skrewrap.exe
  else
    NATIVE := native.ini
    CROSS := cross_unix.ini
    SKREW_SYS := linux
    SKREW_EXE := $(SKREW_DIR)/bin/skrewrap
  endif
else
  ifneq (,$(findstring Darwin,$(UNAME_S)))
    NATIVE := native_macos.ini
    CROSS := cross_unix.ini
    SKREW_SYS := wine
    SKREW_EXE := $(SKREW_DIR)/bin/skrewrap
  else
    ifneq (,$(findstring BSD, $(UNAME_S)))
      NATIVE := native.ini
      CROSS := cross_unix.ini
      SKREW_SYS := linux
      SKREW_EXE := $(SKREW_DIR)/bin/skrewrap
    else
      NATIVE := native.ini
      CROSS := cross.ini
      SKREW_SYS := windows
      SKREW_EXE := $(SKREW_DIR)/bin/skrewrap.exe
    endif
  endif
endif

export NINJA_STATUS := [%p %f/%t] 

# Modders can delete the `check` dependency here after their first build.
all: release check

.NOTPARALLEL: release
release: setup_release rom

.NOTPARALLEL: debug
debug: setup_debug rom
	$(NINJA) -C $(BUILD) debug.nef overlay.map

check: rom
	$(MESON) test -C $(BUILD)

rom: $(BUILD)/build.ninja
	$(NINJA) -C $(BUILD) pokeplatinum.us.nds

format: $(BUILD)/build.ninja
	$(NINJA) -C $(BUILD) clang-format

target: $(BUILD)/build.ninja
	$(MESON) compile -C $(BUILD) $(MESON_TARGET)

clean: $(BUILD)/build.ninja
	$(MESON) compile -C $(BUILD) --clean
	rm -rf $(BUILD)/res

distclean:
	rm -rf $(BUILD)

purge: distclean
	rm -rf $(SKREW_DIR)
	! test -f $(MESON_PY) || $(MESON) subprojects purge --confirm
	rm -rf $(MESON_DIR)

update: meson skrewup
	$(MESON) subprojects update || true

setup_release: $(BUILD)/build.ninja
	$(MESON) configure $(BUILD) -Dgdb_debugging=false -Dlogging_enabled=false

setup_debug: $(BUILD)/build.ninja
	$(MESON) configure $(BUILD) -Dgdb_debugging=true -Dlogging_enabled=true

configure: $(BUILD)/build.ninja

$(BUILD)/build.ninja: | $(BUILD) $(SKREW_EXE) meson
	$(MESON) setup \
		-Drevision=$(ROM_REVISION) \
		--wrap-mode=nopromote \
		--native-file=meson/$(NATIVE) \
		--cross-file=meson/$(CROSS) \
		-- $(BUILD)

$(BUILD):
	mkdir -p -- $(BUILD)

meson: $(MESON_PY)

$(MESON_PY):
	$(GIT) clone --depth=1 -b $(MESON_VER) https://github.com/mesonbuild/meson $(@D)

skrew: $(SKREW_EXE)

skrewrm:
	rm -rf $(SKREW_DIR)

skrewup: skrewrm skrew

$(SKREW_EXE):
	SKREW_SYS=$(SKREW_SYS) SKREW_VER=$(SKREW_VER) SKREW_DIR=$(SKREW_DIR) $(SKREW_GET)
