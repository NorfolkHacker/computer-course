---
letter: W
title: A Home Web Server
level: 4
image: whoosh
---

## What went wrong

*Otic's living room. Otic is proudly showing his phone to Psych.*

**Otic:** I've made a website! It's on my Mint box. Look: `http://localhost`.

*Psych types* `http://localhost` *into his own phone. His phone shows an error.*

**Psych:** Your website's broken.

**Otic:** It works on mine!

**Psych:** Then it's the firewall. Not a problem. *He pulls out the Whudonk Stick, then pauses and types* `sudo ufw disable` *on Otic's server.* There. Now try.

*Still nothing. Unicorn Boy wanders past with a laptop.*

**Unicorn Boy:** Easy. Just forward port 80 on your router to the whole internet! I did that with mine!

*Unicorn Boy's laptop begins to smoke. He rises gently out of the window.*

**Otic:** *(the cow on his shirt)* MOOOOO!

## The Operator says

`localhost` means "this machine". Every device on earth has one. Typing it on your phone asks your phone for your phone's website. It doesn't have one. I could have told you that for free, and I usually charge.

A web server at home is the friendliest way to learn how the internet actually works: names, ports, files, permissions. Keep it on your own network while you learn. The internet will still be there, still full of robots, when you've finished lesson Z.

## The Mender's way

A **web server** is a program that hands out web pages when a browser asks. You'll use **nginx** (said "engine-x"), which is fast, small and very common. The package and the service are both called `nginx` on all three families.

### Install and start it

### On Debian / Ubuntu / Mint

```bash
sudo apt install nginx
```

It starts by itself. Its pages live in `/var/www/html`. Settings for each site go in `/etc/nginx/sites-available/`, and a site is switched on by linking it into `/etc/nginx/sites-enabled/`.

### On Fedora

```bash
sudo dnf install nginx
sudo systemctl enable --now nginx
```

Pages live in `/usr/share/nginx/html`. Settings are in `/etc/nginx/nginx.conf`, plus any `.conf` file you put in `/etc/nginx/conf.d/`.

### On Arch / Manjaro

```bash
sudo pacman -S nginx
sudo systemctl enable --now nginx
```

Pages live in `/usr/share/nginx/html`. Settings are in `/etc/nginx/nginx.conf`.

### Check it's working

