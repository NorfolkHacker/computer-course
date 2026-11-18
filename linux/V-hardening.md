---
letter: V
title: Hardening
level: 4
image: psych-smash
---

## What went wrong

*Psych's flat. A small grey server hums on the shelf.*

**Psych:** My server's on the network now. Arch, by the way. I'm turning off password logins so nobody can guess their way in.

**Otic:** Have you put your key on it first?

**Psych:** Keys are for people who can't remember passwords. *He sets* `PasswordAuthentication no`*, restarts SSH, and closes the terminal.*

*He opens a new terminal and types* `ssh psych@server`. *The screen says:* `Permission denied (publickey).`

**Otic:** So... you've locked the door with the key on the inside.

**Psych:** Not a problem. *He picks up the Whudonk Stick and walks towards the grey box.*

**Otic:** *(the cow on his shirt)* MOOOOO!

## The Operator says

Luser list, entry 4,112: locked himself out of his own server, then tried to log in harder.

Rule one: never shut the door you're standing behind. Rule two: the internet is full of robots trying `root` and `password123` on every address, all day. A machine on a network gets knocked on within minutes. Hardening makes every knock pointless. It isn't clever; it's a checklist. Do it with a second session open and you'll never need a mallet.

## The Mender's way

**Hardening** means removing the easy ways in.

### Automatic security updates

Most break-ins use holes fixed months ago on machines nobody updated (lesson M). On a server, let security fixes install themselves.

### On Debian / Ubuntu / Mint

The tool is **unattended-upgrades**. Ubuntu has it switched on already; Debian may not.

