---
letter: I
title: Inside Files
level: 2
image: otic
---

## What went wrong

*Otic's kitchen. Psych has borrowed Otic's Mint laptop "for a second".*

**Psych:** I need to change one line in a config file. Real admins use vim. I use Arch, by the way.

*He types* `vim notes.txt` *and presses Enter. A mostly empty screen with a column of* `~` *signs appears.*

**Psych:** Right. Type the words. *He types* `hello`. *The cursor leaps around. Something gets deleted.*

**Psych:** Save. *He presses Ctrl+S. The terminal freezes completely.*

**Otic:** How do you get out?

**Psych:** Ctrl+C. *Nothing happens. He presses Escape eleven times, then types* `exit`, `quit` *and* `please`.

*An hour passes. The kitchen clock ticks. The Mender walks past, presses one key on the laptop, and leaves. The screen comes back. Psych pretends not to notice.*

**Otic's shirt:** *(faintly)* moooo.

## The Operator says

I once left a contractor in vim over a bank holiday weekend. He's fine now. Mostly.

Nearly everything on Linux is a plain text file: settings, logs, lists of users. Learn to read them quickly and change them safely and you can fix half the problems on a Linux box without installing anything. The other half are caused by people changing them unsafely. That's why we make backups first. Every time. I'm watching.

## The Mender's way

Files are just text. A few small tools let you look inside them, and one friendly editor lets you change them.

