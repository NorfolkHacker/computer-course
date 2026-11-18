---
letter: M
title: Updates
level: 2
image: whoosh
---

## What went wrong

*The woods. Psych hasn't turned on his Arch laptop for four months. Otic hasn't updated his Mint laptop for four months either. They decide to catch up together.*

**Psych:** Watch. One command. *He types* `sudo pacman -Syu` *and presses Enter without reading anything. Hundreds of packages scroll past. A message about manual intervention scrolls past too.* I use Arch, by the way.

**Otic:** Mine's got a little shield icon with a number on it. It says 214.

**Psych:** That's too many. Don't bother. *He reboots his own laptop.*

*Psych's laptop shows a black screen with a blinking cursor. Nothing else.*

**Psych:** It's thinking.

*It isn't thinking.*

**Otic's shirt:** MOOOOO!

*Psych lifts the Whudonk Stick. The Mender, on his stump, is already holding out a USB stick.*

## The Operator says

Two kinds of people ring me about updates. Those who never do them, whose machines the Scribble walked into months ago. And those who do them at five to nine, before a meeting, without reading a word.

Updates are mostly security fixes. Doing them often keeps you safe. Doing them sensibly (reading the screen, rebooting when asked, knowing how to go back) keeps you working. Psych managed neither.

## The Mender's way

Updates keep your system safe. Little and often is easiest.

### Fixed and rolling releases

Distros release new versions in one of two ways:

- **Fixed releases** come out on a schedule. Between releases you get security and bug fixes, but programs stay on roughly the same version, so nothing changes under your feet. Ubuntu releases every six months, with a **Long Term Support (LTS)** version every two years (like 24.04) that's supported for five years. Mint is built on Ubuntu LTS. Fedora releases roughly every six months, and each version is supported for about thirteen months, so you upgrade about once a year.
- A **rolling release** never has versions. Updates arrive continuously, so you always have the newest software. Arch is rolling. Manjaro is rolling too, but holds updates back a couple of weeks for extra testing.

Fixed is calmer. Rolling is newer, and needs more attention.

### Routine updates

Do this at least once a week.

### On Debian / Ubuntu / Mint

```bash
sudo apt update
sudo apt upgrade
```

`update` refreshes the package lists; `upgrade` installs the newer versions. Read the list of changes and type `y` to go ahead. Or use the graphical tool: **Update Manager** on Mint (the shield icon, bottom-right of the panel) or **Software Updater** on Ubuntu.

### On Fedora

```bash
sudo dnf upgrade --refresh
```

`--refresh` makes sure it checks for the very latest lists first. Fedora Workstation's **Software** app (GNOME Software) also offers updates under its **Updates** tab, and usually installs them while restarting the computer.

### On Arch / Manjaro

Before updating Arch, read the latest news at `archlinux.org` (the front page). Sometimes an update needs you to do something by hand first, and the news tells you exactly what.

```bash
sudo pacman -Syu
```

Read the output. Messages beginning `==>` or saying something was installed as `.pacnew` mean a config file needs attention. Manjaro has a graphical updater too, and posts announcements on its forum.

### When to reboot

Most updates take effect when you next start the program. A few need a **reboot** (restarting the computer): especially the **kernel** (lesson A) and core system libraries. Until you reboot, the old version is still running.

### On Debian / Ubuntu / Mint