```bash
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

Answer **Yes**. It installs security updates only. On a Mint desktop, **Update Manager** → **Edit** → **Preferences** → **Automation** does a similar job (it installs all updates, not only security ones).

### On Fedora

The tool is dnf's **automatic** plugin. On Fedora 41 and later (dnf5), its package is `dnf5-plugin-automatic` (the older `dnf-automatic` package is for dnf4). Install it and copy its example settings into place:

```bash
sudo dnf install dnf5-plugin-automatic
sudo cp /usr/share/dnf5/dnf5-plugins/automatic.conf /etc/dnf/automatic.conf
sudo nano /etc/dnf/automatic.conf
```

(If the first file isn't there, `rpm -ql dnf5-plugin-automatic | grep conf` shows where your version keeps it.)

Under `[commands]`, set `apply_updates = yes`, save, and switch on the timer:

```bash
sudo systemctl enable --now dnf5-automatic.timer
```

On RHEL, Rocky and Alma 9 the timer is `dnf-automatic.timer`.

### On Arch / Manjaro

Arch has no automatic updates, on purpose: a rolling release sometimes needs a human to read a note first. Once a week, read the news on `archlinux.org` (Manjaro: the announcements on `forum.manjaro.org`), then run `sudo pacman -Syu` and read what it prints.

### Lock down SSH

Lesson R set up key login. Now switch passwords off. **First, open two SSH sessions to the server and leave one alone.** That spare session stays logged in even if you break the settings, so you can undo them.

Check your key works: `ssh you@server` should log you in without asking for your account password (it may ask for the key's passphrase).

Settings live in `/etc/ssh/sshd_config`. Current distros also read extra files from `/etc/ssh/sshd_config.d/`, if the main file has an `Include /etc/ssh/sshd_config.d/*.conf` line near the top (check with `grep Include /etc/ssh/sshd_config`). If it's there, create a **drop-in** (a small extra settings file) rather than editing the main file. SSH keeps the *first* value it reads, and reads drop-ins in alphabetical order, so start the name with `00`:

```bash
sudo nano /etc/ssh/sshd_config.d/00-hardening.conf
```

```
PasswordAuthentication no
KbdInteractiveAuthentication no
PermitRootLogin no
```

`PermitRootLogin no` stops anyone logging in directly as root; you log in as yourself and use `sudo` (lesson K). No `Include` line? Put the same three lines at the top of `/etc/ssh/sshd_config`.

Now test the settings. `sshd -t` prints nothing if they're fine, and an error with a line number if not:

```bash
sudo sshd -t
```

Then restart the service (lesson S). It's `ssh` on Debian, Ubuntu and Mint, `sshd` on Fedora and Arch. Open sessions survive a restart.

```bash
sudo systemctl restart ssh
```

From your PC, open a **third** session with `ssh you@server`; it should work. Then prove passwords are refused:

```bash
ssh -o PubkeyAuthentication=no you@server
```

That should say `Permission denied`. Only now close the spare session. If the third session failed, use the spare one to delete the drop-in and restart SSH.

### Firewall: deny by default

On a server, block everything coming in, then allow only what you use (lesson T). For now, that's SSH. Keep your spare session open.

### On Debian / Ubuntu / Mint

On plain Debian, install ufw first: `sudo apt install ufw`.

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw enable
sudo ufw status verbose
```

### On Fedora

firewalld already denies by default, but some zones allow more than you'd guess (Fedora Workstation's allows high ports). List what's open and remove anything you don't use, for example:

```bash
sudo firewall-cmd --list-all
sudo firewall-cmd --permanent --remove-service=cockpit
sudo firewall-cmd --reload
```

Never remove `ssh` while you're connected over SSH.

### On Arch / Manjaro

There's no firewall until you add one. Install `ufw` as in lesson T, run the same commands as the Debian tab, then `sudo systemctl enable --now ufw` so it starts at boot.

### fail2ban: ban the guessers

**fail2ban** blocks any address that fails to log in too often.

### On Debian / Ubuntu / Mint

```bash
sudo apt install fail2ban python3-systemd
```

### On Fedora

```bash
sudo dnf install fail2ban
```

### On Arch / Manjaro

```bash
sudo pacman -S fail2ban
```

If you use ufw, add `banaction = ufw` under `[DEFAULT]` in the file below.

### Switch on the SSH jail

A **jail** is fail2ban's name for one set of rules. Don't edit `jail.conf` (updates overwrite it); put your settings in `jail.local`:

```bash
sudo nano /etc/fail2ban/jail.local
```

```ini
[DEFAULT]
backend = systemd
bantime = 1h
maxretry = 5

[sshd]
enabled = true
```

`backend = systemd` makes it read the journal. Fedora, Arch and a fresh Debian have no plain-text login log, so this works everywhere. Then:

```bash
sudo systemctl enable --now fail2ban
sudo fail2ban-client status sshd
```

Banned yourself? From another machine: `sudo fail2ban-client set sshd unbanip 192.168.1.20` (your address).

### Who's been in?

`who` lists who is logged in now; `last -n 10` lists the last ten logins. Debian 13 no longer includes `last`: install it with `sudo apt install wtmpdb libpam-wtmpdb` (it only records logins from then on), or use the journal. The SSH log shows every attempt; use `-u sshd` on Fedora and Arch:

```bash
sudo journalctl -u ssh --since today | grep -E "Accepted|Failed|Invalid"
```

`Accepted publickey` is a good login; `Invalid user` and `Failed` are knocks. Debian-family systems with **rsyslog** also keep `/var/log/auth.log`.

### SELinux on Fedora

Fedora runs **SELinux**, extra rules limiting what each service may touch, even as root: a broken-into web server still can't read your home folder. `getenforce` should say `Enforcing`. When it blocks something, fix the label (lesson W shows how); never switch it off.

### Least privilege

Give every person and program the smallest power that does the job. Don't add people to `sudo` or `wheel` "just in case". Uninstall services you don't use: no service, no hole.

## Do it now

Use a server **in your virtual machine** (lesson B), reached from your PC with a key (lesson R).

1. Open two SSH sessions. Leave one alone.
2. Add the SSH drop-in, run `sudo sshd -t`, and restart SSH.
3. Open a third session with your key; confirm `ssh -o PubkeyAuthentication=no you@server` is refused.
4. Set up the firewall and the fail2ban `sshd` jail.
5. Run `sudo fail2ban-client status sshd` and `last -n 10`.

**To undo:** `sudo rm /etc/ssh/sshd_config.d/00-hardening.conf` and restart SSH. Locked out? Log in at the VM's own window and do the same.

You've done it when key login works, password login is refused, and the `sshd` jail is listed.

## Quiz

```quiz
- q: You're about to set PasswordAuthentication no. What must you do first?
  options:
    - Close all your SSH sessions so the change applies
    - Check key login works, and keep a second session open
    - Restart the server
  answer: 1
  why: A spare session stays logged in, so if key login fails you can undo the change instead of being locked out like Psych.
- q: Which command checks the SSH settings for mistakes before you restart?
  options:
    - sudo sshd -t
    - sudo systemctl status ssh
    - ssh -v
  answer: 0
  why: "sshd -t tests the configuration and prints nothing if it's valid. Restarting with a broken file can stop SSH starting at all."
- q: SELinux on Fedora blocks your web server from reading a folder. What should you do?
  options:
    - Turn it off with setenforce 0
    - Leave it enforcing and fix the folder's label
    - Uninstall it
  answer: 1
  why: SELinux is protecting you. Fix the label that's wrong and keep getenforce saying Enforcing.
```

## Scribble watch

The Scribble posts a helpful tip: "fail2ban keeps banning you? Just set `PermitRootLogin yes` and `PasswordAuthentication yes` and it all works." It does all work, for everyone, including the robots. If you're banned, unban your address with `fail2ban-client set sshd unbanip`, fix your key, and keep passwords off.
