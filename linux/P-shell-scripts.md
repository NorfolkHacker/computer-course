---
letter: P
title: Shell Scripts
level: 3
image: mender
---

## What went wrong

*Otic's kitchen. Otic proudly shows Psych a text file called* `backup.sh`.

**Otic:** I wrote my first script! It copies my Documents folder somewhere safe.

*He types* `backup.sh` *and presses Enter.*

```
backup.sh: command not found
```

**Otic:** *(the cow on his shirt)* MOOOOO!

**Psych:** Not a problem. *He types* `sudo chmod 777 backup.sh` *and* `sudo ./backup.sh`.

*The script runs. It contains the line* `cp -r $folder /media/usb` *, where* `$folder` *is* `My Documents`. *It tries to copy a folder called* `My` *and a folder called* `Documents`. *Neither exists. It prints two errors, then carries on regardless and announces:* `Backup complete!`

**Otic:** It says complete.

**Psych:** Then it's complete. Arch-level scripting, that.

## The Operator says

A script that says "complete" when it isn't is worse than no script. It's a liar with a schedule.

Here's the thing, though: scripts are where Linux stops being a chore. Any job you type more than twice can become one word. You just need four habits: tell the system which shell runs it, make it executable without handing the keys to the whole planet, quote your variables, and make it stop when something fails. Do that, and your scripts won't lie to you. Unlike Psych.

## The Mender's way

A **shell script** is a text file full of commands that bash runs from top to bottom, exactly as if you'd typed them.

### Your first script

1. Make a folder for your scripts and go into it:

```bash
mkdir -p ~/.local/bin
cd ~/.local/bin
```

2. Create the file: `nano hello`
3. Type these two lines, then save and exit:

```bash
#!/bin/bash
echo "Hello, $USER. It is $(date +%A)."
```

The first line is the **shebang**: `#!` followed by the program that should run the file. Always put it on line 1. `$(...)` runs a command and drops its output into the line.

4. Make it **executable** (allowed to run as a program). `+x` adds the execute permission for you, and nobody needs `777`:

```bash
chmod +x hello
```

5. Run it. `./` means "the file in this folder", because the current folder isn't in `PATH`:

```bash
./hello
```

### Putting your scripts on the PATH

So you can type `hello` from anywhere, `~/.local/bin` has to be in your `PATH` (lesson O).

### On Debian / Ubuntu / Mint

`~/.profile` adds `~/.local/bin` to `PATH` at login, but only if the folder already existed. Log out and back in once, then check with `echo $PATH`.

### On Fedora

`~/.bashrc` already adds `~/.local/bin` and `~/bin`. Open a new terminal and it works.

### On Arch / Manjaro

Not added by default. Put this line at the bottom of `~/.bashrc`, then run `source ~/.bashrc`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Check it

Now, from any folder:

```bash
hello
```

### Arguments

Words you type after a script's name are its **arguments**. Inside the script, `$1` is the first, `$2` the second, `$#` how many there are, and `"$@"` all of them.

```bash
#!/bin/bash
echo "First: $1"
echo "You gave me $# things:"
for thing in "$@"; do
    echo " - $thing"
done
```

That `for` loop runs the indented lines once for each item, with `thing` set to each one in turn. It also works with file patterns: `for f in *.txt; do ... done`.

### Quote your variables

This is the mistake in Psych's script. If a variable holds `My Documents` and you write `$folder` bare, bash splits it at the space into two words. Write `"$folder"` in double quotes and it stays one. **Always put double quotes around variables.**

### if, else and test

`[ ... ]` is the **test** command: it checks something and answers yes or no. Spaces inside the brackets are required.

```bash
if [ -d "$1" ]; then
    echo "$1 is a folder"
else
    echo "$1 is not a folder"
fi
```

Common tests:

| Test | True when |
|---|---|
| `-d "$x"` | `$x` is a folder |
| `-f "$x"` | `$x` is a file |
| `-z "$x"` | `$x` is empty |
| `"$a" = "$b"` | the two texts match |
| `"$n" -gt 5` | the number is greater than 5 |