Make a file to practise on. `ls -l /etc` lists the system settings folder; the `>` sends that list into a file instead of the screen (you'll learn how in lesson J):

```bash
cd ~/practice
ls -l /etc > etc-list.txt
```

### cat: show a whole file

`cat` (short for **concatenate**, joining files together) prints a file to the screen:

```bash
cat etc-list.txt
```

Good for short files. For a long one, it scrolls straight past.

### less: read a long file

`less` shows a file one screen at a time. It uses the same keys as `man` (lesson H):

```bash
less etc-list.txt
```

| Key | Does |
|---|---|
| <kbd>Space</kbd> / <kbd>b</kbd> | Next / previous screen |
| <kbd>/</kbd> then a word, <kbd>Enter</kbd> | Search; <kbd>n</kbd> for the next match |
| <kbd>g</kbd> / <kbd>Shift</kbd> + <kbd>g</kbd> | Top / bottom |
| <kbd>q</kbd> | Quit |

`less` only reads. It can't change the file, so it's always safe.

### head and tail: the start and the end

`head` shows the first ten lines; `tail` shows the last ten. `-n` chooses how many:

```bash
head -n 5 etc-list.txt
tail -n 3 etc-list.txt
```

`tail -f` (**follow**) shows the end of a file and keeps watching, printing new lines as they're added. It's how admins watch a log file live. Press <kbd>Ctrl</kbd> + <kbd>C</kbd> to stop.

### wc: count

`wc` (**word count**) counts lines, words and bytes:

```bash
wc etc-list.txt
wc -l etc-list.txt
```

```
112 1001 6789 etc-list.txt
112 etc-list.txt
```

The first shows lines, words, bytes; `-l` asks for lines only. Your numbers will differ.

### Editing with nano

**nano** is a simple text editor that runs in the terminal. Fedora uses it as the default editor, and Mint and Ubuntu include it. Arch doesn't install it unless you ask, so on Arch or Manjaro install it first:

```bash
sudo pacman -S nano
```

Open (or create) a file:

```bash
nano shopping.txt
```

Just type; it behaves like Notepad. The shortcuts are listed along the bottom, where `^` means <kbd>Ctrl</kbd> and `M-` means <kbd>Alt</kbd>.

| Keys | Does |
|---|---|
| <kbd>Ctrl</kbd> + <kbd>O</kbd>, then <kbd>Enter</kbd> | Save ("write **O**ut"); Enter confirms the file name |
| <kbd>Ctrl</kbd> + <kbd>X</kbd> | Exit. If there are unsaved changes, it asks: <kbd>Y</kbd> to save, <kbd>N</kbd> to throw them away |
| <kbd>Ctrl</kbd> + <kbd>W</kbd> | Search ("**W**here is"); type a word and press <kbd>Enter</kbd> |
| <kbd>Ctrl</kbd> + <kbd>K</kbd> / <kbd>Ctrl</kbd> + <kbd>U</kbd> | Cut the current line / paste it |
| <kbd>Ctrl</kbd> + <kbd>G</kbd> | Help |

### vim, honestly

**vim** (and its older relative **vi**) is a powerful editor that many admins love. It's installed almost everywhere, and sometimes a command opens it without asking. It has **modes**: keys give commands rather than typing text until you switch to typing mode. That's why Psych got stuck.

To escape without saving anything:

1. Press <kbd>Esc</kbd> (it's safe to press it several times).
2. Type `:q!` (colon, q, exclamation mark). It appears at the bottom-left.
3. Press <kbd>Enter</kbd>.

`:q!` means "quit, and throw away my changes". If you want to learn vim properly later, run `vimtutor` (you may need to install the full `vim` package first). For this course, nano is enough.

### Editing system files

Files in `/etc` belong to the system (lesson E), so you need admin rights to change them. Before you change any config file, **make a backup copy**:

```bash
sudo cp /etc/hosts /etc/hosts.bak
```

`sudo` is needed because you're writing a new file into `/etc`. If your edit breaks something, copying the `.bak` back over the original undoes it.

Then edit. There are two ways:

```bash
sudoedit /etc/hosts
```

`sudoedit` copies the file, opens the copy in your normal editor *as you*, and only puts it back with admin rights when you save and exit. It's the safer choice. If it opens vim, escape with `:q!` (or if it complains it can't find an editor), run it like this instead, which tells it to use nano:

```bash
EDITOR=nano sudoedit /etc/hosts
```

The older way, `sudo nano /etc/hosts`, runs the whole editor as root (the all-powerful admin account; lesson K). It works, and you'll see it in many guides, but `sudoedit` is better practice.

## Do it now

All in `~/practice`; you won't change any system file.

1. `cd ~/practice` and make the list file: `ls -l /etc > etc-list.txt`
2. Count its lines with `wc -l etc-list.txt`.
3. Show the first 3 and last 3 lines with `head -n 3` and `tail -n 3`.
4. Open it with `less`, search for `/hosts`, then press <kbd>q</kbd>.
5. Make a backup: `cp etc-list.txt etc-list.txt.bak`
6. Open `nano etc-list.txt`. Add a line at the top saying `I edited this`. Save with <kbd>Ctrl</kbd> + <kbd>O</kbd>, <kbd>Enter</kbd>, and exit with <kbd>Ctrl</kbd> + <kbd>X</kbd>.
7. Check it worked: `head -n 1 etc-list.txt`
8. Try vim and escape: `vim etc-list.txt` (or `vi` if `vim` isn't found; a fresh Arch install may have neither, so skip this step), then <kbd>Esc</kbd>, `:q!`, <kbd>Enter</kbd>.
9. Open a second terminal window. In it, run `tail -f ~/practice/etc-list.txt`. In the first window, run `date >> ~/practice/etc-list.txt` (`>>` adds a line to the end; lesson J). Watch the date appear in the second window, then stop it with <kbd>Ctrl</kbd> + <kbd>C</kbd>.

You've done it when you've edited and saved a file in nano, escaped vim, and watched `tail -f` show a new line live.

## Quiz

```quiz
- q: You're stuck in vim. How do you get out without saving?
  options:
    - Press Ctrl+C
    - "Press Esc, type :q! and press Enter"
    - Type exit and press Enter
  answer: 1
  why: Esc leaves typing mode, and :q! quits while throwing away changes. Ctrl+C and exit don't work inside vim.
- q: How do you save in nano?
  options:
    - Ctrl+S
    - Ctrl+O, then Enter
    - Ctrl+X, then N
  answer: 1
  why: Ctrl+O writes the file out and Enter confirms the name. Ctrl+X then N exits without saving.
- q: What should you do before editing a config file in /etc?
  options:
    - Make a backup copy, for example with sudo cp
    - Run chmod on it so anyone can edit it
    - Open it with cat and type over it
  answer: 0
  why: A .bak copy lets you undo a mistake by copying it back. cat only reads files.
```

## Scribble watch

The Scribble lives in config files. One wrong character in `/etc` and a service won't start, or the machine won't boot. Its favourite moment is just after you've changed something and can't remember what it said before. Always copy a config file to `.bak` before editing, change one thing at a time, and test after each change.
