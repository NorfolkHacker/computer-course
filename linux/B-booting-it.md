---
letter: B
title: Booting It
level: 1
image: whoosh
---

## What went wrong

*The woods. Psych holds a USB stick aloft like a trophy.*

**Psych:** Downloaded Arch. Dragged it onto the stick. *(he restarts the laptop. Windows starts as usual.)* Huh.

**Otic:** Did you copy the file, or *write* it?

**Psych:** Same thing. *(he drags the ISO across again. Windows starts again.)* Not a problem. *(the Whudonk Stick crackles)* I'll just install it straight over Windows.

**Otic:** On your only computer? With all your photos on it?

**Otic:** *(the cow on his shirt)* MOOOOO!

## The Operator says

Luser list, entry 4,117: "Installed Linux over his only copy of the wedding photos. Asked me to undo it."

There is no undo. An installer that says **Erase disk** means it. That's why you're starting in a virtual machine: a pretend computer living in a window, which you can smash, wipe and rebuild before your tea goes cold. Nothing in there can touch your real files. Break it a few times first. Then we'll talk about real hardware. Probably.

## The Mender's way

You need Linux running somewhere. There are three ways, safest first.

| Way | What it is | Risk to your files |
|---|---|---|
| **Virtual machine** (recommended) | A pretend computer inside a window on Windows. | None. |
| **Live USB** | Linux runs from a USB stick, installing nothing unless you choose. | None, until you click **Install**. |
| **A spare PC** | An old computer you don't need, wiped for Linux. | Wipes that PC. |

Use a virtual machine for this course. You can try all three families that way.

### Download the ISO

An **ISO** is a single file holding a whole installer disc. Only download it from the official site:

- **Linux Mint**: `linuxmint.com` → **Download**. Choose the **Cinnamon Edition**.
- **Ubuntu**: `ubuntu.com` → **Download** → **Ubuntu Desktop** (pick the newest **LTS**, such as 26.04 LTS).
- **Fedora**: `fedoraproject.org` → **Workstation** → download the **x86_64** live ISO.
- **Arch**: `archlinux.org` → **Download**, then a UK mirror.

### Check the download

Each download page lists a **SHA256 sum**: a long string worked out from the file. If your copy gives the same string, it arrived whole and untampered. On Windows, open **PowerShell** (**Start**, type `powershell`, <kbd>Enter</kbd>), type `Get-FileHash ` (with a space), drag the ISO onto the window (so the real file name, with its version number, fills in) and press <kbd>Enter</kbd>:

```powershell
Get-FileHash C:\Users\you\Downloads\linuxmint-cinnamon-64bit.iso
```

Compare the **Hash** it prints with the official one (Mint and Ubuntu list theirs in a `sha256sum.txt` or `SHA256SUMS` file beside the download, Fedora in its **CHECKSUM** file, Arch on the download page). If they differ, delete the file and download it again. On Linux, the same check is `sha256sum` followed by the file name.

### Make a virtual machine

**VirtualBox** is free software that runs virtual machines. Download it from `virtualbox.org` (**Windows hosts**) and install it with the default options.

1. Open **VirtualBox** and click **New** (top of the window).
2. **Name**: `Mint` (or `Fedora`, or `Arch`).
3. **ISO Image**: choose **Other...** and pick your ISO. VirtualBox usually fills in **Type** and **Version**; check they say **Linux** and your distro.
4. Turn off the automatic (**unattended**) install, so you do the install yourself. On VirtualBox 7.0, tick **Skip Unattended Installation**; on newer versions, untick **Install OS Using Unattended Installation** (or a box with similar wording).
5. Set **Base Memory** to at least `4096 MB` and **Processors** to `2`.
6. Give the virtual hard disk `25 GB` or more. (On VirtualBox 7.0 this is its own page: choose **Create a Virtual Hard Disk Now**.)
7. Click **Next** through any remaining pages, then **Finish**.
8. Select your new machine on the left and click **Start**.

The wording and layout move around between VirtualBox 7 versions (7.0 uses separate pages with **Next**; newer versions put the sections on one page); the choices are the same. An error about **VT-x** or **AMD-V** means virtualisation is switched off in your PC's firmware settings (the **BIOS** or **UEFI**). If the mouse gets stuck inside the VM, press the right-hand <kbd>Ctrl</kbd> key (the **Host key**).

### Or: a live USB

A **live USB** is a stick Linux can start from. Copying the ISO onto it isn't enough; it must be *written* specially, which wipes the stick (8 GB or more).

- **Ventoy** (`ventoy.net`): install it onto the stick once, then just copy ISOs onto it. At boot it offers a menu of them.
- **balenaEtcher** (`etcher.balena.io`): **Flash from file** → the ISO → **Select target** → the stick → **Flash!**
- **Rufus** (`rufus.ie`): the stick under **Device**, **SELECT** for the ISO, then **START**.

