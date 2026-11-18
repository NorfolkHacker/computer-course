---
letter: A
title: What Linux Is
level: 1
image: psych
---

## What went wrong

*The woods. Psych, Otic and the Mender each sit at a laptop on a tree stump.*

**Otic:** I've installed Linux! It's called Mint. It has a leaf on it.

**Psych:** I've installed Linux too. Arch. By the way.

**Otic:** So we've got the same thing?

**Psych:** No. Mine's better. *He types* `sudo apt install vlc` *and presses Enter.* `apt: command not found`.

**Otic:** It works on mine. *He types the same thing. VLC installs.*

**Psych:** Your Linux is broken. *He raises the Whudonk Stick. It begins to crackle.*

**Otic:** *(the cow on his shirt)* MOOOOO!

*The Mender, who has been quietly typing* `sudo dnf install vlc` *on his own laptop, reaches over and lowers the Stick.*

## The Operator says

Finally. Somewhere I can breathe.

There's no such thing as "Linux" the way there's "Windows". There's a heart called Linux, and hundreds of different bodies built around it, each with its own habits. Psych typed a Debian command into an Arch machine and blamed the computer. Classic. Learn which family you're in and which tool that family uses, and the internet's advice suddenly starts working. Get it wrong and you'll spend your evenings shouting at a perfectly healthy machine. Like Psych.

## The Mender's way

Linux looks confusing because there are so many versions. Once you see how they fit together, it's simple.

### The kernel

The **kernel** is the core of an operating system: the part that talks to the hardware (processor, memory, disk, keyboard) and lets programs share it. **Linux** is, strictly, just a kernel. It was started in 1991 by a Finnish student, Linus Torvalds, and is now built by thousands of people and companies. It's **free and open source**: anyone can use it, read its code and change it.

### Distributions ("distros")

A kernel on its own can't do much. To make a usable computer, people bundle it with everything else: the programs that start the machine, a desktop, a web browser, a file manager, and a way to install more software. That bundle is a **distribution**, or **distro**. Ubuntu, Mint, Fedora and Arch are all distros. They all run the same Linux kernel, and most of the same programs, but they differ in:

- how you install software (the **package manager**),
- how often things update,
- what's installed to begin with,
- how it looks.

### The three families

Most distros are built on top of a few big ones, like branches of a family tree. This course covers the three biggest families. In every lesson where a step differs, you'll see tabs: pick yours once and the site remembers.

| Family | Popular members | Installs software with | Feels like |
|---|---|---|---|
| **Debian** | Debian, Ubuntu, Linux Mint | `apt` | Steady and well-trodden. Most online guides assume this family. |
| **Fedora** | Fedora, Red Hat Enterprise Linux (RHEL), Rocky, Alma | `dnf` | Modern and tidy. The family used on many work servers. |
| **Arch** | Arch, Manjaro, EndeavourOS | `pacman` | You build it yourself, and it's always on the newest versions. |

Here's the same job (installing the media player VLC) in each family. Don't run it yet; just notice the pattern. You'll learn what each part means in lessons F and L.

### On Debian / Ubuntu / Mint

```bash
sudo apt install vlc
```

### On Fedora

```bash
sudo dnf install vlc
```

### On Arch / Manjaro

```bash
sudo pacman -S vlc
```

### Desktop and terminal

Linux gives you two ways to work:

- The **desktop**: windows, icons, a menu, a browser. Much like Windows. Lessons C and D.
- The **terminal**: a window where you type commands. It looks old-fashioned, but it's the fastest, most precise way to control a Linux machine, and the only way on most servers. Most of this course lives here, starting in lesson F.

### Which one should you use?

For learning, the honest advice:

- **Linux Mint** (Debian family) if you want it to feel familiar straight away.
- **Fedora** if you want something modern that's close to what businesses use.
- **Arch** later, once you've finished Level 2. It's an excellent teacher but it expects you to know what you're doing.

You don't have to choose for ever. In lesson B you'll set up a **virtual machine**, a pretend computer inside your real one, so you can try all three without risk.

### How to tell which Linux you're on

On any Linux machine, this command shows the distro's name and family:

```bash
cat /etc/os-release
```

Look for the `NAME=` line, and `ID_LIKE=`, which names the family it's built on. For example, Mint shows `ID_LIKE="ubuntu debian"`.

## Do it now

You don't need Linux installed yet.

1. Copy the family table above onto paper, or into a note on your phone.
2. Choose the distro you'll start with (Mint, Fedora or Arch), and circle its family.
3. Click a tab in the VLC example above and choose your family. Go to another lesson page and back: your choice should stick.
4. Look up your distro's official website (`linuxmint.com`, `fedoraproject.org` or `archlinux.org`) and find its **Download** page. Don't download anything yet; lesson B does that properly.

You've done it when you can say your distro, its family, and which command that family uses to install software.

## Quiz

```quiz
- q: What is Linux, strictly speaking?
  options:
    - A company that makes computers
    - The kernel, the core that talks to the hardware
    - A version of Windows
  answer: 1
  why: Linux is the kernel. Distros like Mint and Fedora wrap a full system around it.
- q: Psych runs Arch. Which command installs software on his machine?
  options:
    - apt
    - dnf
    - pacman
  answer: 2
  why: Arch uses pacman. apt is the Debian family's tool and dnf is Fedora's, which is why Psych's apt command failed.
- q: Which command tells you which distro and family you're running?
  options:
    - cat /etc/os-release
    - whoami
    - sudo apt install vlc
  answer: 0
  why: /etc/os-release names the distro, and its ID_LIKE line names the family.
```

## Scribble watch

The Scribble's favourite trick on Linux is a forum post that says "just paste this into your terminal". Commands written for one family can fail, or do something different, on another, and some are deliberately harmful. Before you run anything from the internet, check it's for your family, and that you understand what it does. If you don't, don't paste it. Ask.
