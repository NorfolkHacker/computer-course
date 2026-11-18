---
letter: Y
title: Rescue
level: 4
image: ohno
---

## What went wrong

*Otic's desk. His Mint laptop is booting. It has been booting for some time.*

**Otic:** It says "A start job is running for dev-disk-by..." with a little timer.

**Psych:** What did you change?

**Otic:** Nothing! I just added my USB drive to `/etc/fstab` so it mounts by itself. Then I unplugged it.

*The screen fills with text and ends:* `You are in emergency mode.`

**Otic:** *(the cow on his shirt)* MOOOOO!

**Psych:** Not a problem. Reinstall. I reinstall Arch every week. By the way. *He raises the Whudonk Stick over the laptop.*

*The Mender gently takes the Stick, sits down, and starts typing.*

## The Operator says

Today's excuse calendar entry: "the bootloader is sulking". It's always sulking. It's a bootloader.

A Linux machine that won't boot is almost never broken. It's one wrong line in one file, and the computer is telling you which one, in red, while you panic. Learn three ways back in and a dead machine is a twenty-minute chore. And if it isn't? You did lesson X. Didn't you.

## The Mender's way

Work from the gentlest fix to the biggest. **Practise all of this in a virtual machine**, and take a VM snapshot first (in VirtualBox: **Machine** → **Take Snapshot**) so you can always go back.

### The GRUB menu

**GRUB** is the **bootloader**: the small program that runs before Linux and lets you choose what to start. Ubuntu, Mint and Fedora hide its menu when the last boot went well. To see it, **hold <kbd>Shift</kbd>** while the machine starts (older BIOS computers) or **tap <kbd>Esc</kbd>** repeatedly (UEFI computers, most from the last ten years). Arch shows it by default. (Some Arch installs use **systemd-boot** instead; its menu looks different.)

### Boot an older kernel

If trouble started after an update, try the previous kernel.

### On Debian / Ubuntu / Mint

Choose **Advanced options for Ubuntu** (or Debian, or Linux Mint). Pick the second kernel in the list, the one *without* "(recovery mode)".

### On Fedora

The last three kernels are listed on the main menu. Choose the second line.

### On Arch / Manjaro

Arch keeps only one kernel. Install a spare now, while things work: `sudo pacman -S linux-lts`, then `sudo grub-mkconfig -o /boot/grub/grub.cfg`. Manjaro lets you keep several kernels from **Manjaro Settings Manager** → **Kernel**.

### Recovery and rescue modes

### On Debian / Ubuntu / Mint

**Advanced options** → the entry ending **(recovery mode)**. Ubuntu and Mint show a menu: **fsck** checks the disk, **root** gives you a root shell. Debian asks for the root password and gives you a shell.

### On Fedora

The entry starting **Fedora Linux (0-rescue-...)** starts a basic, generic kernel. Use it if the normal kernels won't start. For a shell, see "Editing a boot entry" below.

### On Arch / Manjaro

**Advanced options for Arch Linux** → the entry ending **(fallback initramfs)**, if your install has one. The **initramfs** is a small starter system loaded before the real one; the fallback includes every driver, in case the normal one is missing something.

### Editing a boot entry

You can change how Linux starts, for one boot only. In the GRUB menu, highlight an entry and press <kbd>e</kbd>. Find the line starting `linux`, move to its end with the arrow keys and <kbd>End</kbd>, and add a space and one of these:

- `systemd.unit=rescue.target` for a minimal system with a root shell.
- `init=/bin/bash` for a bare root shell that skips almost everything, including `/etc/fstab`. Use this when the others ask for a root password and you don't have one (Ubuntu, Mint and Fedora lock the root account by default).

Press <kbd>Ctrl</kbd> + <kbd>X</kbd> (or <kbd>F10</kbd>) to boot. Nothing is saved; the next boot is normal.

### The emergency shell after a bad /etc/fstab

A wrong line in `/etc/fstab` (lesson U) stops the boot. After about 90 seconds you see `You are in emergency mode` and a prompt for the root password. If it says the root account is locked, reboot and use `init=/bin/bash` instead. Either way you get a root prompt.

