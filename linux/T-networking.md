---
letter: T
title: Networking and Firewalls
level: 3
image: mooo
---

## What went wrong

*Otic's living room. Otic is SSH'd into his Mint laptop from his phone, feeling powerful.*

**Otic:** I've read that every computer should have a firewall. I'm turning mine on. *He types* `sudo ufw enable`.

```
Command may disrupt existing ssh connections. Proceed with operation (y|n)?
```

**Otic:** That sounds like a formality. *He types* `y`.

*His phone screen freezes. The SSH session goes silent. The laptop is upstairs, behind a locked door, and the key is in Psych's pocket. Psych is in Margate.*

**Otic:** *(the cow on his shirt)* MOOOOO!

*Faintly, from the coast:* **Psych:** Not a problem! Just SSH back in!

## The Operator says

Every admin has locked themselves out with a firewall exactly once. I did it to a server in a building with no stairs. I had to wait for the lift engineer.

Networking feels like magic until you can answer four questions: what's my address, where's my way out, can I reach anything, and do names turn into addresses? One command each. Then the firewall: a bouncer on the door. Fine. Just make sure he lets *you* in first.

## The Mender's way

Check a connection one step at a time, then switch on a firewall safely.

### Addresses

An **IP address** identifies a device on a network, like `192.168.1.50`. Home networks use **private** addresses, which only work inside your home:

| Range | Typical use |
|---|---|
| `192.168.x.x` | most home routers |
| `10.x.x.x` | some routers, offices, VMs |
| `172.16.x.x` to `172.31.x.x` | offices, containers |
| `127.0.0.1` | **localhost**: this computer talking to itself |

### Question 1: what's my address? ip a

```bash
ip a
```

Each **interface** (network connection) is listed: `lo` is localhost, `en...` is wired, `wl...` is Wi-Fi. Your address is on the `inet` line, before the `/`.

### Question 2: where's my way out? ip r

The **gateway** is the device (your router) that passes traffic to the internet.

```bash
ip r
```

```
default via 192.168.1.1 dev wlp2s0 proto dhcp metric 600
```

`ip r` (short for `ip route`) shows the **routes**. `default via` is your gateway.

### Question 3: can I reach it? ping

`ping` sends a tiny message and waits for a reply. `-c 4` sends four and stops (without it, press <kbd>Ctrl</kbd> + <kbd>C</kbd>).

```bash
ping -c 4 192.168.1.1
ping -c 4 1.1.1.1
```

If the gateway answers but `1.1.1.1` (a public server) doesn't, the problem is beyond your router.

### Question 4: do names work? DNS

**DNS** turns names like `fedoraproject.org` into addresses. If `ping 1.1.1.1` works but `ping fedoraproject.org` doesn't, DNS is broken.

### On Debian / Ubuntu / Mint

DNS is handled by **systemd-resolved**. See which DNS servers you're using:

```bash
resolvectl status
```

`/etc/resolv.conf` will just say `nameserver 127.0.0.53`: that's resolved, passing questions on.

### On Fedora

Also **systemd-resolved**, so `resolvectl status` works, and `/etc/resolv.conf` points at `127.0.0.53`.

### On Arch / Manjaro

It depends on what you installed. Usually NetworkManager writes the DNS servers straight into `/etc/resolv.conf`:

```bash
cat /etc/resolv.conf
```

`resolvectl status` only works if you've enabled `systemd-resolved`.

### Looking names up: dig and nslookup

`dig` asks DNS directly and shows the answer. `nslookup` is an older, simpler tool that comes with it. The package name differs:

### On Debian / Ubuntu / Mint

```bash
sudo apt install bind9-dnsutils
```

(Older guides call it `dnsutils`.)

### On Fedora

```bash
sudo dnf install bind-utils
```

### On Arch / Manjaro

```bash
sudo pacman -S bind
```

### Using dig

```bash
dig fedoraproject.org +short
nslookup fedoraproject.org
```

`+short` prints only the address.

### What's listening? ss

A **port** is a numbered door on a computer; each service listens on its own (SSH is 22, web is 80 and 443). `ss` shows them:

```bash
sudo ss -tulpn
```

