---
letter: X
title: Backups and Snapshots
level: 4
image: clink
---

## What went wrong

*Otic's desk. A shiny external drive sits next to his laptop, still in its box.*

**Otic:** I've made a backup! Every night, my files copy to... *(he checks)* ...a folder called `backup`. In my home folder.

**Psych:** On the same disk?

**Otic:** It's a *different folder*.

**Psych:** I take snapshots. Arch, by the way. If anything breaks I just roll back. *His laptop makes a noise like a spoon in a blender. The screen goes black.*

**Psych:** Not a problem. I'll restore the snapshot.

**Otic:** Where's the snapshot?

**Psych:** *(slowly)* ...On the disk.

*The laptop makes the noise again, then stops making any noise at all.*

**Otic:** *(the cow on his shirt)* MOOOOO!

## The Operator says

My excuse calendar for today says "cosmic rays". Tomorrow it's "the drive just died", and that one's true every day for somebody.

A backup on the same disk is a copy, not a backup. A snapshot on the same disk is a time machine that's sinking with the ship. And a backup you've never restored is a rumour. I don't care how clever your system is. I care whether you've pulled a file back out of it, this month, and opened it.

## The Mender's way

A **backup** is a copy of your files somewhere else, that you've proved you can get back. A **snapshot** is a quick picture of the system at a moment in time, kept on the same disk, so you can undo a bad change. You want both, for different jobs.

### The 3-2-1 rule