The disk may be **read-only** (can't be changed). Make it writable, then edit:

```bash
mount -o remount,rw /
nano /etc/fstab
```

No `sudo`: you're already root. Put a `#` at the start of the bad line to switch it off, save, then:

```bash
sync
reboot -f
```

`sync` makes sure your change is written to disk; `reboot -f` restarts at once. On Fedora, run `touch /.autorelabel` before rebooting from `init=/bin/bash`; the next boot fixes SELinux labels and takes a few extra minutes.

For drives that aren't always plugged in, add `nofail` to the options in `/etc/fstab` (for example `defaults,nofail`). And before rebooting after any fstab change, check it with `sudo findmnt --verify`.

### Boot a live USB and chroot in

If none of that works, start from the live USB (or ISO) you installed from (lesson B). Choose **Try** rather than **Install**. Open a terminal, and find your Linux partition, usually the biggest `ext4` or `btrfs` one:

```bash
lsblk -f
```

Mount it at `/mnt`. On Fedora's btrfs, add `-o subvol=root`:

```bash
sudo mount /dev/sda2 /mnt
```

Now you can read and edit its files: `sudo nano /mnt/etc/fstab`. For fixing a file, that's enough.

To *run commands* as if you'd booted the broken system (reset a password, reinstall GRUB), you **chroot**: "change root", making `/mnt` look like `/` for the commands you run. If you'll touch the bootloader, first mount the boot partitions listed in `/mnt/etc/fstab` (for example `sudo mount /dev/sda1 /mnt/boot/efi`). Then connect the live system's `/dev`, `/proc`, `/sys` and `/run`, and chroot:

```bash
sudo mount --rbind /dev /mnt/dev
sudo mount --rbind /proc /mnt/proc
sudo mount --rbind /sys /mnt/sys
sudo mount --rbind /run /mnt/run
sudo chroot /mnt
```

On the Arch ISO, `arch-chroot /mnt` does all five lines for you (Manjaro's live USB has `manjaro-chroot`).

### Inside the chroot

Your prompt is now root on the broken system. Type `exit` when done, then `sudo umount -R /mnt` and reboot without the USB.

**Forgotten password:** `passwd otic` (your username) sets a new one. On Fedora, also `touch /.autorelabel`. Yes, anyone holding your computer can do this. Disk encryption is the only defence.

**Reinstall GRUB** (on a UEFI machine):

- Debian/Ubuntu/Mint: `grub-install`, then `update-grub`.
- Fedora: don't use `grub2-install`. Run `dnf reinstall shim-* grub2-efi-* grub2-common`, then `grub2-mkconfig -o /boot/grub2/grub.cfg`.
- Arch: `grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB` (use `/efi` if that's where yours is), then `grub-mkconfig -o /boot/grub/grub.cfg`.

### What went wrong last time?

If the machine boots but something failed, read the errors from the *previous* boot. `-b -1` means one boot ago; `-p err` shows errors and worse:

```bash
journalctl -b -1 -p err
```

`journalctl --list-boots` lists the boots it remembers.

### A full disk

A full disk causes strange failures: logins that bounce back, "No space left on device". Check (lesson U), then find what's big. `du` measures folders: `-x` stays on this disk, `-h` human sizes, `-d1` one level deep. `sort -h` puts the biggest last:

```bash
df -h
sudo du -xh -d1 / | sort -h
```

Old logs and downloaded package files are safe to clear. Shrink the journal with `sudo journalctl --vacuum-size=200M`, then empty the package cache: `sudo apt clean` on Debian, Ubuntu and Mint; `sudo dnf clean all` on Fedora; `sudo paccache -r` on Arch (from the `pacman-contrib` package; it keeps the last three versions of each package).

### When to give up and reinstall

Spent an evening and it still won't start? Stop. Boot the live USB, copy off anything not backed up, and reinstall. With lesson X's backup, `/etc` archive and package list, that's an hour's work, not a disaster.

## Do it now

**In a virtual machine only.** Take a VM snapshot first.

This line points at a disk that doesn't exist:

```
UUID=00000000-0000-0000-0000-000000000000 /mnt/nowhere ext4 defaults 0 2
```

1. Add it to the end of the VM's `/etc/fstab` with `sudo nano /etc/fstab`.
2. Reboot. Wait for emergency mode.
3. Get a root shell (root password, or `init=/bin/bash` from GRUB).
4. Remount `/` read-write, put `#` in front of the line, and reboot.
5. Once booted, run `journalctl -b -1 -p err` and find the error about the missing disk.

**To undo** if you get stuck: restore the VM snapshot.

You've done it when the VM boots normally and you've found the error in the journal.

## Quiz

```quiz
- q: Otic's machine stops at emergency mode after he edited /etc/fstab. What's the right fix?
  options:
    - Reinstall Linux
    - Get a root shell, remount / read-write, and comment out the bad line
    - Hold the power button until it works
  answer: 1
  why: One bad line in fstab stops the boot. Switch it off with a #, reboot, and add nofail for drives that aren't always there.
- q: What does chroot let you do from a live USB?
  options:
    - Run commands as if you'd booted the broken system
    - Wipe the disk
    - Change the root password of the live USB
  answer: 0
  why: chroot makes the mounted system look like /, so passwd, grub-install and package tools act on it.
- q: Which command shows errors from the previous boot?
  options:
    - journalctl -b -1 -p err
    - df -h
    - dmesg --clear
  answer: 0
  why: "-b -1 picks the boot before this one and -p err shows only errors and worse."
```

## Scribble watch

The Scribble loves a fresh install. "Won't boot? Just wipe it and start again!" it says, while your only copy of the photos sits on that disk. Before reinstalling anything, boot the live USB, mount the disk and copy off whatever isn't backed up. Then reinstall.
