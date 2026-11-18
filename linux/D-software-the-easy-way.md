---
letter: D
title: Software the Easy Way
level: 1
image: propellor-boy
---

## What went wrong

*The woods. Propellor Boy and Unicorn Boy crowd round a laptop running Mint.*

**Propellor Boy:** I need a photo editor. Search "free photo editor linux download".

**Unicorn Boy:** First result: "SuperPhotoPro_LINUX_FREE_full_crack.sh". Big green button!

*He downloads it, right-clicks, and runs it. A terminal flashes. It asks for his password. He types it.*

**Otic:** *(from behind a tree)* Wait, Mint has a Software Manager —

**Propellor Boy:** Too slow, Otic!

*The laptop fan roars. The screen fills with scrolling text. Something under the keyboard goes WHOOSH.*

**Otic:** *(the cow on his shirt)* MOOOOO!

*Propellor Boy and Unicorn Boy rise gently through the trees and into space.*

## The Operator says

On Windows you find software by searching the web and hoping. On Linux you've got shops, run by your distro, with thousands of programs, all free, all checked. And still people go to "SuperPhotoPro_crack.sh" and hand it their password.

Typing your password into an installer gives it the keys to the whole machine. Get software from your distro's store and the hard work of checking it has been done for you. That's one less luser on my list.

## The Mender's way

Every Linux desktop has an app store. It's the safe, easy way to install software, and to remove it again.

### Your software store

Each family's store has a different name. Pick your tab.

### On Debian / Ubuntu / Mint

**Mint**: open **Menu** and type `software`, then choose **Software Manager**. It shows both Mint's own packages and **Flatpaks** from **Flathub** (explained below), already switched on.

**Ubuntu**: open **App Center** from the dock (an orange shopping-bag icon). It mostly offers **Snaps** (explained below) and Ubuntu's own packages.

### On Fedora

Open **Software** (also called **GNOME Software**) from Activities. If you said yes to third-party repositories when you set Fedora up, it shows apps from Fedora and from Flathub. If you didn't: open **Software**, click the menu button (three lines, top-right) → **Software Repositories**, and click **Enable** next to the third-party repositories.

On Fedora's KDE edition, the store is **Discover** instead.

### On Arch / Manjaro

**Arch** installs only what you asked for, so your store depends on the desktop you picked:

- **GNOME**: **Software** (if it's not there, install the `gnome-software` package once you reach lesson L).
- **KDE Plasma**: **Discover** (package `discover`).

To use Flathub on Arch, install Flatpak with this one command. You'll learn what `sudo` and `pacman` mean in lessons F and L; it asks for your password because it changes the system.

```bash
sudo pacman -S flatpak
```

Arch's `flatpak` package sets up Flathub for you. Log out and back in afterwards.

**Manjaro** has its own store, **Add/Remove Software** (also called **Pamac**). To see Flatpaks, open its menu → **Preferences** and switch on **Flatpak** support.

### Installing an app

The stores all work the same way:

1. Open your store.
2. Click the search box (or magnifying glass) and type what you want, for example `vlc`.
3. Click the app in the results to open its page. Read the description and check the publisher.
4. Click **Install**.
5. Type your password if asked. Installing software changes the system, so the store checks that you're allowed to.
6. When it's done, the button changes to **Launch** or **Open**. The app is also in your menu now.

### Flatpak and Flathub

A **Flatpak** is an app packaged so that it runs the same on any distro, carrying the bits it needs with it. **Flathub** (`flathub.org`) is the main shop for Flatpaks. It's useful when your distro's own version of an app is old, or missing.

- Flatpak apps run in a **sandbox**: a fenced-off area, so the app can only reach the files and devices it's been given permission to.
- On Flathub, look for the **verified** tick next to the publisher's name. It means the app is published by the people who actually make it.
- In **Software** and **Discover**, if an app is available from more than one source, there's a menu on its page (usually labelled with the source, such as **Fedora Linux** or **Flathub**) to choose which to install.

On Ubuntu, Flatpak isn't installed by default. You can add it later with the package manager (lesson L), but App Center already covers most needs.

### Snap

A **Snap** is Ubuntu's own version of the same idea, run by Canonical, the company behind Ubuntu. Ubuntu's App Center uses Snaps for many apps, including Firefox. They work fine. Mint deliberately leaves Snaps switched off and uses Flatpak instead. You don't need to choose: use whatever your store offers.

### Why the store, not a random download

- **Checked**: the distro or Flathub builds or reviews what's in the store. A random website could be anyone.
- **Updated**: store apps update with the rest of your system (lesson M). A download from a website never updates itself.
- **Removable**: the store can remove everything it installed, cleanly.

If an app's own website offers a download, look first for a **Flathub** link or instructions for your distro on that same site. Only use a `.deb` (Debian family) or `.rpm` (Fedora) from the maker's official site, never from a download site.

### Removing an app

1. Open your store.
2. Go to the list of installed apps: **Installed** in Software and Discover; **Manage** in App Center's left-hand sidebar; in Software Manager, the menu button (top-right) → **Show installed applications**. Or simply search for the app as before.
3. Find the app, open it, and click **Remove** or **Uninstall** (the word varies between stores).
4. Confirm, and type your password if asked.

Your own files made with the app (documents, photos) stay where they were.

## Do it now

In your VM:

1. Open your software store.
2. Search for `GNOME Chess`, a small, free chess game.
3. Open its page, check where it comes from, and install it.
4. Find it in your menu and open it. Make one move.
5. Close it, go back to the store and remove it.

You've done it when GNOME Chess has been installed, played, and removed again, without opening a web browser once.

## Quiz

```quiz
- q: Propellor Boy needs a photo editor. Where should he get it?
  options:
    - The first website that offers a free download
    - His distro's software store, or Flathub
    - A file a forum post links to, run with his password
  answer: 1
  why: Store and Flathub apps are checked and kept up to date. A random download could do anything once you give it your password.
- q: What is Flathub?
  options:
    - The main online shop for Flatpak apps, which work on any distro
    - Arch's package manager
    - A kind of virus
  answer: 0
  why: Flathub is the main store for Flatpaks, which run sandboxed on any distro.
- q: You installed Arch with KDE Plasma. Which app store do you look for?
  options:
    - Software Manager
    - App Center
    - Discover
  answer: 2
  why: Discover is KDE's store. Software Manager is Mint's and App Center is Ubuntu's.
```

## Scribble watch

The Scribble hides in "cracked" paid software and shell scripts from download sites. The moment you type your password into one, it owns the machine. If you can't find an app in your store or on Flathub, ask somebody you trust before installing it another way. And never type your password for an installer you got from a stranger.
