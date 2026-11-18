---
letter: R
title: Remote Control with SSH
level: 3
image: whoosh
---

## What went wrong

*Two rooms. Otic is in the kitchen with his Mint laptop. Psych is in the shed with his Arch machine.*

**Otic:** Can you look at my laptop? Something's wrong with it.

**Psych:** From here. With SSH. *He types* `ssh otic@otic-laptop`.

```
ssh: connect to host otic-laptop port 22: Connection refused
```

*He tries an address he found online instead. A message appears:* `The authenticity of host can't be established. Are you sure you want to continue connecting (yes/no/[fingerprint])?`

**Otic:** *(the cow on his shirt, from the kitchen)* MOOOOO!

**Psych:** Yes. Always yes. *He types* `yes`, *then Otic's password, into a machine in another country.*

*Somewhere, the Scribble says "thank you".*

## The Operator says

Luser list, entry 233: typed his password into a computer he'd never met, because it asked nicely.

SSH is how I do my job without leaving my chair. It's encrypted, it's on every Linux machine, and with keys you'll never type a password again. But it's the front door, and the first-connection question is how you check whose door you're knocking on. "Yes. Always yes" is how people end up in my excuse calendar.

## The Mender's way

**SSH** (Secure SHell) opens an encrypted terminal on another computer over the network. You need an **SSH server** on the machine you want to reach, and an **SSH client** on the one you're sitting at. Every Linux desktop has the client.

### Installing and starting the server

On the machine you want to connect *to*:

### On Debian / Ubuntu / Mint

```bash
sudo apt install openssh-server
```

It starts by itself. The service is called `ssh`. On Ubuntu (24.04 and later) and Mint 22 and later, `systemctl status ssh` may say "inactive" until someone connects; that's normal, it wakes up on demand.

### On Fedora

```bash
sudo dnf install openssh-server
sudo systemctl enable --now sshd
```

The service is called `sshd`. Fedora Workstation's firewall already allows SSH.

### On Arch / Manjaro

```bash
sudo pacman -S openssh
sudo systemctl enable --now sshd
```

The package is `openssh` (client and server together). The service is `sshd`.

### Finding the address

Each computer on your home network has an **IP address**, a number like `192.168.1.50`. On the server, run:

```bash
ip a
```

`ip a` (short for `ip address`) lists network connections. Ignore `lo` (the computer talking to itself). Find the `inet` line under your Wi-Fi or wired connection:

```
inet 192.168.1.50/24 brd 192.168.1.255 scope global dynamic wlp2s0
```

The address is the part before the `/`. Lesson T explains networking properly.

### Connecting

From the other machine:

```bash
ssh otic@192.168.1.50
```

That's the user name on the *server*, then `@`, then its address. The first time, you'll see:

```
The authenticity of host '192.168.1.50' can't be established.
ED25519 key fingerprint is SHA256:Xq3v...
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

The **fingerprint** is the server's unique ID. To check it's really your machine, run this on the server itself and compare:

```bash
ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```

If they match, type `yes`; it's remembered in `~/.ssh/known_hosts`. If the fingerprint ever changes unexpectedly, SSH shows a loud warning: stop and find out why.

Type the user's password. You now have a terminal on the other computer. `exit` (or <kbd>Ctrl</kbd> + <kbd>D</kbd>) brings you back.

### SSH keys: no more passwords

An **SSH key** is a pair of files: a **private key** that stays on your computer and is never shared, and a **public key** you give to servers. The server lets in whoever holds the matching private key. Safer than a password, and quicker.

1. On the machine you sit at, make a key pair:

```bash
ssh-keygen -t ed25519 -C "otic laptop"
```

`-t ed25519` picks the modern key type; `-C` adds a label. Press <kbd>Enter</kbd> to accept the location. Enter a **passphrase** (a password for the key itself) when asked; it protects the key if your laptop is stolen.

2. Copy the public key to the server:

```bash
ssh-copy-id otic@192.168.1.50
```

3. Connect again with `ssh otic@192.168.1.50`. It asks for the key's passphrase (or nothing, if your desktop remembers it), not the server's password.

The private key is `~/.ssh/id_ed25519`. The public one ends in `.pub`. Only ever copy the `.pub` file anywhere.

### Shortcuts in ~/.ssh/config

Create `~/.ssh/config` with nano:

```
Host mint
    HostName 192.168.1.50
    User otic

