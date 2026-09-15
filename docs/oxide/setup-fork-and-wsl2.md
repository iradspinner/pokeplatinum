# Setup: GitHub fork and WSL2 build environment

Written 2026-09-15. Do these in order. Each step says what you should see when it worked. Nothing here touches your existing ROMs or DSPRE files.

## Part 1: GitHub fork (10 minutes, in a browser)

1. Sign in to GitHub and open https://github.com/pret/pokeplatinum.
2. Click **Fork** (top right), keep the name `pokeplatinum`, make sure "Copy the main branch only" is ticked, click **Create fork**. You now have `https://github.com/<your-username>/pokeplatinum`.
3. Send me the URL of your fork.

For me to push changes into your fork, I need permission. Two options; pick one:

- **Token (recommended).** GitHub > your profile picture > Settings > Developer settings > Personal access tokens > **Fine-grained tokens** > Generate new token. Name it `platinum-oxide`, set an expiry you are comfortable with (90 days is fine, it can be regenerated), under Repository access choose **Only select repositories** and pick your `pokeplatinum` fork, and under Permissions > Repository permissions set **Contents: Read and write**. Generate it and save the token string as a text file named `github-token.txt` in the project working folder. I read that file at the start of each session and never write it anywhere else. It only works on that one repository, and you can revoke it from the same page at any time. It is plain text on your disk, so do not commit it or share the folder.
- **Patch files.** I write `.patch` files into the working folder and you apply them yourself with `git am` in WSL. No token needed, but every change requires you to run a command, and it gets tedious.

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

If you ever want to throw away every local change and match my latest push exactly:
```
cd ~/pokeplatinum && git fetch && git reset --hard origin/main
```

## Part 4: What about DSPRE and the old base ROM?

Both stay where they are. The built ROM from the decomp is a normal `.nds` and DSPRE can open it for inspection. The old base ROM is now a reference: its edits are being re-created in the source tree (see `phase3-base-rom-inventory.md`), and it will be compared against as that happens. Nothing you do in DSPRE on the old base will flow into the new ROM, so from here on, edits should go through me into the source tree, or, once you are comfortable, directly into the `res/` data files in the fork.
