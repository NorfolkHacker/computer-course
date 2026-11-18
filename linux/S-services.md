---
letter: S
title: Services
level: 3
image: whudonk
---

## What went wrong

*Psych's shed. Psych has installed a web server on his Arch machine. He opens a browser and visits his own address. Nothing.*

**Psych:** I installed Apache. It's not serving.

**Otic:** On my Mint laptop it just started by itself.

**Psych:** Then mine's broken. *He types* `sudo systemctl start apache2`.

```
Failed to start apache2.service: Unit apache2.service not found.
```

**Otic:** *(the cow on his shirt)* MOOOOO!

**Psych:** Not a problem. *He reboots. Nothing. He reboots again. Nothing. He raises the Whudonk Stick over the tower.*

*The Mender, passing, types* `systemctl status httpd` *and points at the word* `disabled`.

*WHUDONK! The Stick lands on the desk, narrowly missing the tower.*

## The Operator says

When a user says "it's not working", I ask three questions. Is it running? Is it switched on at boot? What did it say in the log? Nobody ever knows. That's why I have a log.

A **service** is a program that runs in the background: the SSH server, the web server, cron. On a server, services are the whole point. Two commands let you check, start, stop and investigate every one of them: `systemctl` and `journalctl`. Learn them, and you can answer my three questions before you ring me. You won't need to ring me at all.

## The Mender's way

Fedora, Debian, Ubuntu, Mint and Arch all use **systemd** to start the computer and look after its services.

### Units and services

systemd manages **units**: things it can start and stop. A unit is described by a small text file. The kind you'll use most is a **service** (file names end in `.service`). You met another kind, the **timer**, in lesson Q. When you type a service name, you can usually leave off `.service`.

### Is it running?

```bash
systemctl status sshd
```

(`ssh` on Debian, Ubuntu and Mint; see the names table below.) The important lines:

```
● sshd.service - OpenSSH server daemon
     Loaded: loaded (/usr/lib/systemd/system/sshd.service; enabled; preset: disabled)
     Active: active (running) since Tue 2026-11-17 09:14:02 GMT; 1 day ago
```

- **Active: active (running)** means it's running now. **inactive (dead)** means it isn't. **failed** means it crashed.
- On the **Loaded** line, **enabled** means it starts at boot; **disabled** means it doesn't.

Below that are the last few log lines. Press <kbd>q</kbd> if it opens in a scrolling view. `status` doesn't need `sudo`.

### Controlling a service

Changing a service affects the whole system, so these need `sudo`:

| Command | What it does |
|---|---|
| `sudo systemctl start NAME` | start it now |
| `sudo systemctl stop NAME` | stop it now |
| `sudo systemctl restart NAME` | stop it and start it again |
| `sudo systemctl reload NAME` | re-read its settings without stopping (only some services support this) |
| `sudo systemctl enable NAME` | start it at every boot (doesn't start it now) |
| `sudo systemctl disable NAME` | don't start it at boot (doesn't stop it now) |
| `sudo systemctl enable --now NAME` | both: start now and at every boot |

**Running** and **starting at boot** are separate switches. Psych's service was installed but not switched on in either sense.

For a quick yes or no, useful in scripts:

```bash
systemctl is-active sshd
systemctl is-enabled sshd
```

### Finding services

List every running service, or only the broken ones:

```bash
systemctl list-units --type=service
systemctl list-units --type=service --failed
```

An empty failed list is what you want.

### Names and habits differ by family

The same software can have a different package and service name, and families disagree about whether a new service should start by itself.

| Software | Debian / Ubuntu / Mint | Fedora | Arch / Manjaro |
|---|---|---|---|
| SSH server | package `openssh-server`, service `ssh` | `openssh-server`, `sshd` | `openssh`, `sshd` |
| Apache web server | `apache2`, `apache2` | `httpd`, `httpd` | `apache`, `httpd` |
| cron | `cron`, `cron` | `cronie`, `crond` | `cronie`, `cronie` |

### On Debian / Ubuntu / Mint

