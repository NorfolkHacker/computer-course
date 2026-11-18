---
letter: J
title: Joining Commands
level: 2
image: shloop
---

## What went wrong

*Psych's flat. Psych is following a guide on his Arch laptop. Otic holds a cup of tea for him.*

**Psych:** The guide says add this line to a system file. Easy. *He types* `echo "hello" > /etc/motd` *and presses Enter.*

**Psych's terminal:** `bash: /etc/motd: Permission denied`

**Psych:** Ha. Forgot `sudo`. I use Arch, by the way. *He types* `sudo echo "hello" > /etc/motd`.

**Psych's terminal:** `bash: /etc/motd: Permission denied`

**Psych:** I *said* sudo.

**Otic:** Maybe say it louder?

**Psych:** *(typing)* `sudo sudo echo "hello" > /etc/motd`

**Psych's terminal:** `bash: /etc/motd: Permission denied`

*The Whudonk Stick begins to crackle. Otic quietly moves the tea out of range.*

**Otic's shirt:** MOOOOO!

## The Operator says

Linux commands are small. Each one does one job. The trick, the bit that makes people like me dangerous, is joining them together: the output of one becomes the input of the next, and ten tiny tools become one big one.

It's also where the most baffling mistakes live. Psych's `sudo` was working perfectly. It just wasn't doing the bit he thought it was. By the end of this lesson you'll know exactly why, and you'll be able to search a thousand files for one word in under a second. I find that very relaxing.

## The Mender's way

Every command has an **input**, an **output** (what it normally prints) and a separate **error output** (where it prints complaints). You can point each of them somewhere else.

Make some practice files first:

```bash
mkdir -p ~/practice/J
cd ~/practice/J
printf "apple\nBanana\ncherry\napple\ndate\nBanana\n" > fruit.txt
cat fruit.txt
```

`printf` prints text; each `\n` means "new line". The `>` puts it in a file, explained next.

### Redirection: > >> <

| Symbol | Means | Example |
|---|---|---|
| `>` | Send output to a file, **replacing** what's in it | `ls > list.txt` |
| `>>` | Send output to a file, **adding** to the end | `date >> log.txt` |
| `<` | Feed a file in as the input | `wc -l < fruit.txt` |

`>` empties the file before it writes, without asking. Use `>>` when you want to keep what's there.

### Errors: 2> and 2>&1

Error messages travel separately from normal output, so `>` doesn't catch them. Linux numbers the two streams: **1** is normal output, **2** is errors. `2>` sends just the errors somewhere:

```bash
ls fruit.txt missing.txt 2> errors.txt
cat errors.txt
```

The file listing appears on screen; the `No such file` complaint went into `errors.txt`.

`2>&1` means "send errors to the same place as normal output". To catch everything in one file, put it **after** the `>`:

```bash
ls fruit.txt missing.txt > all.txt 2>&1
```

You'll also see `2> /dev/null`. `/dev/null` is a special file that throws away anything written to it: a bin for output you don't want.

### Pipes: |

The **pipe** `|` (on UK keyboards, usually <kbd>Shift</kbd> + the key left of <kbd>Z</kbd>) sends one command's output straight into the next command, with no file in between:

```bash
ls -l /etc | less
```

That lets you scroll through a long listing in `less` (lesson I).

### grep: find lines

`grep` prints only the lines that contain a word or pattern.

```bash
grep apple fruit.txt
```

Useful options:

| Option | Means |
|---|---|
| `-i` | **ignore case**: `banana` matches `Banana` |
| `-n` | show line **numbers** |
| `-v` | in**v**ert: show lines that *don't* match |
| `-r` | **recursive**: search every file in a folder and the folders inside it |

```bash
grep -in banana fruit.txt
grep -v apple fruit.txt
grep -r apple ~/practice
```

And with a pipe, `grep` filters any command's output:

```bash
ls /etc | grep conf
```

### sort, uniq and cut

`sort` puts lines in order. `uniq` removes repeated lines, but only when they're next to each other, so you almost always `sort` first. `uniq -c` counts them:

```bash
sort fruit.txt | uniq -c
```

