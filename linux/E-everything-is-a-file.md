---
letter: E
title: Everything Is a File
level: 1
image: jar
---

## What went wrong

*The woods. Otic plugs a USB stick into his Mint laptop and opens the file manager.*

**Otic:** Right. The stick will be drive D:. Or E:. *(he scrolls)* There's no D:. There's no C: either.

**Psych:** There's a folder called `/`. Just slash. Click that.

*Otic clicks it. Folders called `bin`, `etc`, `usr`, `var` and `dev` appear.*

**Otic:** Which one's my stick?

**Psych:** `dev`. Devices. Obviously. I use Arch, by the way. *(he double-clicks a file called `sda`)*

*A window pops up: "There is no application installed for block device files."*

**Otic:** *(the cow on his shirt)* MOOOOO!

**Psych:** *(reaching for the Whudonk Stick)* Not a problem...

## The Operator says

Windows gives every disk a letter. Linux gives you one tree, and hangs everything off it: your files, your settings, your USB stick, even the hardware itself. Very tidy. Very confusing for the first ten minutes.

Know your way round this tree and every guide on the internet starts making sense: "edit the file in `/etc`", "check `/var/log`". Don't know it and you'll go poking round `/dev` like Psych, double-clicking a hard disk.

## The Mender's way

Linux keeps everything in one tree of folders. Once you know the main branches, you'll always know where to look.

### One tree, starting at /

On Windows, each drive has a letter: `C:`, `D:`. Linux has no drive letters. There's one top folder, called **root** and written as a single slash: `/`. Every other folder, on every disk and stick, sits somewhere inside it.

A **path** is the address of a file: the folders you go through to reach it, separated by `/`. For example:

```
/home/otic/Documents/shopping.txt
```

means: start at `/`, go into `home`, then `otic`, then `Documents`, and there's `shopping.txt`. (Windows uses backslashes, `\`. Linux uses forward slashes.)

### Your home folder

Your **home folder** is where your own files live: `/home/` followed by your username. Otic's is `/home/otic`. It holds **Documents**, **Downloads**, **Pictures** and the rest. Your file manager opens here, labelled **Home**.

Because you'll type it so often, it has a short name: `~` (the tilde, <kbd>Shift</kbd> + <kbd>#</kbd> on a UK keyboard). So `~/Documents` means "the Documents folder in my home folder".

You can do anything you like inside your home folder. Most of the rest of the tree belongs to the system, and you need special permission (lesson F) to change it.

### The main branches

| Folder | What's in it |
|---|---|
| `/home` | Everyone's home folders. |
| `/etc` | System settings, as plain text files. Say "et-see". |
| `/usr` | Installed programs and their files. |
| `/var` | Things that change as the system runs: logs (`/var/log`), caches, mail. |
| `/tmp` | Temporary files. Usually emptied when you restart. |
| `/boot` | What the computer needs to start Linux, including the kernel. |
| `/dev` | Devices: your disks, USB sticks, sound card, as special files. |
| `/root` | The home folder of the all-powerful **root** user. Not the same as `/`. |

Don't move, rename or delete anything outside your home folder. Look, by all means.

### Where USB sticks appear

When you plug in a USB stick, it appears in the file manager's sidebar with its name. Click it to open it. Behind the scenes, it's been **mounted**: attached to a folder in the tree, so its files appear there. Which folder depends on your family.

### On Debian / Ubuntu / Mint

`/media/` then your username, then the stick's name. For example: `/media/otic/HOLIDAY`.

### On Fedora

`/run/media/` then your username, then the stick's name. For example: `/run/media/mender/HOLIDAY`.

### On Arch / Manjaro

`/run/media/` then your username, then the stick's name. For example: `/run/media/psych/HOLIDAY`.

### Removing a stick safely

Before you pull a stick out, click the **eject** icon (a triangle over a line) next to its name in the file manager's sidebar. That **unmounts** it: Linux finishes writing to it and detaches it from the tree. Pulling it out without ejecting can lose whatever was being copied.

