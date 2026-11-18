# Linux Course: Design

Date: 2026-11-18
Status: approved (curriculum approved in chat; technical design follows the main course)

## Purpose

A second, standalone A–Z course: general Linux, beginner to **confident admin**.
It shows command variations for three distro families. Same humour and cast as the main
course (`docs/superpowers/specs/2026-11-18-computer-course-design.md`).

Success: someone who has finished (or skipped) the main course can install Linux, live
in the terminal, administer a machine, and build and look after a small home server,
on Debian/Ubuntu/Mint, Fedora/RHEL or Arch/Manjaro.

## Distro families

| Tab | Covers | Package tool |
|---|---|---|
| **Debian** | Debian, Ubuntu, Linux Mint (and Parrot) | apt |
| **Fedora** | Fedora, RHEL, Rocky/Alma | dnf |
| **Arch** | Arch, Manjaro, EndeavourOS | pacman (+ AUR) |

Wherever a step differs, the lesson has `### On Debian`, `### On Fedora`, `### On Arch`
sections. Steps that are the same everywhere are written once.

## Cast

Same as the main course. Linux is the Operator's home turf, so he's almost cheerful. Psych runs **Arch**
and mentions it constantly. Otic runs **Mint**. The Mender quietly runs **Fedora**.
Propellor Boy pastes `curl … | sudo bash` from strangers. The Scribble is malware, broken
configs and `rm -rf`.

## Curriculum

| Level | Lessons |
|---|---|
| **1 · Desktop** | A What Linux is · B Booting it (live USB, VM, installing each distro) · C Desktops (GNOME, KDE, Cinnamon) · D Software the easy way (app stores, Flatpak) · E Everything is a file (the folder layout) · F First steps in the terminal |
| **2 · Terminal** | G Moving files · H Help (man, --help) · I Inside files (cat, less, nano) · J Joining commands (pipes, redirects, grep) · K Permissions, users, sudo · L Package managers (apt, dnf, pacman, AUR) · M Updates, rolling vs fixed releases · N Processes |
| **3 · Power user** | O The shell (aliases, PATH, .bashrc) · P Shell scripts · Q Scheduled jobs (cron, systemd timers) · R Remote (SSH, keys, rsync) · S Services (systemctl, journalctl) · T Networking (ip, DNS, ss, nmcli, ufw/firewalld) · U Disks (lsblk, df, mount, fstab) |
| **4 · Admin** | V Hardening (SSH, fail2ban, updates) · W A home web server · X Backups and snapshots (rsync, Timeshift) · Y Rescue (boot problems, live-USB recovery) · Z Final project: a home server from scratch |

Lesson B recommends practising in a virtual machine so he can try all three families safely.

## Lesson template

Same six sections as the main course: **What went wrong**, **The Operator says**,
**The Mender's way**, **Do it now**, **Quiz** (3 questions), **Scribble watch**.
Front matter adds `level: 1–4`. Commands go in ```` ```bash ```` blocks; the prompt is
not included in copyable commands.

## Technical design

- Source: `linux/<LETTER>-<slug>.md`, built to `site/linux/`. Main course stays at the site root (URLs unchanged).
- `build.py` builds each course from a `Course` config: source dir, output dir, title,
  intro, platform names, whether platform groups render as tabs, level names.
- Platform groups: main course → side-by-side grid (Windows / Android, as now).
  Linux → tabs (Debian / Fedora / Arch). Without JavaScript and in print, all three show stacked.
  The chosen distro is remembered in `localStorage` (try/catch) and applied on every page.
- Lesson parser ignores `## ` lines inside fenced code blocks.
- Pages under `site/linux/` reference shared assets with `../` (style, script, images).
- Main index links to the Linux course; Linux index groups cards by level.
- Linux handbook: `site/linux/handbook.html` → `linux-handbook.pdf`.
- `check_site.py` checks both courses (26 lessons each) and all links.

## Testing

Unit tests for: fenced-code-safe parsing, `level` front matter, tab rendering, nested
output paths. Build + link check for both courses. Visual check at desktop and phone width.

## Out of scope

openSUSE, other families; security tooling beyond hardening basics; development topics.
