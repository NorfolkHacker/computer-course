---
letter: Z
title: The Final Project
level: 4
image: jar
---

## What went wrong

*The woods. Three small servers sit on tree stumps, blinking.*

**Psych:** Done. Arch server, by the way. Took me eleven minutes.

**Otic:** Did you set up the firewall?

**Psych:** Didn't need one.

**Otic:** Backups?

**Psych:** It's brand new. Nothing to back up.

**Otic:** Updates?

**Psych:** It's *brand new*. *He logs in. As root. With the password* `root`.

*A small black scribble crawls out of the ventilation slots and waves at him.*

**Otic:** *(the cow on his shirt)* MOOOOO!

*Psych reaches for the Whudonk Stick. It is already crackling.*

## The Operator says

Final exam. I've marked thousands. Most of them set fire to themselves.

Anyone can install a server in eleven minutes. A server is a promise: it will be there tomorrow, patched, backed up, and not working for someone else. Everything you've learned from A to Y goes into this one box. Build it slowly. Check every step. Then look after it every week, which is the bit nobody does, and the bit that makes you an admin rather than a man with a computer in a cupboard.

## The Mender's way

You'll build a small home server from nothing: a web page, SSH, a firewall, automatic updates and nightly backups. Use a **virtual machine** (lesson B), or a spare PC or small single-board computer. In a VM, set the network to **Bridged** so other devices can reach it, and add a second virtual disk for backups.

Each step names the lesson that taught it. If a step feels unfamiliar, go back and reread that lesson.

### 1. Install a server edition

Server editions have no desktop. You work through SSH.

### On Debian / Ubuntu / Mint

Mint has no server edition; use **Debian** or **Ubuntu Server**.

- **Debian netinst**: at **Software selection**, untick the desktop, tick **SSH server** and **standard system utilities**. If you leave the root password blank, your user gets `sudo`.
- **Ubuntu Server**: tick **Install OpenSSH server** when asked. Your user can use `sudo`.

To give another user `sudo` later: `sudo usermod -aG sudo name`.

### On Fedora

Use **Fedora Server**. In the installer, create your user and tick the box that gives it administrative privileges (the wording varies by release; it adds the user to the `wheel` group). SSH is switched on already. So is **Cockpit**, a web admin page on port 9090; remove it from the firewall if you won't use it (lesson V).

### On Arch / Manjaro

Install Arch from the installation guide, or with `archinstall` choosing the **Minimal** profile. Then add the basics and a user (lesson K):

```bash
pacman -S openssh sudo
systemctl enable --now sshd
useradd -m -G wheel name
passwd name
EDITOR=nano visudo
```

In `visudo`, remove the `#` from the line `%wheel ALL=(ALL:ALL) ALL`.

### 2. Give it an address that doesn't change

Your router hands out addresses using **DHCP** (lesson T), and they can change. A server needs to stay put. The simplest way is a **DHCP reservation**: you tell the router "always give this machine the same address".

1. On the server, run `ip link` and note the `link/ether` value on the main network card, for example `52:54:00:ab:cd:ef`. That's its **MAC address**, a fixed hardware name.
2. Log in to your router's admin page (often `http://192.168.1.1`; it's printed on the router).
3. Find **DHCP reservation**, **Address reservation** or **Static lease** (the name varies by router) and reserve an address for that MAC.
4. Reboot the server and check `ip -4 addr` shows the reserved address.

### 3. SSH with keys only (lessons R and V)

From your PC, copy your key with `ssh-copy-id you@192.168.1.50`. Then add the SSH drop-in from lesson V, test with `sudo sshd -t`, restart, and confirm a password login is refused. **Keep a second session open the whole time.**

### 4. Firewall and fail2ban (lessons T and V)

Deny incoming by default; allow SSH and HTTP. Set up the fail2ban `sshd` jail with `backend = systemd`.

### 5. Automatic updates (lessons M and V)

Debian and Ubuntu: `unattended-upgrades`. Fedora: `dnf5-plugin-automatic` with its `dnf5-automatic.timer`. Arch: a weekly reminder to read the news and run `sudo pacman -Syu`.

### 6. A web page (lesson W)

Install nginx, put your own `index.html` in the web folder, run `sudo nginx -t`, reload, and open it from your phone.

### 7. A nightly backup (lessons P, Q, U and X)

Format the second disk and mount it at `/mnt/backup` with a `nofail` line in `/etc/fstab` (lesson U). Then create `/usr/local/bin/server-backup`:

```bash
#!/bin/bash
# Nightly copy of settings, web files and home folders.
DEST=/mnt/backup

if ! mountpoint -q "$DEST"; then
    echo "Backup disk not mounted at $DEST" >&2
    exit 1
fi

rsync -a --delete /etc /srv /home "$DEST/"
echo "Backup finished $(date)"
```

On Debian-family servers, add `/var/www` to the rsync line. This one runs as root, so it's a **system** timer. Make it runnable, and create the two unit files with `sudo nano`:

```bash
sudo chmod +x /usr/local/bin/server-backup
sudo nano /etc/systemd/system/server-backup.service
```

