# The Operator's Computer Course

An A–Z computer course for absolute beginners, covering **Windows 11** and **Android**.
It's narrated by the Operator, a sysadmin who would rather you didn't, and stars Psych
and Otic from the felt cartoon *Psych and Otic*.

**Take the course:** https://norfolkhacker.github.io/computer-course/
**Print it:** [handbook.pdf](handbook.pdf), or open the
[handbook page](https://norfolkhacker.github.io/computer-course/handbook.html) and print it.

## How each lesson works

1. **Cold open:** Psych and Otic have a go and get it wrong.
2. **The Operator says:** why that annoys him, and why it matters.
3. **The Mender's way:** the proper method, step by step, for Windows and Android.
4. **Do it now:** you do it for real.
5. **Quiz:** three questions.
6. **Scribble watch:** one safety habit.

Tick off each lesson when you've done it. Your progress is saved in your browser.

## The cast

| | |
|---|---|
| **The Operator** | Narrator. Dry, menacing, secretly on your side. |
| **Psych** | Student. Fixes things with the Whudonk Stick. Mostly breaks them. |
| **Otic** | Student. His T-shirt cow goes MOOOOO at anything scary. |
| **The Mender** | Of small weathers. Calm. Shows you the right way. |
| **The Scribble** | Scams, viruses, mess and lost files. Never quite gone. |
| **Propellor Boy & Unicorn Boy** | They clicked the link. |

## Editing the course

Lessons are Markdown files in [`main/`](main/), one per letter. The format and voice
rules are in [`docs/lesson-style-guide.md`](docs/lesson-style-guide.md).

```sh
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/pytest -q                  # tests
.venv/bin/python build.py            # main/*.md -> site/
.venv/bin/python scripts/check_site.py
scripts/make_pdf.sh                  # site/handbook.html -> handbook.pdf (needs Chromium)
```

Pushing to `main` rebuilds and publishes the site with GitHub Actions. Re-run
`scripts/make_pdf.sh` and commit `handbook.pdf` when lessons change.

Pictures come from the felt film (`scripts/make_images.py`).

## Coming later

A separate Linux course, from first install to running your own server.
