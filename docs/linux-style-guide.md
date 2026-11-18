# Linux course style guide (addendum)

Everything in `docs/lesson-style-guide.md` still applies: the six sections, the golden
rule (jokes in the framing, plain instructions), quiz rules and UK English. This page adds
what's different for the Linux course. Exemplar: `linux/A-what-is-linux.md`. Spec:
`docs/superpowers/specs/2026-11-18-linux-course-design.md`.

## Who it's for

The same learner, now comfortable with Windows and a phone (he did the main course). Assume
no Linux or terminal knowledge at lesson A; by lesson Z he's running a server. Each lesson
may use anything taught in earlier lessons, and nothing from later ones without explaining it.

## Cast on Linux

- **The Operator**: Linux is his home turf. He's still dry and menacing, but noticeably happier
  here. He has opinions about `rm -rf`, root, and people who paste commands they don't understand.
- **Psych** runs **Arch** and mentions it constantly ("I use Arch, by the way"). Still reaches for
  the Whudonk Stick, and now also for `sudo`.
- **Otic** runs **Linux Mint** (Debian family). Cautious; the cow still MOOOOOs at red error text.
- **The Mender** runs **Fedora**, and never brings it up.
- **Propellor Boy & Unicorn Boy** paste `curl ... | sudo bash` from random websites, run commands
  from forums as root, and `chmod 777` everything. They still end up in space.
- **The Scribble** is malware, broken config files, a full disk, a typo in `/etc/fstab`.

## Distro families and tabs

Three families, each with a fixed heading (the words after the family name are free):

```markdown
### On Debian / Ubuntu / Mint
### On Fedora
### On Arch / Manjaro
```

- Put the three together, in that order, when a step differs. The site shows them as tabs
  and remembers the learner's choice; print shows all three.
- A platform block runs until the next `###` heading. **After a group, start a new `###`
  heading** before shared text, or the shared text ends up inside the Arch tab.
- If a step is identical on all three, write it once with no tabs. Don't make tabs that
  say the same thing three times.
- Use real, current defaults: Debian/Ubuntu/Mint use `apt`, `ufw` (Ubuntu/Mint) and
  `.deb`; Fedora uses `dnf`, `firewalld`, SELinux; Arch uses `pacman`, the AUR via a
  helper like `yay` (explain it's community-maintained), and installs very little by default
  (no firewall, no SSH server, often no `sudo` until set up). Service names differ (`ssh` vs
  `sshd`, `apache2` vs `httpd`) and so do group names (`sudo` vs `wheel`): show these.

## Commands

- Commands go in fenced blocks marked `bash`. Don't include the `$` prompt, so they copy
  and paste cleanly. Show output in a separate block (no language) when it helps, trimmed.
- Explain every new command and every flag the first time: what `ls -l` means, letter by letter.
- Use `sudo` only when needed, and say why it's needed.
- Never put a destructive command (`rm -rf`, `dd`, `mkfs`, editing `/etc/fstab`, firewall
  rules that could lock out SSH) in **Do it now** unless the lesson says to do it in a
  **virtual machine** or on a **test file**, and says how to undo it.
- In-text commands, file names and paths go in backticks: `ls`, `/etc/hosts`.

## Levels

Front matter gets `level:`: 1 (A–F), 2 (G–N), 3 (O–U), 4 (V–Z).

```yaml
---
letter: L
title: Package Managers
level: 2
image: psych-smash
---
```

## Length

800–1400 words including the front matter and quiz (code blocks make lessons longer).
Run `.venv/bin/python build.py`; it must print `linux: N lessons`.
