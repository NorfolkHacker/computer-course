---
letter: U
title: Disks and Mounting
level: 3
image: ohno
---

## What went wrong

*Psych's shed. Psych has bought a big external hard drive and wants it to appear automatically at boot.*

**Psych:** Forum says add a line to `/etc/fstab`. Easy. Arch, by the way. *He types* `sudo nano /etc/fstab`, *adds* `/dev/sdb1 /mnt/big ext4 defaults 0 2`, *saves, and reboots.*

*Next morning he boots with the drive unplugged.*

```
You are in emergency mode.
Give root password for maintenance
(or press Control-D to continue):
```

**Otic:** *(the cow on his shirt)* MOOOOO!

**Psych:** Not a problem. *He presses Control-D. It comes back. He presses it again. It comes back again.*

*The Scribble, curled up inside the* `fstab` *file, waves.*

## The Operator says

The file `/etc/fstab` has ruined more of my Saturdays than printers. Nearly.

Full disks, sticks that "won't open", drives that vanish after reboot: everyday jobs, all fixable with a handful of commands. Most of this lesson is safe looking. The dangerous bit is `fstab`: the computer reads it at every boot and refuses to carry on if it doesn't like it. Back it up, test it, and never trust a forum.

## The Mender's way

### Disks, partitions, filesystems

- A **disk** is the hardware: SSD, hard drive, USB stick. Linux names them `/dev/sda`, `/dev/sdb` or `/dev/nvme0n1`.
- A disk is split into **partitions**, numbered sections: `/dev/sdb1`, `/dev/nvme0n1p2`.
- Each partition has a **filesystem**, the way files are organised on it. Debian, Ubuntu and Mint use **ext4** by default; Fedora uses **btrfs**; on Arch you chose at install (often ext4). USB sticks usually use **FAT32** or **exFAT**, which Windows reads too.
- **Mounting** attaches a partition to a folder (the **mount point**) so its files appear there.

### Seeing your disks: lsblk

```bash
lsblk
```

```
NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
sda           8:0    1  14.9G  0 disk
└─sda1        8:1    1  14.9G  0 part /run/media/otic/STICK
nvme0n1     259:0    0 476.9G  0 disk
├─nvme0n1p1 259:1    0   600M  0 part /boot/efi
└─nvme0n1p2 259:2    0 476.3G  0 part /
```

`lsblk` lists **bl**oc**k** devices (disks) as a tree. **RM 1** means removable; **SIZE** tells a 16 GB stick from your system disk. Add `-f` to show each filesystem, its label and its **UUID**:

```bash
lsblk -f
```

### UUIDs: names that don't change

`/dev/sdb` might be `/dev/sdc` tomorrow. A **UUID** is a unique ID written into each filesystem when it's made; it never changes. `blkid` shows them (`sudo` so it can read every disk):

```bash
sudo blkid
```

```
/dev/sda1: LABEL="STICK" UUID="4A1F-2B3C" TYPE="exfat"
```

### How full is it? df

```bash
df -h
```

`df` shows **d**isk **f**ree space per mounted filesystem; `-h` gives **h**uman sizes. Check **Use%** for `/`. On Fedora's btrfs, several lines share one pool of space, so show the same numbers.

### What's using the space? du

`du` shows **d**isk **u**sage of folders. `-s` gives one **s**ummary total:

```bash
du -sh ~/Downloads
```

Which folder in your home is biggest (sorted, largest last):

```bash
du -h --max-depth=1 ~ | sort -h
```

`--max-depth=1` stops it listing every folder inside every folder; `sort -h` understands sizes like `4.2G`.

### ncdu: the friendlier way

**ncdu** shows the same thing as a list you can move around with the arrow keys:

### On Debian / Ubuntu / Mint

```bash
sudo apt install ncdu
```

### On Fedora

```bash
sudo dnf install ncdu
```

### On Arch / Manjaro

```bash
sudo pacman -S ncdu
```

### Using ncdu

```bash
ncdu ~
```

<kbd>Enter</kbd> opens a folder, <kbd>←</kbd> goes back, <kbd>q</kbd> quits. <kbd>d</kbd> deletes, so be careful.

### Mounting a USB stick by hand

Your desktop mounts sticks for you (at `/media/YOURNAME/LABEL` on Debian, Ubuntu and Mint; `/run/media/YOURNAME/LABEL` on Fedora and Arch). On a server, you do it by hand.

1. Plug in the stick and run `lsblk`. Find it by size and **RM 1**; say it's `sda1`. **Check twice.**
2. If the desktop has already mounted it, unmount it (`umount`, no "n"):

```bash
sudo umount /dev/sda1
```

