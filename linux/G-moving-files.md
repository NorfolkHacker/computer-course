---
letter: G
title: Moving Files
level: 2
image: poof
---

## What went wrong

*Psych's flat. Psych at his Arch laptop, Otic peering over his shoulder.*

**Psych:** My Downloads folder's full of junk. Watch this. One command and it's gone. I use Arch, by the way.

**Otic:** You said that already.

*Psych types* `cd Downloadz` *and presses Enter. The terminal says* `No such file or directory`. *Psych doesn't read it.*

**Psych:** Now we delete everything in here. *He types* `rm -r *` *and presses Enter.*

*Nothing happens for a moment. Then nothing keeps happening, very fast.*

**Otic:** Psych. What folder are you in?

**Psych:** *(typing* `ls`*)* ...

*The screen is empty. His Documents, Pictures and Music are gone.*

**Otic:** Where's the Recycle Bin?

**Otic's shirt:** MOOOOO!

*POOF.*

## The Operator says

Luser list, entry 2,117: "deleted home folder, asked where the bin was".

There is no bin. `rm` doesn't move things somewhere safe. It removes them. The terminal does exactly what you type, in the folder you're actually in, not the folder you meant to be in. That's not a flaw; that's the whole point. It's also why I sleep well and Psych doesn't.

This lesson is how to make, copy, move, rename and delete files without the screaming. Practise in a test folder. Always know where you are before you delete anything.

## The Mender's way

Everything here happens in the terminal, and it's the same on every distro. Go slowly. Check where you are with `pwd` (lesson F) before anything that deletes.

### Making folders: mkdir

`mkdir` (**make directory**) makes a new folder. A **directory** is just Linux's word for a folder.

```bash
mkdir practice
```

To make a folder inside a folder inside a folder in one go, add `-p` (**parents**: make any missing folders along the way). It also doesn't complain if the folder already exists.

```bash
mkdir -p practice/photos/2026
```

### Making empty files: touch

`touch` creates an empty file if it doesn't exist. (If it does exist, it just updates the file's "last changed" time and leaves the contents alone.)

```bash
touch notes.txt
```

### Copying: cp

`cp` copies a file. You give it the **source** (what to copy) first, then the **destination** (where to put it).

```bash
cp notes.txt notes-copy.txt
cp notes.txt practice/
```

The first makes a second file with a new name. The second puts a copy inside the `practice` folder, keeping its name.

To copy a whole folder and everything in it, add `-r` (**recursive**: go into every folder inside it too):

```bash
cp -r practice practice-backup
```

### Moving and renaming: mv

`mv` (**move**) does two jobs. Linux treats renaming as moving a file to a new name in the same place.

```bash
mv notes-copy.txt old-notes.txt
mv old-notes.txt practice/
```

The first renames. The second moves the file into `practice`. `mv` works on folders without needing `-r`.

**Careful:** if the destination file already exists, `cp` and `mv` replace it without asking. Add `-i` (**interactive**) and they ask first:

```bash
mv -i notes.txt practice/
```

### Deleting: rm and rmdir

`rm` (**remove**) deletes files. `rmdir` deletes folders, but only empty ones, which makes it the safe choice.

```bash
rm practice/notes.txt
rmdir practice/photos/2026
```

To delete a folder that still has things in it, you need `rm -r`. You'll also see `rm -rf` on the internet: `-f` means **force**, never ask, never complain. Together they delete everything below that point with no questions. Use them only when you've just checked with `pwd` and `ls` exactly what you're about to remove.

**Why there's no Recycle Bin:** `rm` is a basic tool that's older than desktop bins. It tells the system to forget the file, straight away. The **Trash** you see in your file manager (lesson C) is a separate feature of the desktop; `rm` never uses it. Assume anything you `rm` is gone for good.

To make `rm` ask before each file, add `-i`:

```bash
rm -i practice/old-notes.txt
```

```
rm: remove regular empty file 'practice/old-notes.txt'?
```

Type `y` and Enter to delete, or `n` and Enter to keep it.

### Wildcards: * and ?

A **wildcard** is a symbol that stands for other characters, so one command can match many files.

| Wildcard | Matches | Example | Matches |
|---|---|---|---|
| `*` | any number of any characters (including none) | `*.txt` | `a.txt`, `notes.txt` |
| `?` | exactly one character | `photo?.jpg` | `photo1.jpg`, `photoA.jpg`, not `photo10.jpg` |

Before you use a wildcard with `rm`, use it with `ls` first. `ls` shows you exactly which files it matches, without harming anything:

```bash
ls *.txt
```

If the list is what you expected, then (and only then) swap `ls` for `rm`.

### Names with spaces

The terminal splits commands at spaces. So `rm holiday photo.jpg` means "delete a file called `holiday` and a file called `photo.jpg`". Wrap the name in quotes so it's treated as one name:

```bash
touch "holiday photo.jpg"
ls "holiday photo.jpg"
```

You can also put a backslash before each space: `holiday\ photo.jpg`. Pressing <kbd>Tab</kbd> to complete a name (lesson F) adds the backslashes for you, which is the easiest way.

## Do it now

Everything happens in a new test folder in your home directory. Nothing outside it is touched.

1. Open a terminal. Go home and make the test folder:

   ```bash
   cd ~
   mkdir -p ~/practice/G
   cd ~/practice/G
   pwd
   ```

   Check `pwd` shows a path ending in `/practice/G`.
2. Make some files: `touch one.txt two.txt three.log "my file.txt"`
3. Make a nested folder: `mkdir -p box/inner`
4. Copy and rename: `cp one.txt box/` then `mv two.txt second.txt`
5. Copy the whole folder: `cp -r box box-copy`
6. Test a wildcard safely: `ls *.txt`. You should see `my file.txt`, `one.txt` and `second.txt`, but not `three.log`.
7. Delete with a safety net: `rm -i *.txt`. Answer `n` to `my file.txt` and `y` to the others.
8. Remove the empty inner folder: `rmdir box-copy/inner`
9. Run `ls -R` (**R**ecursive list) to see what's left.

You've done it when `ls` shows `box`, `box-copy`, `my file.txt` and `three.log`, and you can explain why `rmdir box` would fail (it isn't empty). Keep `~/practice`; later lessons use it.

## Quiz

```quiz
- q: Psych typed a folder name wrong, didn't notice, then ran rm -r *. What should he have done first?
  options:
    - Run it again with sudo
    - Check where he was with pwd and what would be deleted with ls
    - Look in the Recycle Bin afterwards
  answer: 1
  why: The terminal acts on the folder you're actually in. pwd and ls show you that before anything is deleted.
- q: How do you rename report.txt to final.txt?
  options:
    - rename report.txt
    - cp -r report.txt final.txt
    - mv report.txt final.txt
  answer: 2
  why: On Linux, renaming is moving a file to a new name. mv does it.
- q: Which command lists the files that photo?.jpg would match, without deleting them?
  options:
    - "rm -i photo?.jpg"
    - "ls photo?.jpg"
    - "rmdir photo?.jpg"
  answer: 1
  why: Always test a wildcard with ls first. Only swap ls for rm once the list is right.
```

## Scribble watch

The Scribble loves a forum reply that says "just run `rm -rf` on this folder to fix it". One typo, one stray space (`rm -rf / home/you/thing` instead of `/home/you/thing`), and it isn't one folder any more. Never run `rm -rf` you've copied from someone else. Type it yourself, check the path with `ls` first, and if you aren't sure, use `rm -ri` so it asks you about every file.