### Exit codes and $?

Every command finishes with an **exit code**: `0` means success, anything else means something went wrong. `$?` holds the last one:

```bash
ls /nonexistent
echo $?
```

```
2
```

### Safety switches: set -euo pipefail

Put this on line 2 of serious scripts:

```bash
set -euo pipefail
```

- `-e`: stop as soon as a command fails, instead of carrying on.
- `-u`: stop if you use a variable that was never set (catches typos).
- `-o pipefail`: in a pipe like `a | b`, count it as failed if any part fails, not just the last.

It isn't perfect, but it turns "lied about success" into "stopped and told you".

### A useful one: dated backups

Save this as `~/.local/bin/backup-folder` and `chmod +x` it:

```bash
#!/bin/bash
set -euo pipefail

if [ $# -ne 1 ]; then
    echo "Usage: backup-folder FOLDER" >&2
    exit 1
fi

src="$1"
dest="$HOME/backups"
stamp="$(date +%Y-%m-%d_%H%M)"
name="$(basename "$src")"

if [ ! -d "$src" ]; then
    echo "Not a folder: $src" >&2
    exit 1
fi

mkdir -p "$dest"
tar -czf "$dest/$name-$stamp.tar.gz" -C "$(dirname "$src")" "$name"
echo "Saved $dest/$name-$stamp.tar.gz"
```

What's new here: `-ne` means "not equal"; `!` means "not"; `>&2` sends a message to the error output; `exit 1` stops with a failure code. `tar -czf` **c**reates a **z**ipped archive in the **f**ile named next. `-C` makes tar step into the parent folder first, so the archive holds `Documents/...` rather than the full path.

### shellcheck: a spelling checker for scripts

**shellcheck** reads a script and points out mistakes, like missing quotes.

### On Debian / Ubuntu / Mint

```bash
sudo apt install shellcheck
```

### On Fedora

```bash
sudo dnf install ShellCheck
```

### On Arch / Manjaro

```bash
sudo pacman -S shellcheck
```

### Using it

```bash
shellcheck ~/.local/bin/backup-folder
```

No output means it found nothing to complain about.

## Do it now

All of this happens in your home folder.

1. Create `~/.local/bin/backup-folder` with the script above and run `chmod +x ~/.local/bin/backup-folder`.
2. Make a test folder with a space in its name: `mkdir -p ~/"test stuff"` then `echo hi > ~/"test stuff"/note.txt`.
3. Run `backup-folder ~/"test stuff"`.
4. Check it worked: `ls ~/backups` and `tar -tzf ~/backups/*.tar.gz` (`-t` lists what's inside).
5. Run `backup-folder ~/nope` and then `echo $?`. You should see the error and `1`.
6. Install shellcheck and run it on your script.

You've done it when the archive lists `test stuff/note.txt` and the bad folder gives exit code `1`. To tidy up: `rm -r ~/"test stuff" ~/backups`.

## Quiz

```quiz
- q: Otic typed backup.sh and got "command not found". What should he type?
  options:
    - sudo backup.sh
    - ./backup.sh, after chmod +x backup.sh
    - sudo chmod 777 backup.sh
  answer: 1
  why: The current folder isn't in PATH, so you run it with ./, and it needs the execute permission that chmod +x gives.
- q: A variable holds "My Documents". How should you use it in a command?
  options:
    - $folder
    - "'$folder'"
    - '"$folder"'
  answer: 2
  why: Double quotes keep it as one item. Bare, it splits at the space; single quotes stop the variable being filled in at all.
- q: What does set -e do?
  options:
    - Stops the script as soon as a command fails
    - Makes the script run faster
    - Hides error messages
  answer: 0
  why: Without it, bash carries on after a failure, which is how a broken backup ends up saying "complete".
```

## Scribble watch

The Scribble posts handy one-liners: `curl https://some.site/install.sh | sudo bash`. That runs a stranger's script as root without you ever reading it. Propellor Boy did it once and is now orbiting Neptune. Download the script to a file instead, read it in `less`, run `shellcheck` on it, and only then decide whether to run it.