3. Make a mount point. `/mnt` is the traditional place for temporary mounts:

```bash
sudo mkdir -p /mnt/usb
```

4. Mount it. For a FAT32 or exFAT stick, the `uid` and `gid` options make the files yours rather than root's (`id -u` and `id -g` print your user and group numbers):

```bash
sudo mount -o uid=$(id -u),gid=$(id -g) /dev/sda1 /mnt/usb
```

For an ext4 stick, leave out `-o` and everything after it up to the device.

5. Look: `ls /mnt/usb`
6. Leave the folder (`cd ~`), then unmount before unplugging, so everything is written:

```bash
sudo umount /mnt/usb
```

**target is busy** means something is still inside the folder. Close it and retry.

### Permanent mounts: /etc/fstab

`/etc/fstab` (**f**ile**s**ystem **tab**le) lists what to mount at boot. Each line has six fields:

```
UUID=4A1F-2B3C  /mnt/usb  exfat  defaults,nofail,uid=1000,gid=1000  0  0
```

| Field | Meaning |
|---|---|
| `UUID=...` | which filesystem (use the UUID, never `/dev/sdb1`) |
| `/mnt/usb` | where to mount it |
| `exfat` | the filesystem type |
| `defaults,nofail,...` | options; **`nofail`** means "if it's missing, carry on booting" |
| `0` | old backup setting; leave at 0 |
| `0` | check order at boot: `1` for `/`, `2` for other ext4, `0` for none |

Psych made two mistakes: `/dev/sdb1` instead of a UUID, and no `nofail`, so a missing drive stopped the boot.

**Warning. A mistake in this file can stop your computer booting.** Practise in a VM. Every time:

1. Back it up: `sudo cp /etc/fstab /etc/fstab.bak`
2. Edit with `sudo nano /etc/fstab`. Add your line at the bottom; don't change the existing lines (Fedora's include btrfs options like `subvol=`, which it needs).
3. Tell systemd the file changed: `sudo systemctl daemon-reload`
4. Test it **before** rebooting: `sudo mount -a` mounts everything listed. Any error here would have been a boot failure. `sudo findmnt --verify` checks the file too.
5. To undo: `sudo cp /etc/fstab.bak /etc/fstab`

### Disk tools with windows

**GNOME Disks** (**Disks** in the menu on Mint, Ubuntu and Fedora) and **KDE Partition Manager** (KDE desktops) show the same as `lsblk` and can format sticks. Formatting erases the whole device: check the name and size first.

## Do it now

Use a USB stick with nothing on it you need, or a VM. Never the disk your system runs from.

1. Run `lsblk`, `df -h`, and `du -h --max-depth=1 ~ | sort -h`. Note your biggest folder.
2. Install `ncdu` and run `ncdu ~`. Look, don't delete.
3. Plug in the stick. Use `lsblk` to identify it by size and **RM 1**.
4. Unmount it if needed, then mount it by hand at `/mnt/usb` as above.
5. Create a file on it: `touch /mnt/usb/hello.txt` (on an ext4 stick, `sudo touch /mnt/usb/hello.txt`), then `ls /mnt/usb`.
6. `cd ~`, then `sudo umount /mnt/usb`. Check with `lsblk` that it has no mount point.
7. Optional, **in a VM only**: follow the five fstab steps above for the stick, then restore the backup.

You've done it when you've mounted and unmounted the stick by hand and `hello.txt` is on it. Delete it afterwards if you like.

## Quiz

```quiz
- q: Psych's computer went into emergency mode when his external drive was unplugged. What would have prevented it?
  options:
    - Using the UUID and adding nofail to the fstab line
    - Rebooting twice
    - Pressing Control-D more firmly
  answer: 0
  why: nofail tells the boot to carry on if the drive is missing, and a UUID always points at the right filesystem.
- q: Which command shows what's using the most space in your home folder?
  options:
    - df -h
    - du -h --max-depth=1 ~ | sort -h
    - lsblk
  answer: 1
  why: du measures folders. df shows how full each whole filesystem is, and lsblk lists disks.
- q: You've edited /etc/fstab. What do you do before rebooting?
  options:
    - Nothing, reboot to see if it works
    - Delete the backup
    - Run sudo mount -a to test it
  answer: 2
  why: mount -a tries every line now. An error here is one you can fix, instead of a computer that won't boot.
```

## Scribble watch

The Scribble's favourite trick is a full disk. When `/` reaches 100%, updates fail, programs crash and you can't save anything. Run `df -h` once a month. If **Use%** on `/` is over 90%, run `ncdu` to find the culprit: usually old downloads, videos, or a runaway log file.
