# Setup: GitHub fork and WSL2 build environment

Written 2026-09-15. Do these in order. Each step says what you should see when it worked. Nothing here touches your existing ROMs or DSPRE files.

## Part 1: GitHub fork (10 minutes, in a browser)

1. Sign in to GitHub and open https://github.com/pret/pokeplatinum.
2. Click **Fork** (top right), keep the name `pokeplatinum`, make sure "Copy the main branch only" is ticked, click **Create fork**. You now have `https://github.com/<your-username>/pokeplatinum`.
3. Send me the URL of your fork.

## Part 2: WSL2 and the build tools (30 to 40 minutes, mostly waiting)

WSL2 is a Linux environment that runs inside Windows. The decomp's build tools are Linux tools, so this is how you run them. You will type commands into a terminal; everything below is copy-paste.

1. **Install WSL.** Open the Start menu, type `PowerShell`, right-click **Windows PowerShell**, choose **Run as administrator**. Paste and press Enter:
   ```
   wsl --install -d Ubuntu
   ```
   It downloads Ubuntu (a few hundred MB). When it asks, restart the PC. If Windows complains about virtualization, it needs enabling in your BIOS/UEFI; tell me your motherboard model and I will give you the exact menu path.

2. **First launch.** After the restart, Ubuntu opens on its own (or open it from the Start menu). It asks for a Linux username and password. Use something short and lowercase, and remember the password; you will type it for `sudo` commands. You should end at a prompt like `ian@DESKTOP:~$`.

3. **Confirm it is WSL2.** In PowerShell (normal, not admin):
   ```
   wsl -l -v
   ```
   You should see `Ubuntu` with VERSION `2`. If it says 1: `wsl --set-version Ubuntu 2`.

4. **Install the build dependencies.** In the Ubuntu window, paste this whole block and press Enter. It asks for your password once and then runs for several minutes:
   ```
   sudo dpkg --add-architecture i386 && sudo apt update && sudo apt install -y bison flex g++ gcc-arm-none-eabi git make ninja-build pkg-config wget python3 python3-pip xz-utils nasm libc6:i386 libpng-dev && pip3 install --user --break-system-packages meson
   ```
   Success looks like a return to the prompt with no red `E:` lines.

5. **Tell git who you are** (one time):
   ```
   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"
   ```

6. **Clone your fork into the Linux filesystem.** Not into `/mnt/g/...`; the build is far slower on Windows drives.
   ```
   cd ~
   git clone https://github.com/<your-username>/pokeplatinum.git
   cd pokeplatinum
   ```

7. **Build once, unmodified, to prove the setup.** This downloads the compiler automatically and then compiles everything. Expect 10 to 20 minutes the first time.
   ```
   make
   ```
   Success looks like the last lines mentioning `pokeplatinum.us.nds` and a test step passing the checksum. The ROM is at `~/pokeplatinum/build/pokeplatinum.us.nds`. If anything fails, copy the last 30 lines of output to me.

8. **Find the ROM from Windows.** In File Explorer's address bar type `\\wsl$\Ubuntu\home\<your-linux-username>\pokeplatinum\build` and press Enter. Copy `pokeplatinum.us.nds` from there into a Windows folder to run it in your emulator. Do not edit files under `\\wsl$` from Windows tools; treat it as read-only.

## Part 3: The routine once we are set up

Each time I finish a change, I will say so. You then run, in Ubuntu:
```
cd ~/pokeplatinum && git pull && make rom
```
`make rom` skips the checksum test (which is expected to fail once we change things) and rebuilds only what changed, usually well under a minute. Copy the ROM out as in step 8 and play-test. Report what you see; screenshots help.

**Builds on GitHub, retired.** From 2026-09-23 to 2026-09-29, while this box's CPU was degraded, playtest ROMs came from GitHub's machines, built by the private repo `iradspinner/oxide-rom-builder` through `tools/oxide/fetch-rom`. The replacement CPU builds the same ROM byte for byte, so both were retired on 2026-10-01 (Ian): every ROM is built here, and the public repo's build of each push to `oxide` gives the SHA-1 to compare with.

If you ever want to throw away every local change and match my latest push exactly:
```
cd ~/pokeplatinum && git fetch && git reset --hard origin/oxide
```

## Part 3b: Python packages

The helper scripts under `tools/oxide/` run on the system `python3` and need
four packages that Ubuntu does not ship (numpy for the balance track's
`fightfit.py` only). They are installed for the user:

```
python3 -m pip install --user --break-system-packages ndspy pillow openpyxl numpy
```

For a day in September 2026 the project pinned its own interpreter, blaming
the system Python for wrong answers that turned out to be a degraded CPU; the
pin was removed once that was found (design doc findings log, 2026-09-22).
The `Makefile` put `~/.venvs/oxide` first on PATH until the replacement CPU
was in (2026-09-29); the build now uses the system Python.

## Part 4: What about DSPRE and the old base ROM?