Restart with the stick in and press the **boot menu key** as the PC powers on (usually <kbd>F12</kbd>, <kbd>F11</kbd>, <kbd>Esc</kbd> or <kbd>F8</kbd>, depending on the maker), then choose the stick. Mint, Ubuntu and Fedora start a desktop you can try without installing. The Arch ISO doesn't support **Secure Boot**, so on real hardware you may need to turn that off in the firmware settings.

### Install it

In the VM, **erase disk** means the VM's pretend disk only.

### On Debian / Ubuntu / Mint

**Mint**: double-click **Install Linux Mint** on the live desktop.

1. Choose your language and keyboard layout (**English (UK)**).
2. Tick **Install multimedia codecs** (for videos and music).
3. Choose **Erase disk and install Linux Mint**, then **Install Now**, then **Continue**.
4. Click your location on the map (London).
5. Fill in your name, computer name, username and password. Write the password down.
6. When it finishes, click **Restart Now**.

**Ubuntu**: the installer opens by itself (the wording below is from 24.04 LTS; newer versions are very similar). Choose **Install Ubuntu**, **Interactive installation**, tick both third-party boxes, then **Erase disk and install Ubuntu**. Create your account, pick your time zone, and click **Install**.

### On Fedora

Fedora's installer is called **Anaconda**. On the live desktop, choose **Install Fedora** (in some versions it's called **Install to Hard Drive**).

1. Choose your language.
2. Choose the disk and the option to use the whole disk, partitioned automatically (the wording differs between Fedora releases).
3. Review the summary and start the installation.
4. When it's done, restart.

On first boot a setup wizard asks for your username and password, and offers to **Enable Third-Party Repositories**. Say yes: lesson D uses them.

### On Arch / Manjaro

Arch is a bigger job, honestly. It boots to a text prompt, `root@archiso ~ #`, not a desktop. In a VM the internet already works. Type:

```bash
archinstall
```

`archinstall` is Arch's official guided installer: a menu you drive with the arrow keys and <kbd>Enter</kbd>.

1. **Mirrors and repositories** → **Select regions**: choose **United Kingdom**.
2. **Locales**: set the keyboard layout to `uk`.
3. **Disk configuration**: choose **Use a best-effort default partition layout**, and the VM's disk.
4. **Authentication**: set a **Root password** and add a **User account** (older versions show these two directly on the main menu). Answer yes when it asks whether your user should be a **superuser (sudo)**.
5. **Profile** → **Desktop** → pick **GNOME**, **KDE Plasma** or **Cinnamon**.
6. **Network configuration**: choose **Use Network Manager**.
7. **Timezone**: `Europe/London`.
8. Choose **Install**, wait, then reboot.

Menu names shift between `archinstall` versions; read each before pressing <kbd>Enter</kbd>. **Manjaro** is gentler: a desktop with a graphical installer, much like Mint's.

### After installing

If the VM boots back into the installer, shut it down, open its **Settings** → **Storage**, remove the ISO, and start it again.

### Dual-booting

**Dual-booting** means Windows and Linux on one computer, choosing at start-up. It's possible, but one wrong click erases Windows. If you ever try it, **back up everything first** (main course, lesson L) and follow your distro's own guide.

## Do it now

1. Install VirtualBox.
2. Download the ISO for the distro you chose in lesson A, and check its SHA256 sum.
3. Make a VM for it and install it, following the tab for your family.
4. Restart the VM and log in with your username and password.

You've done it when you see your new Linux desktop, inside a window, with Windows still safely running around it.

## Quiz

```quiz
- q: Psych dragged the Arch ISO onto a USB stick and it wouldn't boot. Why?
  options:
    - The stick was too small
    - An ISO must be written with a tool like Ventoy, balenaEtcher or Rufus, not just copied
    - Arch doesn't work from USB
  answer: 1
  why: Copying puts the ISO there as an ordinary file. A writing tool (or Ventoy) makes the stick bootable.
- q: What's the safest way to try Linux while learning?
  options:
    - Install it over Windows on your only PC
    - Dual-boot straight away
    - A virtual machine in VirtualBox
  answer: 2
  why: A virtual machine is a pretend computer in a window. Wiping its disk can't touch your real files.
- q: Why check an ISO's SHA256 sum?
  options:
    - To prove the download arrived complete and wasn't tampered with
    - To make it download faster
    - To unlock the installer
  answer: 0
  why: If your file's SHA256 matches the one on the official site, it's the genuine, complete file.
```

## Scribble watch

The Scribble runs lookalike download sites: "Fast Linux Mint Download!", with a bundled extra you didn't ask for. Only download ISOs from the distro's own site (or the mirrors it lists), and check the SHA256 sum against the number on that official page. If they don't match, delete the file. Don't "try it anyway".