Ubuntu tells you with a message on screen, and creates a file called `/var/run/reboot-required`. The `needrestart` tool (installed on many Ubuntu systems; if it's missing, install it with `sudo apt install needrestart`) runs after each upgrade and lists anything still using old versions. To check by hand:

```bash
sudo needrestart
```

### On Fedora

```bash
sudo dnf needs-restarting -r
```

`-r` asks just "does the whole machine need a reboot?". It answers yes or no and gives the reason. If the command isn't found, install the plugins with `sudo dnf install dnf5-plugins`.

### On Arch / Manjaro

There's no built-in checker. If the update list included `linux` (the kernel), reboot. You can compare the running kernel with the installed one:

```bash
uname -r
pacman -Q linux
```

If the versions differ, reboot. (On Manjaro the kernel package is named after its version, such as `linux612`.)

### Upgrading to a new release

This moves you to the next version of your distro: a bigger job. **Back up your files first** (lesson X; for now, copy anything important to a USB stick), and do a routine update and reboot before you start.

### On Debian / Ubuntu / Mint

On Ubuntu:

```bash
sudo do-release-upgrade
```

By default, LTS versions only offer the next LTS, and only once its first point release (such as 26.04.1) is out.

On Mint, small "point" upgrades (22 to 22.1) are offered in **Update Manager** under **Edit**. A big jump (21 to 22) uses Mint's own tool, `mintupgrade`; follow the official upgrade guide on `linuxmint.com`'s blog for that release.

### On Fedora

```bash
sudo dnf upgrade --refresh
sudo dnf system-upgrade download --releasever=42
sudo dnf system-upgrade reboot
```

Change `42` to the version you're moving to. The computer restarts, installs the upgrade, and restarts again. Check Fedora's docs before skipping a version. GNOME Software also offers the upgrade with a button.

### On Arch / Manjaro

There are no releases to upgrade between. Your routine `pacman -Syu` keeps you on the current version. That's why reading the news before each update matters.

### Keeping an older kernel

If a new kernel won't boot, you can pick an older one from the **boot menu** (called **GRUB** on most systems; lesson Y covers it). Hold <kbd>Shift</kbd> or tap <kbd>Esc</kbd> while the computer starts if the menu doesn't appear, then choose **Advanced options**.

### On Debian / Ubuntu / Mint

The previous kernel stays installed until `autoremove` removes it, so there's usually one to fall back on. Mint's **Update Manager** has **View → Linux Kernels** for choosing and installing kernels.

### On Fedora

Fedora keeps the three most recent kernels and shows them all in the boot menu.

### On Arch / Manjaro

Arch keeps only one kernel, replacing it on each update. Install the **long-term support** kernel as a spare, so there's always a second choice in the boot menu:

```bash
sudo pacman -S linux-lts
```

If you use GRUB, regenerate its menu afterwards with `sudo grub-mkconfig -o /boot/grub/grub.cfg`. Manjaro offers kernels in **Manjaro Settings Manager** under **Kernel**.

## Do it now

1. Check what kind of release you have: `cat /etc/os-release`. Find the version number (Arch has none).
2. Run the routine update for your family, above. Read the list before agreeing. On Arch, read the news page first.
3. Check whether you need a reboot, using your family's method above. If you do, reboot.
4. After rebooting, run `uname -r` to see which kernel you're running now.
5. Open your desktop's graphical updater (Update Manager, Software Updater, or GNOME Software) and find where it shows available updates.

You've done it when your system is up to date, you know whether it needed a reboot, and you can name your kernel version.

## Quiz

```quiz
- q: What's the difference between a fixed and a rolling release?
  options:
    - Fixed releases never get security updates
    - Fixed releases come in versions on a schedule; rolling releases update continuously
    - Rolling releases only update once a year
  answer: 1
  why: Mint and Fedora come in versions. Arch has no versions and updates continuously.
- q: What should an Arch user do before running sudo pacman -Syu?
  options:
    - Read the news on archlinux.org
    - Run pacman -Sy first
    - Nothing, just reboot afterwards
  answer: 0
  why: The news warns about updates that need a manual step. Skipping it is how Psych ended up with a black screen.
- q: You've installed a kernel update. When does the new kernel start being used?
  options:
    - Straight away
    - After you log out
    - After you reboot
  answer: 2
  why: The running kernel can't be swapped while it's running. Reboot to start using the new one.
```

## Scribble watch

The Scribble loves a machine that hasn't been updated in months: every known hole is still open. It also loves fake "urgent update" pop-ups on websites. Real updates only ever come from your package manager or your distro's own update app. Never install an "update" from a web page, and update at least weekly.
