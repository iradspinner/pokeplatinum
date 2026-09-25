#!/bin/bash
# Setup script for Platinum Oxide's Claude Code cloud environment.
#
# Paste this file's contents into the environment's setup script at
# claude.ai/code. It runs as root on the environment's Ubuntu 24.04 image,
# before any session starts, and the result is cached for about a week. It
# installs what GitHub's ROM workflow installs (.github/workflows/oxide-rom.yml)
# plus the two Python packages the tools in tools/oxide/ import. The compiler
# (Metroskrew) and meson are fetched by the first `make rom` into the repo
# itself, from github.com; the meson subprojects also come from github.com and
# wrapdb.mesonbuild.com, so if a first build fails to reach the second, add it
# to the environment's allowed domains.
#
# Set OXIDE_CLOUD=1 in the environment's variables as well: the repo's guard
# hook then lets builds run, and integrate.sh knows it is in the cloud.
set -euo pipefail

apt-get update -y
apt-get install -y --no-install-recommends \
    bison flex g++ gcc-arm-none-eabi git make ninja-build pkg-config \
    python3 python3-pip wget xz-utils libpng-dev

# ndspy reads NDS files and NARCs; openpyxl reads Ian's design spreadsheets.
pip3 install --break-system-packages ndspy openpyxl
