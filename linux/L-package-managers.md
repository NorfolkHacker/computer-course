---
letter: L
title: Package Managers
level: 2
image: psych-smash
---

## What went wrong

*Otic's kitchen. Otic wants a program he saw on a website. Psych is "helping".*

**Otic:** The website has a download for Fedora. It's an `.rpm` file. Is that one OK?

**Psych:** Linux is Linux. *He double-clicks it. Nothing useful happens.* Fine. We'll do it properly. *He types* `sudo apt install ./program.rpm`.

**Otic's terminal:** *(a screen of red text)*

**Otic's shirt:** MOOOOO!

**Psych:** On Arch I'd just do `pacman -Sy program`. I use Arch, by the way. *He opens a forum post titled "how to install pacman on Mint".*

**Psych:** *(lifting the Whudonk Stick)* Not a problem...

*WHUDONK.*

## The Operator says

Every family has one tool for installing software and one place to get it from. Use them and software installs cleanly, updates itself and leaves no rubbish behind. Grab random files from random websites and you get the opposite, plus whatever the Scribble packed in.

Psych's crimes today: a Fedora package on a Debian system, and an Arch habit that will one day break his machine. I'm taking notes.

## The Mender's way

A **package** is a program bundled up with the information needed to install it: its files, a description, its version, and a list of other packages it needs (its **dependencies**). A **repository**, or **repo**, is an online store of packages, checked and signed by your distro. The **package manager** downloads packages from the repos, installs their dependencies too, and keeps everything up to date.

Each family uses its own format: `.deb` for Debian, Ubuntu and Mint; `.rpm` for Fedora; `.pkg.tar.zst` for Arch. **Never mix them.** A package from another family is built for different library versions and file layouts. At best it won't install; at worst it breaks other programs.

Installing and removing need `sudo`, because they change system folders. Searching and showing information don't.

### The everyday commands

### On Debian / Ubuntu / Mint

```bash
sudo apt update
sudo apt upgrade
apt search htop
apt show htop
sudo apt install htop
sudo apt remove htop
sudo apt purge htop
sudo apt autoremove
apt list --installed
```

- `update` refreshes the list of what's available (it installs nothing). Run it before installing.
- `upgrade` installs newer versions (lesson M). `search` and `show` find and describe packages.
- `remove` uninstalls but keeps system-wide settings files; `purge` removes those too.
- `autoremove` removes dependencies nothing needs any more.

### On Fedora

```bash
dnf check-update
sudo dnf upgrade
dnf search htop
dnf info htop
sudo dnf install htop
sudo dnf remove htop
sudo dnf autoremove
dnf list --installed
```

- `check-update` lists available updates. `dnf` refreshes its lists by itself, so there's no separate step.
- `upgrade` installs newer versions (lesson M). `search` and `info` find and describe packages.
- `autoremove` clears dependencies nothing needs any more.
- `sudo dnf clean all` empties the download cache if you need disk space.

### On Arch / Manjaro

```bash
sudo pacman -Syu
pacman -Ss htop
pacman -Si htop
sudo pacman -S htop
sudo pacman -Rns htop
pacman -Qs htop
pacman -Q
pacman -Qdt
```

`pacman` uses capital letters for the main job and small letters to adjust it:

- `-S` is **sync** (install from the repos). `-Syu` refreshes the lists (`y`) **and** upgrades everything (`u`). `-Ss` searches; `-Si` shows information.
- `-R` is **remove**. `-Rns` also removes its no-longer-needed dependencies (`s`) and its saved settings files (`n`).
- `-Q` is **query** your installed packages. `-Q` alone lists them all; `-Qs` searches them; `-Qdt` lists **orphans**: packages installed as dependencies that nothing needs now. Remove any you find with `sudo pacman -Rns name`.
- `sudo pacman -Sc` clears old downloaded packages from the cache.

### Comparison

| Job | Debian / Ubuntu / Mint | Fedora | Arch / Manjaro |
|---|---|---|---|
| Refresh lists | `sudo apt update` | automatic | (part of `-Syu`) |
| Upgrade all | `sudo apt upgrade` | `sudo dnf upgrade` | `sudo pacman -Syu` |
| Search | `apt search` | `dnf search` | `pacman -Ss` |
| Show info | `apt show` | `dnf info` | `pacman -Si` |
| Install | `sudo apt install` | `sudo dnf install` | `sudo pacman -S` |
| Remove | `sudo apt remove` / `purge` | `sudo dnf remove` | `sudo pacman -Rns` |
| List installed | `apt list --installed` | `dnf list --installed` | `pacman -Q` |
| Clean up | `sudo apt autoremove` | `sudo dnf autoremove` | `pacman -Qdt`, then `-Rns` |