- `-t` **T**CP and `-u` **U**DP (the two kinds of connection)
- `-l` only **l**istening ports
- `-p` show the **p**rogram (needs `sudo` for other users' programs)
- `-n` show **n**umbers, not names

An address of `0.0.0.0` or `[::]` means "listening to everyone"; `127.0.0.1` means "only this computer".

### NetworkManager and nmcli

**NetworkManager** runs the network on Mint, Ubuntu, Fedora and Manjaro desktops; it's what the Wi-Fi icon talks to. On plain Arch it's there only if you installed it. `nmcli` is its terminal tool:

```bash
nmcli device status
nmcli connection show
nmcli device wifi list
```

To join a Wi-Fi network (`--ask` makes it prompt for the password, so the password isn't saved in your command history):

```bash
nmcli --ask device wifi connect "Network Name"
```

### /etc/hosts: your own name list

`/etc/hosts` is checked before DNS. Adding a line gives a machine on your network a name:

```
192.168.1.50    mint-laptop
```

Back it up first (`sudo cp /etc/hosts /etc/hosts.bak`), then edit with `sudo nano /etc/hosts`. Now `ping mint-laptop` works.

### Firewalls

A **firewall** decides which incoming connections are allowed. **Golden rule: if you're connected over SSH, allow SSH before you switch the firewall on.** That's what Otic missed.

### On Debian / Ubuntu / Mint

**ufw** ("uncomplicated firewall") is installed but switched off.

```bash
sudo ufw status verbose
sudo ufw allow ssh
sudo ufw enable
```

`allow ssh` opens port 22. Later, `sudo ufw allow http` would open port 80. Undo a rule with `sudo ufw delete allow ssh`; switch the whole thing off with `sudo ufw disable`.

### On Fedora

**firewalld** is already running. Rules belong to **zones**; your connection uses the default one.

```bash
sudo firewall-cmd --list-all
sudo firewall-cmd --add-service=http --permanent
sudo firewall-cmd --reload
```

`--permanent` saves the rule; `--reload` loads saved rules. Without `--permanent`, a rule vanishes at the next reload or reboot. SSH is already allowed. Undo with `--remove-service=http --permanent`, then reload.

### On Arch / Manjaro

Plain Arch has **no firewall**. Pick **one** of ufw or firewalld (never both). With ufw:

```bash
sudo pacman -S ufw
sudo ufw allow ssh
sudo systemctl enable --now ufw
sudo ufw enable
```

Arch needs the service enabled as well as `ufw enable`. Manjaro may already include ufw: check with `sudo ufw status` first.

### When it's not working

Work through the four questions in order: `ip a`, `ip r`, `ping` the gateway, then `dig` a name. The first one that fails tells you where to look.

## Do it now

All of this only reads information, except the firewall check, which changes nothing.

1. Run `ip a` and write down your address.
2. Run `ip r` and write down your gateway.
3. `ping -c 4` your gateway, then `ping -c 4 1.1.1.1`.
4. Install your family's DNS tools and run `dig fedoraproject.org +short`.
5. Run `sudo ss -tulpn` and find which program is on port 22, if any.
6. Run `nmcli device status`.
7. Check your firewall's status: `sudo ufw status` or `sudo firewall-cmd --list-all`.

Only switch a firewall on in a VM, or while sitting at the machine (not over SSH). If it goes wrong, `sudo ufw disable` (or `sudo systemctl stop firewalld`) turns it off.

You've done it when you can say your address, your gateway, and whether your firewall is on.

## Quiz

```quiz
- q: Otic enabled ufw over SSH and lost his connection. What should he have done first?
  options:
    - sudo ufw allow ssh
    - sudo ufw disable
    - Rebooted the laptop
  answer: 0
  why: Once ufw is on, it blocks anything not allowed. Allow SSH first, then enable.
- q: ping 1.1.1.1 works but ping fedoraproject.org fails. What's broken?
  options:
    - The Wi-Fi
    - The firewall
    - DNS, the system that turns names into addresses
  answer: 2
  why: Reaching an address proves the connection works. Failing on a name points at DNS.
- q: On Fedora, you added a firewall rule and it disappeared after a reboot. Why?
  options:
    - Fedora deletes rules every night
    - It was added without --permanent
    - firewalld only works on Arch
  answer: 1
  why: Without --permanent, firewall-cmd changes only last until the next reload or reboot.
```

## Scribble watch

The Scribble loves an open door. Run `sudo ss -tulpn` now and then: anything listening on `0.0.0.0` can be reached by every device on your network, including that suspiciously cheap smart plug. If you don't recognise a program, find out what it is. If you don't need it, stop and disable its service (lesson S), and keep your firewall on.