- **3** copies of anything that matters (the original plus two backups),
- on **2** different devices (your computer and an external drive),
- with **1** somewhere else (a drive at a friend's house, or an encrypted online backup).

Fire, theft and a spilt cup of tea take everything in one room.

### A nightly rsync to an external drive

In lesson R you used `rsync` to copy over SSH. It copies to a local drive just as well, and only sends what's changed.

Plug in the drive and find where it's mounted (lesson U):

```bash
lsblk -f
```

Desktops mount it automatically. On Debian, Ubuntu and Mint that's `/media/yourname/LABEL`; on Fedora and Arch it's `/run/media/yourname/LABEL`, where `LABEL` is the drive's name. Give it a simple label, like `BACKUP`.

Create the script `~/.local/bin/drive-backup` (lesson P), using your own path:

```bash
#!/bin/bash
# Copy my home folder to the external drive.
DEST=/media/otic/BACKUP

# Stop if the drive isn't plugged in, or we'd fill the main disk.
if ! mountpoint -q "$DEST"; then
    echo "Backup drive not mounted at $DEST" >&2
    exit 1
fi

rsync -a --delete --exclude='.cache/' "$HOME/" "$DEST/home/"
echo "Backup finished $(date)"
```

What the flags mean:

- `-a` (**archive**): copy folders inside folders, and keep permissions, owners and dates.
- `--delete`: remove files from the backup that you've deleted at home, so it stays a mirror.
- `--exclude='.cache/'`: skip the cache folder, which is junk that rebuilds itself.
- The `/` at the end of `"$HOME/"` means "the contents of", not the folder itself.

`mountpoint -q` quietly checks whether a path is a mounted drive. Without that check, an unplugged drive means rsync fills an empty folder on your main disk.

Make it runnable and try it once by hand:

```bash
chmod +x ~/.local/bin/drive-backup
~/.local/bin/drive-backup
```

### Run it every night

Use a user timer, exactly as in lesson Q. Create `~/.config/systemd/user/drive-backup.service`:

```ini
[Unit]
Description=Back up home to external drive

[Service]
Type=oneshot
ExecStart=%h/.local/bin/drive-backup
```

And `~/.config/systemd/user/drive-backup.timer`:

```ini
[Unit]
Description=Nightly home backup

[Timer]
OnCalendar=*-*-* 01:00
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable --now drive-backup.timer
journalctl --user -u drive-backup.service
```

The last command shows how each run went.

### Restore, and test the restore

A mirror has one weakness: `--delete` copies your mistakes too. Delete a file today and tomorrow night it's gone from the backup. So restore promptly, and keep a second, older copy (the "2" and "1" above).

To restore one file, copy it back, ideally into a new folder first so you don't overwrite anything:

```bash
mkdir ~/restore-test
rsync -a /media/otic/BACKUP/home/Documents/letter.odt ~/restore-test/
```

Then open it. Once a month, restore something at random and check it opens. To check a whole folder matches, `diff -r` compares two folders and prints nothing if they're the same:

```bash
diff -r ~/Documents /media/otic/BACKUP/home/Documents
```

### Snapshots with Timeshift

**Timeshift** takes snapshots of the *system* (programs and settings, not your home folder by default), so a bad update can be undone. It comes with Mint. It has two modes:

- **RSYNC** mode works on any disk. Snapshots are copies, so the first one is big and slow.
- **BTRFS** mode is instant, but only on a **btrfs** disk with Ubuntu-style subvolumes named `@` and `@home`.

### On Debian / Ubuntu / Mint

Mint: open **Timeshift** from the menu; the setup wizard runs. Ubuntu and Debian: `sudo apt install timeshift` first.

### On Fedora

Fedora uses btrfs, but with subvolumes called `root` and `home`, so Timeshift's BTRFS mode won't work. Use `sudo dnf install timeshift` in RSYNC mode, or Fedora's own tool, **snapper**:

```bash
sudo dnf install snapper
sudo snapper -c root create-config /
sudo snapper -c root create --description "before tinkering"
sudo snapper -c root list
```

`-c root` names the setup ("config") you're using. Snapshots appear in `/.snapshots`, where you can copy old files back. Rolling the whole system back takes more setup; see the Fedora documentation.

### On Arch / Manjaro

Manjaro often includes Timeshift. On Arch, try `sudo pacman -S timeshift`; if pacman can't find it, it's in the AUR (lesson L): `yay -S timeshift`. On a btrfs install, **snapper** (`sudo pacman -S snapper`) works as in the Fedora tab.

### Using Timeshift

The command line does the same as the window:

```bash
sudo timeshift --create --comments "before big update"
sudo timeshift --list
sudo timeshift --restore
```

`--restore` asks which snapshot to restore, then reboots.

### What snapshots are not

A snapshot lives on the same disk. If the disk dies, is stolen or is encrypted by ransomware, the snapshots go with it. Snapshots undo *mistakes*. Backups survive *disasters*.

### Back up /etc and your package list

To rebuild a machine quickly, keep its settings (`/etc`) and a list of what you installed. `tar` packs a folder into one file: `-c` create, `-z` compress, `-f` the file name. `sudo` is needed because some of `/etc` is root-only.

```bash
sudo tar -czf /media/otic/BACKUP/etc-$(date +%F).tar.gz /etc
```

### On Debian / Ubuntu / Mint

```bash
apt-mark showmanual > /media/otic/BACKUP/packages.txt
```

### On Fedora

```bash
dnf repoquery --userinstalled --queryformat '%{name}\n' > /run/media/otic/BACKUP/packages.txt
```

### On Arch / Manjaro

```bash
pacman -Qqe > /run/media/otic/BACKUP/packages.txt
```

`-Q` query installed, `-q` names only, `-e` explicitly installed (not pulled in as dependencies). AUR packages are listed too.

## Do it now

1. Label a USB stick or external drive `BACKUP` and plug it in.
2. Create `drive-backup` with your path, run it, and check `ls` shows your files on the drive.
3. Set up the timer and check `systemctl --user list-timers` shows it.
4. Restore one file into `~/restore-test` and open it.
5. Save your package list to the drive.

You've done it when you've opened a restored file and the timer is listed. Unplug the drive afterwards and the next run will safely refuse to start.

## Quiz

```quiz
- q: Otic's nightly backup goes to a folder on the same disk. What's wrong?
  options:
    - Nothing, it's a different folder
    - If the disk dies, the backup dies with it
    - It should be a snapshot instead
  answer: 1
  why: A backup has to be on a different device, and ideally one copy in a different place too. That's the 3-2-1 rule.
- q: Why does the script check mountpoint before running rsync?
  options:
    - To make the copy faster
    - So an unplugged drive doesn't mean filling the main disk
    - Because rsync can't copy to USB drives
  answer: 1
  why: Without the drive, the path is just an empty folder on your main disk, and rsync would copy your whole home folder into it.
- q: Psych's disk has died. Can he restore from his Timeshift snapshots?
  options:
    - Yes, that's what snapshots are for
    - Only in BTRFS mode
    - No, they were on the same disk
  answer: 2
  why: Snapshots live on the same disk and undo mistakes. Only a backup on another device survives a dead disk.
```

## Scribble watch

The Scribble encrypts every file it can reach, including the backup drive you left plugged in. Then it asks for money. Keep at least one backup unplugged or somewhere else, and check it with a test restore. If ransomware does strike, unplug everything, don't pay, and restore from the copy it couldn't reach.
