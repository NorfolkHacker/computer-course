---
letter: Q
title: Scheduled Jobs
level: 3
image: clink
---

## What went wrong

*Otic's living room. Midnight. Otic sits in front of his laptop with an alarm clock and a flask of tea.*

**Psych:** What are you doing?

**Otic:** Waiting for midnight. Then I run my backup script. I do it every night.

**Psych:** Amateur. Let the computer do it. *He types* `crontab -e`. *A black screen full of tildes appears.* `~` `~` `~`

**Psych:** *(pressing keys)* Exit. Quit. Stop. *Escape.* Please.

**Otic:** *(the cow on his shirt)* MOOOOO!

*Twenty minutes later Psych escapes, having saved the line* `0 0 * * * backup-folder ~/Documents`. *At midnight, nothing happens. Nothing happens the next night either. He does not notice for three weeks.*

**Psych:** Cron's broken. On Arch. Which is impossible.

## The Operator says

Somewhere there's a server that's been "backing up nightly" since 2019 and hasn't saved a byte. I know, because I set it up. For a user I didn't like.

Scheduling is how Linux does chores while you sleep: backups, clean-ups, updates. The catch is that a scheduled job runs alone, in the dark, with nobody watching. If it fails, it fails silently. So the real skill isn't writing the schedule. It's making the job leave a note saying what happened.

## The Mender's way

There are two ways to run things on a timetable: **cron**, the classic, and **systemd timers**, the modern one. Both work on all three families.

### Is cron there?

**cron** is a background service that checks a timetable every minute and runs anything that's due.

### On Debian / Ubuntu / Mint

Installed and running already. The service is called `cron`.

### On Fedora

Fedora Workstation doesn't include it any more (other editions may). The package is **cronie** and the service is called `crond`. If `crontab` says "command not found":

```bash
sudo dnf install cronie
sudo systemctl enable --now crond
```

### On Arch / Manjaro

