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
# from wrapdb.mesonbuild.com, which the "Trusted" level blocks, so the
# environment's allowed domains must add wrapdb.mesonbuild.com (the first cloud
# build, 2026-09-25, had to fetch two patches by hand without it).
#
# Set OXIDE_CLOUD=1 in the environment's variables as well: the repo's guard
# hook then lets builds run, and integrate.sh knows it is in the cloud.
set -euo pipefail

# The cloud image carries extra package sources (the deadsnakes and ondrej
# PPAs on ppa.launchpadcontent.net) that the "Trusted" network level blocks
# with 403, and one unreachable source makes `apt-get update` fail the whole
# script (exit 100, 2026-09-25). This project needs neither, so they are
# switched off first; Ubuntu's own archives are reachable.
for f in /etc/apt/sources.list.d/*; do
    [ -e "$f" ] || continue
    if grep -qs "launchpadcontent.net\|ppa.launchpad.net" "$f"; then
        mv "$f" "$f.disabled"
    fi
done

# Metroskrew, the compiler, is a 32-bit Linux program, so it needs the 32-bit
# C library (INSTALL.md and the WSL2 setup doc list it; GitHub's runners
# already have it, which is why the ROM workflow does not install it).
dpkg --add-architecture i386

apt-get update -y
apt-get install -y --no-install-recommends \
    bison flex g++ gcc-arm-none-eabi git make ninja-build pkg-config \
    python3 python3-pip wget xz-utils libpng-dev libc6:i386

# ndspy reads NDS files and NARCs; openpyxl reads Ian's design spreadsheets.
pip3 install --break-system-packages ndspy openpyxl
