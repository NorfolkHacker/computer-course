---
letter: F
title: First Steps in the Terminal
level: 1
image: psych-smash
---

## What went wrong

*The woods. Otic opens a terminal for the first time. A black window with a blinking cursor.*

**Otic:** Psych said copy this command from the website. *(he selects it, presses Ctrl + C, clicks the terminal, presses Ctrl + V)*

*The terminal shows* `^V`.

**Otic:** That's not it. *(he presses Ctrl + C again to copy. The terminal prints* `^C` *and a fresh prompt.)*

**Psych:** You've got to *mean* it. Here. *(he types* `sudo whoami`*, presses Enter, and starts typing his password. No dots appear.)* It's not even typing! *(he types it again. And again. Then presses Enter.)*

*The terminal prints:* `Sorry, try again.`

**Otic:** *(the cow on his shirt)* MOOOOO!

*Psych lifts the Whudonk Stick, which crackles hopefully.*

## The Operator says

Ah. The terminal. My office.

Everyone's scared of it for a week. Then they realise it's a window where you say exactly what you want, and get exactly that. No menus. No "are you sure?", which is both the good news and the bad news.

The keyboard shortcuts are different in here, the password doesn't show while you type, and `sudo` means "do this with the power to break everything". Learn those three things today and the rest of this course is just vocabulary.

## The Mender's way

The **terminal** is a window where you type commands and read the replies. It's quiet and literal. Take it slowly.

### Opening the terminal

### On Debian / Ubuntu / Mint

Press <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>T</kbd>. Or open the menu and type `terminal`. It's called **Terminal**.

### On Fedora

Press <kbd>Super</kbd> and type `terminal`. Fedora's is called **Terminal** (the program is named Ptyxis; older versions used GNOME Terminal). On Fedora's KDE edition, it's **Konsole**, and <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>T</kbd> opens it.

### On Arch / Manjaro

It depends on your desktop. On GNOME, press <kbd>Super</kbd> and type `terminal` (it may be called **Console** or **Terminal**). On KDE Plasma, press <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>T</kbd> to open **Konsole**. On Cinnamon, open **Menu** and type `terminal`.

### The prompt

The terminal shows a **prompt**: a short line that means "ready, type a command". It tells you who you are, which computer you're on and where you are.

```
otic@mint-vm:~$
```

That's **user** `otic`, **@** (at) the computer `mint-vm`, in the folder `~` (home, from lesson E). The `$` means you're an ordinary user. Fedora and Arch put square brackets round it, `[mender@fedora ~]$`, but it means the same.

To run a command, type it after the prompt and press <kbd>Enter</kbd>.

### Where am I, and what's here?

```bash
pwd
```

`pwd` means **p**rint **w**orking **d**irectory: it shows the full path of the folder you're in (a **directory** is the same as a folder). In a new terminal, that's your home folder, such as `/home/otic`.

```bash
ls
```

`ls` **l**i**s**ts what's in the current folder: `Desktop  Documents  Downloads  Music ...`

Commands can take **options**, usually a dash and a letter, which change what they do:

```bash
ls -l
```

`-l` means **long**: one item per line, with details. A line looks like this:

```
drwxr-xr-x 2 otic otic 4096 Nov 18 10:02 Documents
```

The first letter `d` means it's a directory (a `-` means an ordinary file). The rest of that block is **permissions** (lesson K). Then the owner (`otic`), the size, the date it was last changed, and the name.

```bash
ls -a
```

`-a` means **all**: it includes hidden files whose names start with a dot (lesson E). You can combine them: `ls -la`.

### Moving around

`cd` means **c**hange **d**irectory. Put the folder after it, with a space:

```bash
cd Documents
```

That's a relative path: the `Documents` inside wherever you are. Run `pwd` to check where you've ended up.

```bash
cd ..
```

Goes up one level, to the folder above.

```bash
cd ~
```

Goes straight home, from anywhere. (Plain `cd` on its own does the same.) Absolute paths work too: `cd /etc`.

Remember from lesson E: `Documents` and `documents` are different names. Capitals matter.

### Time-savers

