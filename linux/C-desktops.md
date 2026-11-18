---
letter: C
title: Desktops
level: 1
image: huh
---

## What went wrong

*The woods. Otic sits down at Psych's laptop.*

**Otic:** Where's the menu? Bottom-left. There's always a menu bottom-left.

**Psych:** Not on mine. I use Arch, by the way. With GNOME.

*Otic clicks the bottom-left corner. Nothing. He clicks it harder. Nothing.*

**Otic:** It's broken. There's no Start button.

**Psych:** There's an Activities thing somewhere.

**Otic:** Where's somewhere?

*He gives up and holds down the laptop's power button. The screen goes black mid-update.*

**Otic:** *(the cow on his shirt)* MOOOOO!

## The Operator says

Linux doesn't have *a* desktop. It has dozens, and the luser always sits down at the one he's never seen.

The bit of Linux you look at all day is a separate program, and different distros pick different ones. Learn the three big ones and you can sit at almost any Linux machine without your cow going off. And for pity's sake, stop shutting computers down with the power button. That's what I do to *other people's* machines.

## The Mender's way

The look of a Linux machine depends on its desktop. Learn the idea once, then learn where your desktop keeps things.

### What a desktop environment is

A **desktop environment** (**DE**) is the set of programs that draw what you see: the panel, the menu, windows, the settings app and the file manager. Windows has exactly one. On Linux you can choose. Underneath, the programs you run are the same: Firefox is Firefox whichever DE you use.

| Desktop | Default on | Feels like | Menu | Settings app | File manager |
|---|---|---|---|---|---|
| **GNOME** | Fedora, Ubuntu | Clean and minimal, works by searching | **Activities** (top-left) | **Settings** | **Files** (also called **Nautilus**) |
| **KDE Plasma** | Fedora KDE, Kubuntu, Manjaro KDE | Like Windows, with a setting for everything | **Application Launcher** (bottom-left) | **System Settings** | **Dolphin** |
| **Cinnamon** | Linux Mint | Like Windows 7: menu, panel, taskbar | **Menu** (bottom-left) | **System Settings** | **Nemo** (shown as **Files** in the menu) |

On Arch, you have whichever you picked in `archinstall`.

### Getting around GNOME

1. Press the <kbd>Super</kbd> key (the one with the Windows logo), or click **Activities** in the top-left corner. This is the **Activities overview**: all your open windows, spread out.
2. Start typing the name of an app (`files`) and press <kbd>Enter</kbd> to open it.
3. To see every app, click **Show Apps** (the grid of dots at the end of the dock). The **dock** is the row of app icons; on Ubuntu it's always on the left side of the screen, on Fedora it appears at the bottom of the overview.
4. To close a window, click the **×** at its top-right.

The menu at the very top-right (click the network, sound or battery icons) holds volume, Wi-Fi, and the power button.

### Getting around KDE Plasma

1. Click the **Application Launcher** at the bottom-left of the panel (the **panel** is the bar along the bottom), or press <kbd>Super</kbd>.
2. Type an app's name, or browse the categories.
3. Open windows appear in the panel as a **taskbar**, as on Windows.
4. Right-click almost anything for more options. Plasma loves options.

### Getting around Cinnamon

1. Click **Menu** at the bottom-left, or press <kbd>Super</kbd>.
2. Type an app's name, or browse the categories on the right.
3. Open windows appear in the panel along the bottom, as on Windows.

### Workspaces

A **workspace** (KDE calls it a **virtual desktop**) is an extra, empty desktop. Put your browser on one and your email on another, and switch between them instead of piling windows on top of each other.

- **GNOME**: open the Activities overview. Your workspaces appear as strips; drag a window onto one. GNOME adds a fresh empty workspace automatically. <kbd>Super</kbd> + <kbd>Page Down</kbd> and <kbd>Super</kbd> + <kbd>Page Up</kbd> switch between them.
- **KDE Plasma**: press <kbd>Super</kbd> + <kbd>W</kbd> for the **Overview**, which shows your desktops at the top. Add more in **System Settings** → **Virtual Desktops**.
- **Cinnamon**: press <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>Up</kbd> to see all workspaces. <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>Left</kbd> and <kbd>Right</kbd> switch between them.

### Settings

Open the settings app by name from the menu: **Settings** on GNOME, **System Settings** on Plasma and Cinnamon. Each has a search box. Try it now: search for `display` to change screen size, or `keyboard` to check your layout is **English (UK)**.

### Locking, logging out and shutting down

- **Lock** the screen when you walk away. Your programs keep running; your password gets you back in. <kbd>Super</kbd> + <kbd>L</kbd> works on GNOME and Plasma. On Cinnamon use <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>L</kbd>.
- **Log out** closes all your programs and returns to the **login screen** (the screen where you type your password).
- **Shut down** (some desktops say **Power Off**) closes everything safely and turns the machine off.

Where to find them:

- **GNOME**: click the top-right icons, then the **power** icon for **Suspend**, **Restart**, **Power Off** and **Log Out**. The padlock icon locks the screen.
- **KDE Plasma**: open the **Application Launcher**; the buttons at its bottom-right are **Sleep**, **Restart**, **Shut Down** and a **Leave** menu that holds **Log Out** and **Lock**.
- **Cinnamon**: open **Menu**; the buttons down its left side include **Lock Screen**, **Log Out** and **Quit** (which offers **Shut Down**).

Never hold the power button except as a last resort when the machine has frozen solid. Cutting the power mid-update can leave Linux unable to start.

### Trying another desktop

You can install a second desktop on the same machine. At the login screen, click your name, then look for a small gear or session icon (usually near the password box or the bottom corner) to choose which desktop to start. You'll learn the commands to install one in lesson L. Mixing desktops leaves you with two of many things (two settings apps, two file managers), so try it in a spare VM first.

## Do it now

Do this in the VM you made in lesson B.

1. Open your menu (Activities, Application Launcher or Menu) and start your file manager by typing its name.
2. Open your settings app and use its search box to find **keyboard**. Check the layout is **English (UK)**.
3. Open a second app (the web browser), then move it to a second workspace and switch back and forth.
4. Lock the screen, then unlock it with your password.
5. Shut the VM down properly from the desktop's own power menu.

You've done it when the VM window closes by itself after a clean shutdown, without you touching VirtualBox's own close button.

## Quiz

```quiz
- q: On Fedora's or Ubuntu's GNOME desktop, how do you find an app?
  options:
    - Click the bottom-left corner for the Start menu
    - Press the Super key (or click Activities) and type its name
    - Hold down the power button
  answer: 1
  why: GNOME has no Start menu. The Super key opens the Activities overview, where you type to search.
- q: Which file manager comes with KDE Plasma?
  options:
    - Dolphin
    - Nemo
    - Nautilus
  answer: 0
  why: Plasma uses Dolphin. Nemo is Cinnamon's (Mint's) and Nautilus, called Files, is GNOME's.
- q: What's the right way to turn off a Linux desktop?
  options:
    - Hold the power button
    - Close the last window
    - Use the desktop's own Shut Down or Power Off option
  answer: 2
  why: The desktop's shutdown closes everything safely. Holding the power button can damage an update in progress.
```

## Scribble watch

The Scribble loves an unlocked desktop. You pop out for a cup of tea, and anyone passing can read your email or run a command as you. Lock the screen every time you step away: <kbd>Super</kbd> + <kbd>L</kbd> on GNOME and Plasma, <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>L</kbd> on Cinnamon. It takes half a second.
