---
letter: K
title: Permissions and Users
level: 2
image: propellor-boy
---

## What went wrong

*The woods. Propellor Boy and Unicorn Boy sit at a laptop. Psych and Otic watch from a log.*

**Unicorn Boy:** My script says `Permission denied`.

**Propellor Boy:** A forum says fix it with this. *He types* `sudo chmod -R 777 /` *and presses Enter.*

**Propellor Boy:** Everybody can do everything now. Nothing can be denied ever again.

*The laptop churns for a long time. Unicorn Boy types* `sudo ls`. *The answer comes back:* `sudo: /usr/bin/sudo must be owned by uid 0 and have the setuid bit set`.

**Unicorn Boy:** What does that mean?

**Propellor Boy:** It means it's working.

**Psych:** Amateurs. On Arch I just log in as root all the time. Saves typing sudo. I use Arch, by the way.

*A tangle of Scribble slides out of a forum tab and makes itself at home.*

**Otic's shirt:** MOOOOO!

*The propellor begins to spin. WHOOSH.*

## The Operator says

Luser list, special section: people who solved a permissions problem by giving everyone permission to everything. I keep it in a file with mode 600. Nobody else gets to read it, which is rather the point.

Permissions are how Linux keeps your files private and stops one bad click wrecking the whole machine. Learn to read them and `Permission denied` stops being a wall and becomes a sign telling you exactly which door is locked.

## The Mender's way

Every file has an owner, a group and three sets of rules. Read them, and you can fix them properly.

### Users, groups and root

A **user** is an account: a name, a password and a home folder. A **group** is a named set of users who share access to things. Every file belongs to one user and one group.

**root** is the built-in all-powerful administrator account. It can read, change and delete anything, so a mistake as root has no safety net.

`id` shows who you are and which groups you're in:

```bash
id
```

```
uid=1000(otic) gid=1000(otic) groups=1000(otic),27(sudo)
```

`uid` is your user number and `groups` lists every group you're in. Yours will differ.

### Reading ls -l

```bash
cd ~/practice
touch secret.txt
ls -l secret.txt
```

```
-rw-r--r-- 1 otic otic 0 Nov 18 10:00 secret.txt
```

The first ten characters are the permissions:

| Characters | Here | Means |
|---|---|---|
| 1st | `-` | type: `-` file, `d` directory, `l` link |
| 2nd–4th | `rw-` | the **user** (owner): read, write, no execute |
| 5th–7th | `r--` | the **group**: read only |
| 8th–10th | `r--` | **others** (everyone else): read only |

`r` is **read**, `w` is **write** (change), `x` is **execute** (run it as a program; for a folder, go into it). A `-` means that permission is off. Then come a link count (ignore it), the owner, the group, the size, the date and the name.

### chmod: change permissions

`chmod` (**change mode**) has two styles. The **symbolic** style uses letters: `u` user, `g` group, `o` others, `a` all; `+` adds, `-` removes.

```bash
chmod o-r secret.txt
chmod u+x myscript.sh
```

The first stops others reading `secret.txt`. The second lets you run `myscript.sh`.

The **numeric** style sets everything at once with three digits (user, group, others). Each digit adds up: read = 4, write = 2, execute = 1.

| Number | Letters | Typical use |
|---|---|---|
| `644` | `rw-r--r--` | ordinary files: you edit, others read |
| `755` | `rwxr-xr-x` | programs and folders: you change, others run or enter |
| `600` | `rw-------` | private files: only you |

```bash
chmod 600 secret.txt
```

**Never use 777** (`rwxrwxrwx`). It lets every user and program change or replace the file: it "fixes" `Permission denied` by switching security off. Some programs (SSH, for one) refuse to work with files that open. Give only the access that's needed.

### chown and chgrp: change owner

`chown` (**change owner**) gives a file to another user, and optionally a group, written `user:group`. `chgrp` changes only the group. Both need `sudo` for files you don't own:

```bash
sudo chown otic:otic somefile.txt
sudo chgrp users somefile.txt
```

### sudo properly