- **Tab completion**: type the start of a name and press <kbd>Tab</kbd>. The terminal finishes it for you. Type `cd Doc` then <kbd>Tab</kbd> and it becomes `cd Documents/`. If nothing happens, there's more than one match (or none); press <kbd>Tab</kbd> twice to see the choices.
- **History**: press <kbd>Up</kbd> to bring back your last command, and again for the one before. Press <kbd>Enter</kbd> to run it again, or edit it first.
- **Clear the screen**: `clear` (or <kbd>Ctrl</kbd> + <kbd>L</kbd>) wipes the window. It doesn't undo anything.

### Stopping, copying and pasting

In the terminal, <kbd>Ctrl</kbd> + <kbd>C</kbd> doesn't copy. It **stops** whatever's running and gives you a fresh prompt. It's your emergency brake: if anything runs on and on, press it.

To copy and paste, add <kbd>Shift</kbd>:

- **Copy**: select text with the mouse, then <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>C</kbd>.
- **Paste**: <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>V</kbd>.

Or right-click inside the terminal and choose **Copy** or **Paste**.

### Who am I, and what am I running?

```bash
whoami
```

Prints your username.

```bash
uname -r
```

`uname` shows information about the system; `-r` asks for the **r**elease of the Linux kernel (lesson A), such as `6.8.0-48-generic` on Mint and Ubuntu, or a number ending in `fc41` on Fedora or `arch1-1` on Arch.

```bash
cat /etc/os-release
```

`cat` prints a file's contents into the terminal. This is the file you opened in lesson E: your distro's name and family.

### sudo: borrowing the keys

Your user can change your own files, but not the system. The **root** user (also called the **superuser**) can change anything. `sudo` (**s**uper**u**ser **do**) runs one command as root, after asking for *your* password:

```bash
sudo whoami
```

It asks for your password, then prints `root`, because that one command ran as root.

- **While you type the password, nothing appears on screen.** That's deliberate, so nobody can count the letters. Type it and press <kbd>Enter</kbd>. (Mint shows a star for each letter instead.)
- After a correct password, `sudo` remembers you for a few minutes.
- On Arch, `sudo` only works if you made your user a superuser in `archinstall` (lesson B).
- Only use `sudo` when a command needs to change the system, and only when you know what that command does. As root, there are no safety nets.

## Do it now

In your VM's terminal, run each of these, one at a time, and read the reply:

1. `whoami`, then `pwd`.
2. `ls`, then `ls -l`, then `ls -a`. Spot a hidden file.
3. `cd Doc` then press <kbd>Tab</kbd>, then <kbd>Enter</kbd>. Run `pwd`.
4. `cd ..`, then `pwd`. Then `cd /etc`, then `cd ~`.
5. Press <kbd>Up</kbd> a few times to see your history.
6. `uname -r` and `cat /etc/os-release`.
7. `sudo whoami`, and type your password even though nothing shows.
8. `clear`.

You've done it when `sudo whoami` prints `root` and you're back home, with `pwd` showing your home folder.

## Quiz

```quiz
- q: In the terminal, what does Ctrl + C do?
  options:
    - Copies the selected text
    - Stops the command that's running
    - Clears the screen
  answer: 1
  why: In a terminal, Ctrl + C stops the running command. To copy, use Ctrl + Shift + C.
- q: Psych types his password for sudo and nothing appears. What's going on?
  options:
    - The keyboard is broken
    - sudo needs restarting
    - It's hiding the password on purpose; type it and press Enter
  answer: 2
  why: Most terminals show nothing while you type a password, so nobody can see how long it is. Type it once and press Enter.
- q: Which command shows the folder you're in?
  options:
    - pwd
    - ls -a
    - whoami
  answer: 0
  why: pwd prints the working directory. ls -a lists the folder's contents, including hidden files, and whoami prints your username.
```

## Scribble watch

The Scribble's favourite move is a web page that says "just paste this into your terminal", with `sudo` in front. Once it runs as root, it can do anything. Before you paste a command, read it: if you don't know what every part does, don't run it. Lesson H shows you how to look commands up. Never type your password for a command you don't understand.