On the server itself, `curl` fetches a page and prints it (install the `curl` package if it's missing):

```bash
curl http://localhost
```

You should see some HTML containing "Welcome to nginx" (Fedora shows its own test page). If you're unsure where your nginx looks for files, `sudo nginx -T` prints the entire configuration it's using; look for the `root` lines.

### Open port 80 in the firewall

A **port** is a numbered door on a machine; web pages use port **80**. Lesson V closed every door except SSH, so open this one.

### On Debian / Ubuntu / Mint

```bash
sudo ufw allow 80/tcp
```

### On Fedora

```bash
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --reload
```

### On Arch / Manjaro

If you installed ufw in lesson V:

```bash
sudo ufw allow 80/tcp
```

### See it from another device

Find the server's address on your network (lesson T):

```bash
ip -4 addr
```

Look for `inet 192.168.x.x` (or `10.x.x.x`) on the main network card, not `127.0.0.1`. On your phone or PC, on the same Wi-Fi, type `http://192.168.1.50` (your address) into the browser's address bar. You should see the welcome page.

If you're using a VM, its network must be in **Bridged** mode, not **NAT**, for other devices to reach it. That's in the VM's network settings (lesson B).

### Put up your own page

Replace the welcome page with your own `index.html`. The folder belongs to root, so editing needs `sudo`. Use your family's folder:

```bash
sudo nano /var/www/html/index.html
```

On Fedora and Arch, use `/usr/share/nginx/html/index.html`. Type a tiny page:

```html
<!doctype html>
<title>Otic's server</title>
<h1>Hello from my server</h1>
<p>It works.</p>
```

Save, and refresh the browser. No restart is needed for new files. (On Fedora and Arch that file comes with a package, so an update can put the welcome page back. For a page that lasts, use your own folder, as in the server block below.)

### Fedora: SELinux labels

SELinux (lesson V) only lets nginx read files labelled as web content. Files you create in the web folder get the right label. Files you *move* there with `mv` keep their old label, and nginx gets `403 Forbidden`. Fix the labels with `restorecon` (`-R` every file inside, `-v` show what changed):

```bash
sudo restorecon -Rv /usr/share/nginx/html
```

### A server block for your own folder

A **server block** tells nginx "for this address and port, serve this folder". Let's serve `/srv/notes` on port **8008**, alongside the default site. (On Fedora, SELinux only allows web servers on certain ports; 8008 is one of them.)

Make the folder and a page:

```bash
sudo mkdir -p /srv/notes
echo "<h1>My notes</h1>" | sudo tee /srv/notes/index.html
```

`tee` writes what it's given to a file; with `sudo` it can write where you can't. The server block itself is the same everywhere:

```nginx
server {
    listen 8008;
    root /srv/notes;
    index index.html;
}
```

Where it goes differs:

### On Debian / Ubuntu / Mint

Save it as `/etc/nginx/sites-available/notes`, then switch it on with a link:

```bash
sudo nano /etc/nginx/sites-available/notes
sudo ln -s /etc/nginx/sites-available/notes /etc/nginx/sites-enabled/
```

### On Fedora

Save it as `/etc/nginx/conf.d/notes.conf`. Then tell SELinux the new folder is web content, and apply the label:

```bash
sudo nano /etc/nginx/conf.d/notes.conf
sudo semanage fcontext -a -t httpd_sys_content_t "/srv/notes(/.*)?"
sudo restorecon -Rv /srv/notes
```

If `semanage` is missing: `sudo dnf install policycoreutils-python-utils`.

### On Arch / Manjaro

Check whether `nginx.conf` already includes a folder of extra files:

```bash
sudo nginx -T | grep include
```

If there's no `conf.d` line, open `/etc/nginx/nginx.conf` and, inside the `http {` block, just before its closing `}`, add `include /etc/nginx/conf.d/*.conf;`. Then:

```bash
sudo mkdir -p /etc/nginx/conf.d
sudo nano /etc/nginx/conf.d/notes.conf
```

### Test, then reload

Always check the configuration before reloading. `nginx -t` tests it and says `syntax is ok` and `test is successful`, or names the file and line that's wrong:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

`reload` applies the new settings without dropping visitors. If the test fails, don't reload: fix the line it names. Then open port 8008 as you did port 80 (`sudo ufw allow 8008/tcp`, or on Fedora `sudo firewall-cmd --permanent --add-port=8008/tcp` then `--reload`), and visit `http://192.168.1.50:8008`.

### Why not on the internet yet

Forwarding a port on your router puts your server in front of every robot on earth. Before you do that you need lesson V done properly, automatic updates, and **HTTPS**, which encrypts the connection and proves the site is yours. The usual way is a free certificate from **Let's Encrypt** using a tool called **certbot**, which has an nginx plugin. You'll also need a domain name. That's the next step after this course, not this lesson.

**Caddy** is an alternative web server that gets and renews Let's Encrypt certificates automatically, with a much shorter configuration file (`/etc/caddy/Caddyfile`). It's packaged as `caddy` in all three families. If you ever put a small site on the internet, it's well worth a look. Don't run it and nginx on the same port at the same time.

## Do it now

1. Install nginx and start it.
2. Open port 80 in your firewall.
3. Replace the welcome page with your own `index.html`.
4. Visit `http://your-server-address` from your phone or another computer on the same network.
5. Add the `/srv/notes` server block, run `sudo nginx -t`, reload, open port 8008, and visit it.

You've done it when your own page shows on a different device. Don't forward any ports on your router.

## Quiz

```quiz
- q: Otic's page works at http://localhost on the server. What should Psych type on his phone?
  options:
    - http://localhost
    - The server's network address, like http://192.168.1.50
    - The server's password
  answer: 1
  why: localhost always means "this device". From another device you use the server's address on your network.
- q: You've edited an nginx config file. What should you run before reloading?
  options:
    - sudo nginx -t
    - sudo ufw disable
    - sudo reboot
  answer: 0
  why: "nginx -t checks the configuration and names any broken line. Reloading a broken config can take the site down."
- q: Your home server works on your Wi-Fi. When should you forward port 80 to the internet?
  options:
    - Now, so friends can see it
    - Only once it's hardened and set up for HTTPS
    - Never use ports
  answer: 1
  why: Forwarding a port exposes the server to the whole internet. Harden it first, and add HTTPS with Let's Encrypt or Caddy.
```

## Scribble watch

The Scribble posts on a forum: "nginx giving you 403 Forbidden? Just `sudo chmod -R 777 /var/www`." Propellor Boy did it, and now any program on his machine, friendly or not, can rewrite his website. Fix only the folder you're serving: files need to be readable (`644`), folders openable (`755`), and on Fedora correctly labelled with `restorecon`. Never use `777`.