Both stay where they are. The built ROM from the decomp is a normal `.nds` and DSPRE can open it for inspection. The base ROM (since 2026-09-26 your `Test.nds` of 2026-08-31) is a reference: Phase 3 re-created its edits in the source tree (see `phase3-base-rom-inventory.md`), and every verify tool compares the build against it. Nothing you do in DSPRE on the old base will flow into the new ROM, so from here on, edits should go through me into the source tree, or, once you are comfortable, directly into the `res/` data files in the fork.

## Part 5: Debugger in WSL2 (written 2026-09-20)

> **Do not use this route. Read Part 5b instead.** Part 5 records how an agent ran
> its own melonDS under WSLg. It was tried on 2026-09-20 and 2026-09-21 and does
> not work well enough to be worth the tokens: a headless emulator has to be
> driven blind through screenshots and synthetic button presses, the stub's
> limits bite harder without a person watching, and a second copy of the game
> is one more thing to keep in step. The way debugging is done on this project is
> that **Ian runs melonDS on Windows and drives the game; the agent attaches to
> his emulator over the stub with `tools/oxide/live_watch.py` and reads.** Ian
> restarts the emulator at the startup break, says go, plays to the point of
> interest, and reports what he sees; the agent plants breakpoints, reads memory,
> and asks Ian for the next input. On 2026-09-22 a fresh bug-fix session was
> handed a prompt that did not say this and spent its budget rebuilding the
> Part 5 route before getting anywhere, which is why this banner exists. The GDB
> build below stays because `tools/oxide/melonds.gdb` and offline struct-offset
> reads use it; the WSLg melonDS recipe was removed in the 2026-09-21 docs pass.


What is needed to attach a debugger to the built ROM without leaving WSL2 and without sudo. All of it was done once and lives under `~/tools/`; the only repo pieces are `tools/oxide/live.py` and `tools/oxide/melonds.gdb`.

**GDB, the overlay-aware fork.** The prebuilt binary on the fork's Releases page needs `libpython3.12`, which Ubuntu 26.04 does not have, so it is built from source with Python off. GMP and MPFR headers are not installed and there is no sudo, so both are built statically first. GCC 15 defaults to C23, which breaks GMP's configure tests and the bundled readline, hence the C-standard and permissive flags; `MAKEINFO=true` has to be on the make line, not in the environment, or the bfd docs fail the build.
```
git clone --depth 1 https://github.com/joshua-smith-12/binutils-gdb-nds.git ~/tools/binutils-gdb-nds
D=~/tools/deps; mkdir -p $D/src $D/prefix; cd $D/src
curl -sLO https://gmplib.org/download/gmp/gmp-6.3.0.tar.xz && curl -sLO https://ftp.gnu.org/gnu/mpfr/mpfr-4.2.1.tar.xz
tar xf gmp-6.3.0.tar.xz && tar xf mpfr-4.2.1.tar.xz
(cd gmp-6.3.0 && CC="gcc -std=gnu17" ./configure --prefix=$D/prefix --disable-shared && make -j32 && make install)
(cd mpfr-4.2.1 && CC="gcc -std=gnu17" ./configure --prefix=$D/prefix --with-gmp=$D/prefix --disable-shared && make -j32 && make install)
mkdir ~/tools/binutils-gdb-nds/build && cd ~/tools/binutils-gdb-nds/build
CFLAGS="-O2 -std=gnu17 -fpermissive -Wno-error" CXXFLAGS="-O2 -Wno-error" MAKEINFO=true \
  ../configure --target=arm-none-eabi --prefix=$HOME/tools/gdb-nds --with-gmp=$D/prefix --with-mpfr=$D/prefix \
  --with-python=no --disable-binutils --disable-ld --disable-gas --disable-gprof --disable-gold --disable-sim --disable-gdbserver
make -j32 MAKEINFO=true all-gdb && make MAKEINFO=true install-gdb
```
Result: `~/tools/gdb-nds/bin/arm-none-eabi-gdb` (GDB 16 with the fork's overlay support). `tools/oxide/melonds.gdb` is the init script: from the repo root, `~/tools/gdb-nds/bin/arm-none-eabi-gdb -x tools/oxide/melonds.gdb`. It loads `build/main.nef`, the linked ELF with DWARF, which exists for both `make rom` and `make debug`; `debug.nef` only differs in having source paths rewritten by `debugedit`, which is not installed, and the init script's `substitute-path` does the same job. Only a `make debug` build exports `_ovly_table`, so `overlay auto` follows overlay loads only there; a release build still names whatever overlay is loaded. Offline use also works (`-batch -ex "file build/main.nef" -ex "print/x &((BattleContext*)0)->battleMons[0].curHP"`), which is the quickest way to get a struct offset.

### Part 5b: the Windows melonDS stub from WSL2 (2026-09-21)

**This is the working method, and it is a two-person loop**: Ian owns the
emulator and the agent never launches one. The setup it needs on Ian's side:
`networkingMode=mirrored` in `C:\Users\Ian\.wslconfig` (and a `wsl --shutdown`),
so WSL2 shares localhost with Windows and Ian's own melonDS 1.1 can serve the
stub (Config, Emu settings, Devtools: GDB stub on, ARM9 port 3333, **Break on
startup on**). The loop itself, the stub's limits and `live_watch.py`'s options
are the `debug-live` skill.