```
      2 apple
      2 Banana
      1 cherry
      1 date
```

(The order of capital and small letters may differ slightly between systems.)

`cut` takes out one column. `-d` says what separates the columns and `-f` which field (column) you want. `/etc/passwd` lists user accounts, with fields separated by `:`; the first field is the username:

```bash
cut -d: -f1 /etc/passwd
```

### tee: a T-junction

`tee` writes its input to a file **and** to the screen, like a T-shaped pipe joint:

```bash
sort fruit.txt | tee sorted.txt
```

Add `-a` to append (add to the end) instead of replacing.

### The sudo echo gotcha

Here's what went wrong for Psych. In `sudo echo "hello" > /etc/motd`, the `>` isn't part of the `sudo` command. Your own shell (the program reading what you type, running as you) opens the file first, then runs `sudo echo`. So `echo` runs as root, but the file is opened by you, and you aren't allowed to write in `/etc`.

The fix is to let a command that *is* running with `sudo` do the writing. That's what `tee` is for:

```bash
echo "hello" | sudo tee -a /etc/motd
```

Here `echo` runs as you, and `sudo tee` (running as root) writes the file. Without `-a`, `tee` replaces the whole file, so be careful. You'll see this pattern in lots of setup guides. (Don't run this one: it changes a system file.)

### Chaining: && ; ||

You can put several commands on one line:

| Between commands | Runs the next one... |
|---|---|
| `;` | always, whatever happened |
| `&&` | only if the first **succeeded** |
| <code>&#124;&#124;</code> | only if the first **failed** |

```bash
mkdir -p ~/practice/J/new && cd ~/practice/J/new
```

If `mkdir` fails, `cd` doesn't run, so you don't end up working in the wrong folder. `&&` is the one you'll use most.

```bash
grep -q mango ~/practice/J/fruit.txt || echo "No mangoes"
```

`grep -q` (**quiet**) prints nothing and just succeeds or fails, so `echo` runs only when there's no mango.

## Do it now

All inside `~/practice/J`, using the fruit file made above. The last part uses `sudo` on a test file you create; nothing in the system changes.

1. Count how many times each fruit appears, ignoring case: `sort -f fruit.txt | uniq -ic`
2. Find which lines mention "an", with line numbers: `grep -n an fruit.txt`
3. Catch an error: `ls nothing-here 2> err.txt` then `cat err.txt`
4. Append, don't replace: `date >> log.txt`, twice, then `cat log.txt` shows two lines.
5. Try the gotcha safely. Make a file owned by root: `sudo touch rootfile.txt`
6. Run `sudo echo hi > rootfile.txt`. You get `Permission denied`.
7. Now run `echo hi | sudo tee rootfile.txt` and check with `cat rootfile.txt`.
8. Tidy up: `sudo rm rootfile.txt` (`sudo` is needed because root owns it).

You've done it when step 6 fails, step 7 works, and you can explain why.

## Quiz

```quiz
- q: Why did Psych's sudo echo "hello" > /etc/motd still say Permission denied?
  options:
    - He needed to type sudo twice
    - The > is handled by his own shell, which runs as him, not as root
    - echo can't write text
  answer: 1
  why: Redirection happens before sudo runs. Use echo "hello" | sudo tee -a /etc/motd so the root command does the writing.
- q: You want to add a line to the end of notes.txt without losing what's there. Which do you use?
  options:
    - "echo hi > notes.txt"
    - "echo hi >> notes.txt"
    - "echo hi < notes.txt"
  answer: 1
  why: Two arrows append. One arrow empties the file first.
- q: Which runs cd only if mkdir worked?
  options:
    - "mkdir box; cd box"
    - "mkdir box || cd box"
    - "mkdir box && cd box"
  answer: 2
  why: "&& runs the second command only when the first succeeds. A semicolon always runs it, and || only on failure."
```

## Scribble watch

The Scribble's quietest trick is a single `>` where you meant `>>`. The file is emptied instantly, no question asked, and there is no undo. Before redirecting into any file you care about, especially with `sudo tee`, back it up first (lesson I), and double-check whether you've typed one arrow or two.