Installing a package that contains a service usually **starts and enables it straight away**. Convenient, but it means a freshly installed server program is already running and reachable. Check with `systemctl status` after installing.

### On Fedora

Services are installed **switched off**. After installing, run `sudo systemctl enable --now NAME`. Fedora's firewall may also need opening for it (lesson T).

### On Arch / Manjaro

Services are installed **switched off**, and nothing extra is installed for you. After installing, run `sudo systemctl enable --now NAME`.

### Reading the logs: journalctl

systemd keeps one big log, the **journal**. `journalctl` reads it. On its own it shows everything since records began, so narrow it down:

| Command | Shows |
|---|---|
| `journalctl -u NAME` | only messages from that unit |
| `journalctl -f` | new messages as they arrive (**f**ollow); <kbd>Ctrl</kbd> + <kbd>C</kbd> to stop |
| `journalctl -b` | messages since the last **b**oot |
| `journalctl -b -1` | messages from the boot before that |
| `journalctl -p err` | only errors and worse (**p**riority) |
| `journalctl --since "1 hour ago"` | recent messages; also `--since today` or `--since "2026-11-18 09:00"` |
| `journalctl -n 20` | only the last 20 lines |

You can combine them:

```bash
journalctl -u sshd -b -p err
```

That means: SSH server errors since this boot. The journal opens in `less` (lesson I): arrow keys to scroll, <kbd>/</kbd> to search, <kbd>q</kbd> to quit. Add `-e` to jump straight to the end.

If you see a note saying you can't see messages from other users or the system, your account isn't in a log-reading group (`adm` on Debian-family, `wheel` on Fedora and Arch). Put `sudo` in front.

### The three-question habit

When something isn't working:

1. Is it running? `systemctl status NAME`
2. Will it start at boot? Look for **enabled** on the **Loaded** line.
3. What did it say? `journalctl -u NAME -b`

## Do it now

You'll use cron from lesson Q: stopping it for a minute does no harm. Its name differs, so use yours:

### On Debian / Ubuntu / Mint

```bash
systemctl status cron
sudo systemctl stop cron
systemctl is-active cron
sudo systemctl start cron
systemctl is-active cron
systemctl is-enabled cron
journalctl -u cron -n 20
```

### On Fedora

```bash
systemctl status crond
sudo systemctl stop crond
systemctl is-active crond
sudo systemctl start crond
systemctl is-active crond
systemctl is-enabled crond
journalctl -u crond -n 20
```

### On Arch / Manjaro

```bash
systemctl status cronie
sudo systemctl stop cronie
systemctl is-active cronie
sudo systemctl start cronie
systemctl is-active cronie
systemctl is-enabled cronie
journalctl -u cronie -n 20
```

### Then

Finally, run `systemctl list-units --type=service --failed` and `journalctl -b -p err`, and read what's there. A few errors at boot are normal on most machines.

You've done it when `is-active` said `inactive` after stopping, `active` after starting, and `is-enabled` says `enabled`. If cron is left stopped, `sudo systemctl start` it again.

## Quiz

```quiz
- q: Psych installed Apache on Arch, but it isn't running. What should he type?
  options:
    - sudo systemctl start apache2
    - sudo systemctl enable --now httpd
    - sudo reboot
  answer: 1
  why: On Arch the service is called httpd, and new services start switched off. enable --now starts it now and at every boot.
- q: What's the difference between start and enable?
  options:
    - start runs it now; enable makes it start at every boot
    - They're the same thing
    - enable runs it now; start makes it start at boot
  answer: 0
  why: They're separate switches. enable --now does both at once.
- q: Which command shows only the SSH server's messages since this boot?
  options:
    - journalctl -f
    - systemctl list-units --failed
    - journalctl -u sshd -b
  answer: 2
  why: -u picks the unit and -b limits it to the current boot. On Debian-family the unit is ssh.
```

## Scribble watch

The Scribble loves a forgotten service: something you installed once to try, which Debian-family systems started automatically and which has been listening on the network ever since. Every few months, run `systemctl list-units --type=service` and look for anything you don't recognise or no longer use. If you don't need it, `sudo systemctl disable --now` it, or remove the package.