```ini
[Unit]
Description=Nightly server backup

[Service]
Type=oneshot
ExecStart=/usr/local/bin/server-backup
```

And `/etc/systemd/system/server-backup.timer`:

```ini
[Unit]
Description=Run server backup nightly

[Timer]
OnCalendar=*-*-* 03:00
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now server-backup.timer
sudo systemctl start server-backup.service
journalctl -u server-backup.service -n 5
```

The last two run it once now and show the result. Then restore one file into your home folder and check it (lesson X). A second disk in the same box is your "2"; for the "1", copy it to another machine now and then with `rsync` over SSH (lesson R).

### 8. The weekly check

A server you never look at is a server you've lost track of. Once a week, log in and work through this list:

| Check | Command |
|---|---|
| Disk space | `df -h` |
| Failed services | `systemctl --failed` |
| Errors this week | `sudo journalctl -p err --since "7 days ago"` |
| Who's logged in, who's knocking | `last -n 20` (on Debian 13, after installing `wtmpdb`; lesson V) and `sudo fail2ban-client status sshd` |
| Backup ran | `systemctl list-timers` and `journalctl -u server-backup.service -n 5` |
| Updates | Debian/Ubuntu: `less /var/log/unattended-upgrades/unattended-upgrades.log`; Fedora: `journalctl -u dnf5-automatic`; Arch: read the news, then `sudo pacman -Syu` |

Once a month, also restore a random file and open it.

## Do it now

Build the server, then tick off every lesson. Each row is something you can check on your new machine.

| Lesson | Check on your server | Done |
|---|---|---|
| A What Linux is | `cat /etc/os-release` names your distro and family | ☐ |
| B Booting it | The server is installed (VM or real) and starts on its own | ☐ |
| C Desktops | You chose no desktop, and can say why | ☐ |
| D Software the easy way | You can explain why a server uses the package manager, not an app store | ☐ |
| E Everything is a file | You can say what `/etc`, `/var/log` and `/srv` hold | ☐ |
| F First steps in the terminal | You logged in and ran `pwd` and `ls` | ☐ |
| G Moving files | You copied `index.html` into the web folder | ☐ |
| H Help | You read `man rsync` for one flag you use | ☐ |
| I Inside files | You edited a config file with `nano` | ☐ |
| J Joining commands | You piped `journalctl` into `grep` to find failed logins | ☐ |
| K Permissions, users, sudo | Your user has `sudo`; you never log in as root | ☐ |
| L Package managers | You installed nginx and fail2ban with your family's tool | ☐ |
| M Updates | Everything is up to date | ☐ |
| N Processes | You found the nginx processes with `ps aux` and `grep` | ☐ |
| O The shell | You added one useful alias to `~/.bashrc` | ☐ |
| P Shell scripts | `server-backup` runs and checks its disk | ☐ |
| Q Scheduled jobs | `server-backup.timer` appears in `systemctl list-timers` | ☐ |
| R Remote | You log in from your PC with a key | ☐ |
| S Services | nginx, SSH and fail2ban are all `active (running)` | ☐ |
| T Networking | The server has a reserved address; the firewall allows only SSH and HTTP | ☐ |
| U Disks | `/mnt/backup` is in `/etc/fstab` with `nofail` | ☐ |
| V Hardening | Password and root logins are refused; automatic updates or a weekly reminder are set | ☐ |
| W A home web server | Your page loads on your phone | ☐ |
| X Backups and snapshots | You restored a file from `/mnt/backup` and opened it | ☐ |
| Y Rescue | You know your way into the GRUB menu, and have a live USB ready | ☐ |

You've done it when every row is ticked and the server has run for a week with a clean weekly check.

## Quiz

```quiz
- q: Psych's new server is "brand new". What does it still need before he leaves it running?
  options:
    - Nothing until something goes wrong
    - Key-only SSH, a firewall, updates and backups
    - A desktop so he can see it
  answer: 1
  why: A new server is attacked within minutes of being on a network, and backups only help if they exist before the disk dies.
- q: How do you keep a home server on the same address?
  options:
    - Reboot it until it gets the same one
    - Reserve its address on the router using its MAC address
    - Type the address into /etc/hostname
  answer: 1
  why: A DHCP reservation tells the router to always give that MAC address the same IP.
- q: Which command shows services that have failed?
  options:
    - systemctl --failed
    - df -h
    - who
  answer: 0
  why: "systemctl --failed lists any service that crashed or couldn't start. df -h shows disk space and who shows logins."
```

## Scribble watch

A server left alone slowly fills up, falls behind on updates, and stops backing up without telling anyone. That's the Scribble's last trick: waiting. Put the weekly check in your phone's calendar now, and do it.

*The Mender drops the last bit of Scribble into a jar and sets it on top of the server, where it rattles faintly.*

**The Operator:** Your server works. Your backups restore. You didn't paste anything you didn't understand. *(long pause)* Fine. You're an Operator now. Don't make me regret it. And leave that jar where I can see it.