### Beyond the official repos

Each family has a way to get software the main repos don't carry. Each one means trusting someone extra, so use them only when you need to.

### On Debian / Ubuntu / Mint

A **PPA** (Personal Package Archive) is a repo run by one person or team on Ubuntu's Launchpad site. Mint can use them too.

```bash
sudo add-apt-repository ppa:owner/name
sudo apt update
```

Add a PPA only if the project's official website says to. Its owner can replace any package on your system, and abandoned PPAs often break the next big upgrade.

### On Fedora

Fedora leaves out some software for legal reasons, such as some video codecs. **RPM Fusion** is the long-standing community repo that provides it. Its setup page (`rpmfusion.org/Configuration`) gives the current command; at the time of writing:

```bash
sudo dnf install https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
```

`$(rpm -E %fedora)` fills in your Fedora version. The same page sets up the `nonfree` repo.

### On Arch / Manjaro

**Never install with `pacman -Sy name`.** That refreshes the lists but installs one new package on top of old ones: a **partial upgrade**. Arch only supports everything being upgraded together, and partial upgrades break programs. Always use `sudo pacman -Syu name`, or `-S name` on its own.

The **AUR** (Arch User Repository) is a huge collection of build recipes from community members. It's **not** official and nobody checks it for you. Each recipe is a script called a **PKGBUILD** that downloads and builds the program. A helper called `yay` makes this easier. Manjaro has `yay` in its repos (`sudo pacman -S yay`). On Arch, build it once from the AUR itself:

```bash
sudo pacman -S --needed git base-devel
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si
```

`git clone` downloads the recipe; `makepkg -si` builds and installs it. Then `yay name` searches repos and AUR together, and `yay -Syu` upgrades both. **Read every PKGBUILD before you install it** (`yay` offers to show it). If it downloads from anywhere strange, or you don't understand it, say no. Malware has been found in AUR packages before.

### Which to use

Official repos first, Flatpak (lesson D) second, PPAs, RPM Fusion and the AUR only when needed. Random downloaded packages, almost never.

## Do it now

This installs one small, harmless program, `cowsay`, which draws a cow saying a message, and then removes it.

Use your family's commands from the sections above.

1. Search for `cowsay`, then show its information.
2. Install it. (Debian family: run `sudo apt update` first.)
3. Run `cowsay moo`.
4. Check it's listed as installed: pipe your "list installed" command into `grep cowsay` (lesson J), or on Arch use `pacman -Qs cowsay`.
5. Remove it (`remove`, or `-Rns` on Arch), then run your family's clean-up command. On Arch, if `pacman -Qdt` lists nothing, that's fine.

You've done it when a cow said moo and is now gone again.

## Quiz

```quiz
- q: Otic runs Mint. A website offers an .rpm download. What should he do?
  options:
    - Install it with sudo apt install ./program.rpm
    - Look for the program in apt or as a Flatpak instead
    - Install pacman so he can use Arch packages too
  answer: 1
  why: .rpm is Fedora's format. Mixing families breaks things; use your own family's repos or Flatpak.
- q: On Arch, how should Psych install a new package?
  options:
    - "sudo pacman -Sy name"
    - "sudo pacman -Syu name"
    - "sudo pacman -Rns name"
  answer: 1
  why: -Sy alone refreshes the lists without upgrading, a partial upgrade that breaks things. -Syu upgrades everything together.
- q: What should you do before installing anything from the AUR?
  options:
    - Read its PKGBUILD
    - Run it as root
    - Nothing, the AUR is official
  answer: 0
  why: The AUR is community-run and unchecked. The PKGBUILD shows exactly what it will download and run.
```

## Scribble watch

The Scribble's favourite installer is a website that says "just run `curl https://... | sudo bash`". That downloads a script and runs it as root, unseen, with no package manager to keep track or remove it later. Install from your distro's repos or Flatpak. If a project only offers a script, download it first, read it, and decide.
