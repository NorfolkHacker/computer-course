---
letter: N
title: Processes
level: 2
image: mooo
---

## What went wrong

*Otic's kitchen. Otic's Mint laptop fan is roaring. The mouse pointer moves in slow jerks.*

**Otic:** Everything's frozen. The web browser's gone grey.

**Psych:** Something's eating your computer. On Arch I'd find it in seconds. I use Arch, by the way.

**Otic:** So find it.

**Psych:** Easier to restart. *He reaches round the back of the laptop for the power button and holds it down.*

*The screen goes black. The fan stops. Silence.*

**Otic:** My essay. I hadn't saved my essay.

**Otic's shirt:** MOOOOOOOOO!

*The Mender, passing with a teapot, glances at the dark screen. A tiny scrap of Scribble crawls out of the vent, satisfied, and drifts off into the woods.*

## The Operator says

Every running program is a process, and every process is mine. I can stop any of them. I usually don't. Remarkable restraint.

When one program misbehaves, you don't pull the plug on the whole machine and everything else you had open. You find the one process causing trouble and stop it: politely first, firmly only if you must. Today you get my power. Use it more kindly than I do.

## The Mender's way

When a computer is slow or stuck, the answer is almost always one program. Here's how to find it and stop it.

### What a process is

A **process** is a program that's currently running. Open two terminal windows and you have (at least) two processes. Each one gets a **PID** (process ID), a number that identifies it until it ends. Every process also has an owner: the user who started it.

### Listing processes: ps and pgrep

`ps` (**process status**) lists processes. On its own it shows only the ones in this terminal. To see everything:

```bash
ps aux
```

`a` means all users, `u` shows the owner and resource use, and `x` includes processes not attached to a terminal (most background ones). The useful columns:

| Column | Means |
|---|---|
| `USER` | who owns it |
| `PID` | its ID |
| `%CPU` / `%MEM` | how much processor and memory it's using |
| `COMMAND` | the program |

The list is long, so pipe it through `grep` (lesson J) or `less`. Or use `pgrep`, which finds PIDs by name; `-a` shows the full command too:

```bash
pgrep -a firefox
```

### Watching live: top and htop

`top` shows processes updating every few seconds, busiest at the top:

```bash
top
```

Press <kbd>Shift</kbd> + <kbd>P</kbd> to sort by CPU, <kbd>Shift</kbd> + <kbd>M</kbd> to sort by memory, and <kbd>q</kbd> to quit.

`htop` does the same job with colour, a mouse and clearer controls. Install it if it isn't there:

### On Debian / Ubuntu / Mint

```bash
sudo apt install htop
```

### On Fedora

```bash
sudo dnf install htop
```

### On Arch / Manjaro

```bash
sudo pacman -S htop
```

### Using htop

```bash
htop
```

The bars at the top show each processor core and memory. Click a column heading (or press <kbd>F6</kbd>) to sort by it; **CPU%** and **MEM%** are the useful ones. <kbd>F3</kbd> searches by name, <kbd>F9</kbd> stops the selected process (it asks which signal; see below), and <kbd>F10</kbd> or <kbd>q</kbd> quits.

### Stopping a process: kill

`kill` sends a **signal** to a process. Despite the name, a signal is a message, and the default one is a polite request.

```bash
kill 4321
```

That sends **TERM** (terminate) to PID 4321: "please finish up and close". Most programs save what they can and exit. If a program is truly stuck and ignores it, wait a few seconds, then send **KILL**:

```bash
kill -9 4321
```

`-9` is the number for KILL. The system stops the process instantly; the program gets no chance to save or tidy up. Use it only as a last resort.

You can only stop your own processes. Stopping another user's or a system process needs `sudo`, and you rarely should.

### By name: pkill and killall

`pkill` and `killall` stop processes by name instead of PID:

```bash
pkill firefox
killall firefox
```