`sudo` runs one command as root, asking for **your** password, if you're in the admin group. `su` (**switch user**) makes you root completely, using **root's** password (Ubuntu and Mint lock it, so `su` doesn't work there). Prefer `sudo`: one command at a time, and logged. For a root shell, `sudo -i`; type `exit` to leave.

Which group gives admin rights depends on the family:

### On Debian / Ubuntu / Mint

The group is called `sudo`. The user made during installation is already in it. (On plain Debian, if you set a root password while installing, your user isn't; add it as below.) To give another user admin rights:

```bash
sudo usermod -aG sudo username
```

### On Fedora

The group is called `wheel`. The first user you create while setting Fedora up is an administrator, so it's already in it (if the installer asks, tick **Make this user administrator**). To add another user:

```bash
sudo usermod -aG wheel username
```

### On Arch / Manjaro

The group is `wheel`. Manjaro sets this up for you. On Arch you may need to do it yourself, as root (log in as root, or use `su -`):

```bash
pacman -S sudo
usermod -aG wheel username
EDITOR=nano visudo
```

`visudo` edits the sudo settings safely: it refuses to save a broken file. Find this line, delete the `#` and space at the start, then save and exit (lesson I):

```
# %wheel ALL=(ALL:ALL) ALL
```

### After changing groups

`usermod -aG` means **a**ppend this user to the **G**roup. Never leave out `-a`: without it, the user is removed from every other group. The new group only takes effect after the user logs out and back in.

### Adding users and passwords

On Debian, Ubuntu and Mint, `adduser` is a friendly helper: it makes the home folder and asks for a password.

```bash
sudo adduser alice
```

On Fedora and Arch, use `useradd`, then set a password (Fedora's `adduser` is just another name for `useradd`):

```bash
sudo useradd -m alice
sudo passwd alice
```

`-m` makes the home folder. `passwd` on its own changes **your** password; with `sudo` and a name, someone else's. To give the new user admin rights, add them to the admin group as above. To remove a test user and their home folder: `sudo deluser --remove-home alice` (Debian family) or `sudo userdel -r alice` (Fedora, Arch).

## Do it now

All in `~/practice`. Nothing outside it changes.

1. Run `id`. Find whether you're in `sudo` or `wheel`.
2. `cd ~/practice` and make a tiny script:

   ```bash
   echo 'echo "It runs!"' > hello.sh
   ls -l hello.sh
   ```
3. Try to run it: `./hello.sh` (`./` means "in this folder"). You get `Permission denied`: there's no `x`.
4. Add execute for you only: `chmod u+x hello.sh`, then `ls -l hello.sh` and `./hello.sh` again.
5. Try `chmod 700 hello.sh`, then `chmod 755 hello.sh`, reading `ls -l` after each.
6. Make `secret.txt` private: `chmod 600 secret.txt`, and check it reads `-rw-------`.

You've done it when `./hello.sh` prints `It runs!` and you can read every letter of `-rwxr-xr-x` out loud.

## Quiz

```quiz
- q: What does -rw-r----- mean?
  options:
    - Everyone can read and write it
    - The owner can read and write, the group can read, others get nothing
    - Only root can open it
  answer: 1
  why: Read it in threes after the first character. rw- for the user, r-- for the group, --- for others.
- q: A script says Permission denied when you run it. What's the right fix?
  options:
    - "sudo chmod -R 777 /"
    - "chmod u+x script.sh"
    - Log in as root for everything
  answer: 1
  why: The script needs execute permission for you, nothing more. 777 and living as root throw away your safety net.
- q: Which group gives admin (sudo) rights on Fedora and Arch?
  options:
    - sudo
    - wheel
    - root
  answer: 1
  why: Fedora and Arch use wheel. The Debian family (Ubuntu, Mint) uses a group called sudo.
```

## Scribble watch

The Scribble loves instructions that say "give everything 777" or "just run it all as root". Both open the door to anything nasty. When you hit `Permission denied`, use `ls -l` to see who owns the file and what's allowed, then change just that. Never `chmod 777`, and never `chmod -R` anything outside your home folder.