Host vm
    HostName 127.0.0.1
    Port 2222
    User otic
```

Now `ssh mint` does the same as `ssh otic@192.168.1.50`.

### Copying files: scp and rsync

**scp** copies files over SSH, like `cp` with an address:

```bash
scp notes.txt mint:/home/otic/
scp mint:/home/otic/photo.jpg .
```

**rsync** only copies what has changed. It must be installed on both machines (package `rsync` everywhere).

```bash
rsync -avh --dry-run ~/Music/ mint:/home/otic/Music/
```

- `-a` **archive**: copy folders inside folders, and keep dates and permissions.
- `-v` **verbose**: list each file.
- `-h` **human**: sizes in KB and MB.
- `--dry-run`: show what *would* happen, without copying. Remove it once the list looks right.

**The trailing slash matters.** `~/Music/` means "the contents of Music". `~/Music` (no slash) means "the Music folder itself", so you'd end up with `Music/Music`. Always check with `--dry-run` first.

### Connecting from Windows

Windows 11 has an SSH client built in. Open **Terminal** (right-click **Start** › **Terminal**) and use the same commands: `ssh otic@192.168.1.50`, `ssh-keygen -t ed25519`. Windows has no `ssh-copy-id`; instead, run this in PowerShell to send your public key:

```powershell
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh otic@192.168.1.50 "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

### Reaching a virtual machine

VirtualBox VMs use **NAT** by default, which hides them from your network. Two fixes (shut the VM down, then open its **Settings** › **Network**):

- **Bridged Adapter**: set **Attached to** to **Bridged Adapter**. The VM gets its own address on your home network. Simplest, but some workplace networks block it.
- **Port forwarding**: keep **NAT**, open **Port Forwarding** (you may need to switch the settings window to **Expert** mode and open **Advanced** to see it) and add a rule: **Host Port** `2222`, **Guest Port** `22`. Then connect with `ssh -p 2222 otic@127.0.0.1`.

## Do it now

Use your VM, or a second Linux machine. If you have only one, connect to yourself with `localhost`, which always means "this computer".

1. Install and start the SSH server for your family (above).
2. On the server, run `ip a` and note the address.
3. Connect: `ssh YOURNAME@ADDRESS` (or `ssh YOURNAME@localhost`). Check the fingerprint, type `yes`, then your password. Type `exit`.
4. Make a key with `ssh-keygen -t ed25519` and copy it with `ssh-copy-id`.
5. Add a `Host` shortcut to `~/.ssh/config` and connect using just its name.
6. Make a test folder and try rsync: `mkdir -p ~/rtest && touch ~/rtest/a ~/rtest/b`, then `rsync -avh --dry-run ~/rtest/ YOURHOST:/tmp/rtest/`.

You've done it when `ssh` plus your shortcut name logs in without asking for the account password. Tidy up with `rm -r ~/rtest`.

## Quiz

```quiz
- q: Psych got "Connection refused" connecting to Otic's laptop. What's the most likely reason?
  options:
    - Otic's laptop has no SSH server running
    - Psych used the wrong password
    - SSH only works on Arch
  answer: 0
  why: Connection refused means nothing is listening on port 22. Install and start the SSH server on the machine you're connecting to.
- q: What should you do at the first-connection fingerprint question?
  options:
    - Always type yes
    - Compare the fingerprint with the one shown on the server, then type yes
    - Type your password
  answer: 1
  why: The fingerprint proves which machine you're talking to. Check it before you trust it.
- q: "What does rsync -avh ~/Music/ mint:/home/otic/Music/ copy?"
  options:
    - The Music folder itself, into a new Music/Music folder
    - Only files that are newer on the server
    - The contents of Music, into the Music folder on mint
  answer: 2
  why: A trailing slash on the source means "its contents". Without it, rsync copies the folder itself inside the destination.
```

## Scribble watch

The Scribble wants your private key: the file `~/.ssh/id_ed25519` with no `.pub` on the end. Anyone who has it can log in wherever your public key is installed. Never email it, paste it into a chat, or copy it to a server. If you think it's leaked, make a new key pair and remove the old public key from each server's `~/.ssh/authorized_keys`.