### Hidden files

Any file or folder whose name starts with a dot (`.`) is **hidden**. Your home folder is full of them: `.config`, `.bashrc`, `.local`. They hold your programs' settings, and they're hidden so they don't clutter your view.

To show them in the file manager, press <kbd>Ctrl</kbd> + <kbd>H</kbd>. Press it again to hide them. This works in Files, Nemo and Dolphin.

### Case matters

On Linux, `Photos`, `photos` and `PHOTOS` are three different names. You could have all three folders side by side. Windows would treat them as the same. If a command says it can't find a file, check the capital letters first.

### Absolute and relative paths

- An **absolute path** starts with `/`, and works from anywhere: `/home/otic/Documents`.
- A **relative path** doesn't start with `/`. It's read from wherever you are now. If you're already in `/home/otic`, then `Documents` means `/home/otic/Documents`.

Two special names work in any folder: `.` means "this folder" and `..` means "the folder above". You'll use these in the terminal in lesson F.

### Everything is a file

Linux has a famous idea: **everything is a file**. Not just documents, but disks, USB sticks, the keyboard and even information about the running system appear as files in the tree. Your first disk might be `/dev/sda` or `/dev/nvme0n1`. Information about your processor is in `/proc/cpuinfo`, a "file" Linux writes on the fly whenever you read it.

This means the same few tools (read a file, write a file) can work on almost anything. It's why Psych's double-click on `/dev/sda` didn't open anything: it's the whole disk, not a document. Don't try opening those with ordinary apps.

### Seeing paths in the file manager

The file manager can show you the path of the folder you're in, and let you type one.

1. Open your file manager (**Files**, **Nemo** or **Dolphin**).
2. Press <kbd>Ctrl</kbd> + <kbd>L</kbd>. The bar at the top turns into a box showing the path, such as `/home/otic`.
3. Type a path, for example `/etc`, and press <kbd>Enter</kbd> to go there.
4. Press <kbd>Ctrl</kbd> + <kbd>L</kbd> again, type `~` and press <kbd>Enter</kbd> to go home.

## Do it now

In your VM:

1. Open your file manager. Press <kbd>Ctrl</kbd> + <kbd>L</kbd> and note your home folder's full path.
2. Press <kbd>Ctrl</kbd> + <kbd>H</kbd>. Find the hidden `.config` folder. Press <kbd>Ctrl</kbd> + <kbd>H</kbd> again to hide it.
3. Go to `/etc` by typing it into the path box. Find the file `os-release` and open it with a double-click (it opens in a text editor). Read the `NAME=` line. Close it without saving.
4. Go to `/`. Find `home`, `usr`, `var` and `dev` in the list.
5. Go back home with `~`.

You've done it when you can write down the full path to your Downloads folder, starting with `/`.

## Quiz

```quiz
- q: Otic plugs in a USB stick on Mint. Where does it appear in the tree?
  options:
    - Drive D:
    - "/media/otic/ followed by the stick's name"
    - /dev/stick
  answer: 1
  why: Linux has no drive letters. On the Debian family, sticks are mounted under /media/your-username. Fedora and Arch use /run/media/your-username.
- q: What does ~ mean in a path?
  options:
    - Your home folder, such as /home/otic
    - The root of the whole tree
    - The folder above
  answer: 0
  why: ~ is a shortcut for your own home folder. / is the root of the tree, and .. is the folder above.
- q: Why can't you see .config in your home folder at first?
  options:
    - It has been deleted
    - Only root can see it
    - Its name starts with a dot, so it's hidden; Ctrl + H shows it
  answer: 2
  why: Names beginning with a dot are hidden. Press Ctrl + H in the file manager to show them.
```

## Scribble watch

The Scribble lurks in "tidy up" advice: "free some space by deleting these big folders in `/usr` and `/var`". Delete the wrong thing outside your home folder and Linux may not start again. Keep your tidying inside your home folder. If a guide tells you to delete anything outside it, stop and check with someone who knows.