Not installed. Install **cronie** and switch it on (`sudo` because you're changing the system):

```bash
sudo pacman -S cronie
sudo systemctl enable --now cronie
```

### What enable --now means

`systemctl enable --now` means "start this service now, and every time the computer boots". Lesson S covers it fully. Psych skipped this step: he installed cron but never switched it on, so nothing ever read his timetable.

### Editing your timetable

Each user has their own timetable, the **crontab**. Edit it with:

```bash
crontab -e
```

The first time, Debian, Ubuntu and Mint ask which editor you want: choose **nano**. Fedora sets nano as the default editor already. Arch goes straight into **vi** (Psych's black screen of tildes), or gives an error if vi isn't installed, unless you say otherwise. Ask for nano instead:

```bash
EDITOR=nano crontab -e
```

To make that permanent, add `export EDITOR=nano` to `~/.bashrc` (lesson O). To escape vi if you land in it: press <kbd>Esc</kbd>, type `:q!` and press <kbd>Enter</kbd>.

`crontab -l` lists your jobs without editing.

### The five fields

Each job is one line: five time fields, then the command.

```
# min  hour  day-of-month  month  day-of-week  command
  30   2     *             *      *            /home/otic/.local/bin/backup-folder /home/otic/Documents
```

| Field | Range | `*` means |
|---|---|---|
| minute | 0–59 | every minute |
| hour | 0–23 | every hour |
| day of month | 1–31 | every day |
| month | 1–12 | every month |
| day of week | 0–7 (0 and 7 are Sunday) | every day |

More examples:

| Line starts with | Runs |
|---|---|
| `0 * * * *` | on the hour, every hour |
| `*/15 * * * *` | every 15 minutes |
| `0 9 * * 1-5` | 9:00 on weekdays |
| `0 3 1 * *` | 3:00 on the 1st of each month |
| `@reboot` | once, when the machine starts |

To check a line in plain English, paste the five fields into **crontab.guru** in a browser.

### Three cron traps

1. **Short PATH.** cron doesn't read your `~/.bashrc`, so it may not find your scripts. Use full paths, like `/home/otic/.local/bin/backup-folder`, not `~` or bare names.
2. **The % sign.** In a crontab, `%` means "new line". Write `\%` if a command needs one (for example `date +\%F`). Better: put the command in a script.
3. **Silence.** Output goes nowhere useful. Send it to a log file.

### Logging output

Add this to the end of the line:

```
30 2 * * * /home/otic/.local/bin/backup-folder /home/otic/Documents >> /home/otic/cron.log 2>&1
```

`>>` appends normal output to the log (lesson J). `2>&1` sends error messages to the same place. Now you can read `~/cron.log` in the morning and see exactly what happened.

### systemd timers: the modern way

A **systemd timer** is a pair of small text files: a **service** file that says *what* to run, and a **timer** file that says *when*. They take more typing than cron, but they log automatically, can catch up on runs missed while the computer was off, and need nothing extra installed.

Your own timers live in `~/.config/systemd/user/`. System-wide ones go in `/etc/systemd/system/` and need `sudo`.

1. Make the folder:

```bash
mkdir -p ~/.config/systemd/user
```

2. Create `~/.config/systemd/user/backup.service`:

```ini
[Unit]
Description=Back up Documents

[Service]
Type=oneshot
ExecStart=%h/.local/bin/backup-folder %h/Documents
```

`%h` means your home folder. `Type=oneshot` means "run once and finish".

3. Create `~/.config/systemd/user/backup.timer` (same name, different ending):

```ini
[Unit]
Description=Back up Documents daily

[Timer]
OnCalendar=*-*-* 02:30
Persistent=true

[Install]
WantedBy=timers.target
```

`OnCalendar` reads as year-month-day hour:minute, so this means 02:30 every day. `Persistent=true` runs it at the next chance if the computer was off at 02:30.

4. Tell systemd to reload, then start the timer. `--user` means "my own services, not the system's", so no `sudo`:

```bash
systemctl --user daemon-reload
systemctl --user enable --now backup.timer
```

5. Check when it will next run:

```bash
systemctl --user list-timers
```

To test the job straight away, without waiting: `systemctl --user start backup.service`. To read its output: `journalctl --user -u backup.service`.

Your user timers run while you're logged in. To keep them running when you're not, run `sudo loginctl enable-linger $USER` once.

To check an `OnCalendar` value before you use it:

```bash
systemd-analyze calendar "Mon..Fri 09:00"
```

### at: just once, later

`at` runs a command once, at a set time. It may need installing (package **at**); on Fedora and Arch also run `sudo systemctl enable --now atd`.

```bash
echo "touch ~/at-was-here" | at now + 5 minutes
atq
```

`atq` lists waiting jobs; `atrm` followed by the job number cancels one.

## Do it now

1. Make sure cron is installed and running for your family (above).
2. Run `EDITOR=nano crontab -e` and add this line at the bottom, using your own user name:
   `*/2 * * * * date >> /home/YOURNAME/cron-test.log 2>&1`
3. Save and exit. Run `crontab -l` to check it's there.
4. Wait four minutes, then run `cat ~/cron-test.log`. You should see two or more dates.
5. Run `crontab -e` again and delete the line. Save.

You've done it when the log shows the job ran on its own, and `crontab -l` no longer lists it. Then delete the log: `rm ~/cron-test.log`.

## Quiz

```quiz
- q: Psych's nightly job on Arch never ran. What was the likely cause?
  options:
    - Arch doesn't support scheduled jobs
    - cronie wasn't installed and enabled
    - Midnight is written 24 * * * *
  answer: 1
  why: Arch doesn't include cron. Install cronie and run sudo systemctl enable --now cronie.
- q: What does the line 0 9 * * 1-5 mean?
  options:
    - Every 9 minutes, five times
    - 9:00 on the 1st to 5th of each month
    - 9:00 Monday to Friday
  answer: 2
  why: Minute 0, hour 9, any day of the month, any month, days of the week 1 to 5 (Monday to Friday).
- q: How do you list your systemd user timers and when they run next?
  options:
    - systemctl --user list-timers
    - crontab -l
    - at --timers
  answer: 0
  why: list-timers shows each timer with its next and last run. crontab -l only shows cron jobs.
```

## Scribble watch

The Scribble likes jobs nobody checks. A backup that has failed silently for months feels exactly like one that works, right up until you need it. Every scheduled job should write to a log or the journal. Once a month, look at the log, and actually open one of the backups to check the files are inside.