`pkill` matches part of a name, so check first with `pgrep -a` and the same word. `killall` needs the exact name. (If `killall` isn't found, it's in a package called `psmisc`.)

### Foreground and background

A command normally runs in the **foreground**: it holds the terminal until it finishes. `sleep 300` just waits 300 seconds, which makes it perfect for practice.

| You do | It does |
|---|---|
| Add `&` at the end | Starts the command in the **background**; you get the prompt straight back |
| <kbd>Ctrl</kbd> + <kbd>Z</kbd> | Pauses the foreground command |
| `bg` | Lets the paused command carry on in the background |
| `fg` | Brings a background command back to the foreground |
| `jobs` | Lists this terminal's background and paused commands, numbered `[1]`, `[2]`... |
| <kbd>Ctrl</kbd> + <kbd>C</kbd> | Stops the foreground command (lesson F) |

`fg %2` brings back job number 2. Background jobs belong to this terminal; close it and they usually stop.

### Memory and load: free and uptime

```bash
free -h
```

`-h` means **human-readable** (sizes in G and M). Look at the **available** column: that's how much memory programs can still use. Linux uses spare memory for a cache, so a small **free** number is normal; a small **available** one isn't. **Swap** is disk space used as overflow memory. If it's heavily used, the machine slows down.

```bash
uptime
```

```
 10:42:01 up 3 days,  2:11,  1 user,  load average: 0.52, 0.61, 0.70
```

The **load average** is roughly how many processes were running or waiting, averaged over the last 1, 5 and 15 minutes. Compare it with your number of processor cores (`nproc` tells you). Below that number is fine; well above it means things are queuing.

### The graphical way

Every desktop has a graphical tool that does the same as `htop`: usually called **System Monitor**, found by searching the app menu. Some newer GNOME desktops use an app called **Resources** instead. Select a process and choose **End** (TERM) or **Kill** (KILL); the wording varies slightly between desktops.

## Do it now

Safe practice with a harmless `sleep` command, then a look round.

1. Run `sleep 300 &`. Note the job number and PID it prints.
2. Run `jobs`, then `pgrep -a sleep`. The PIDs should match.
3. Start another one in the foreground: `sleep 400`. Press <kbd>Ctrl</kbd> + <kbd>Z</kbd> to pause it, then `bg` to let it carry on, then `jobs` to see both.
4. Bring one back: `fg %1`. Press <kbd>Ctrl</kbd> + <kbd>C</kbd> to stop it.
5. Stop the other politely with `kill` and its PID (from `pgrep -a sleep`). Run `jobs` to check it's gone.
6. Install and open `htop`. Sort by **MEM%** and find the biggest memory user. Press <kbd>q</kbd>.
7. Run `free -h`, `uptime` and `nproc`, and decide whether your machine is busy.

You've done it when both `sleep` commands are gone and you can say which program uses the most memory on your machine.

## Quiz

```quiz
- q: A program has frozen. What should you try first?
  options:
    - Hold down the power button
    - "kill -9 straight away"
    - "kill with its PID, which sends TERM and lets it close properly"
  answer: 2
  why: TERM asks politely so the program can save and tidy up. KILL (-9) is a last resort, and pulling the power loses everything else too.
- q: How do you start a long command and get the prompt back immediately?
  options:
    - Put & at the end of it
    - Press Ctrl+C
    - Run it with sudo
  answer: 0
  why: A trailing & runs the command in the background. Ctrl+C stops it instead.
- q: In free -h, which column shows how much memory programs can still use?
  options:
    - free
    - available
    - swap
  answer: 1
  why: Linux uses spare memory as a cache, so free is often small. available is the real figure.
```

## Scribble watch

The Scribble sometimes hides as a process with a dull name, quietly using all your processor to mine cryptocurrency for someone else. If your fan roars when you're doing nothing, open `htop`, sort by **CPU%**, and look at the top. If you don't recognise the name, look it up (lesson H) before stopping it, and if it's genuinely suspicious, ask for help on your distro's forum.
