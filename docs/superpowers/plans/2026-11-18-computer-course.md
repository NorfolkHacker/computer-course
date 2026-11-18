# Computer Course (Main A–Z) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the main A–Z computer course (Windows 11 + Android) as Markdown lessons that compile into a GitHub Pages web course and a printable handbook/PDF.

**Architecture:** One Markdown file per lesson in `main/`. `course/lesson.py` parses and validates a lesson; `course/render.py` turns lessons into HTML; `build.py` writes `site/`. Pictures are cut from the felt *Psych and Otic* film into `assets/img/` by `scripts/make_images.py` and copied into `site/img/`. A GitHub Actions workflow builds and deploys `site/` to Pages.

**Tech Stack:** Python 3 (`markdown`, `pyyaml`, `pillow` for the image script only), pytest, plain HTML/CSS/JS, headless Chromium for the PDF, ffmpeg for frame grabs.

**Spec:** `docs/superpowers/specs/2026-11-18-computer-course-design.md`

## Global Constraints

- Audience: absolute beginner. Every instruction plain and literal; jokes live only in framing (cold open, Operator, Scribble watch). Never make a step depend on understanding a joke.
- Platforms: Windows 11 and Android only. No macOS/iPhone.
- The Operator is an original BOFH-*style* narrator. Never name or quote BOFH / Simon Travaglia's characters.
- Cast: Operator, Psych (Whudonk Stick), Otic (cow T-shirt, MOOOOO), the Mender, the Scribble, Propellor Boy, Unicorn Boy.
- Every lesson has exactly these `##` sections in order: `Cold open`, `The Operator says`, `The Mender's way`, `Do it now`, `Quiz`, `Scribble watch`.
- Quiz: exactly 3 questions, each 3–4 options, `answer` is a 0-based index, `why` required.
- Site: no backend; progress in `localStorage` wrapped in try/catch; usable at 360px wide; light and dark themes.
- Repo: `~/computer-course`, commits as NorfolkHacker (repo-local git config already set), commit messages end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- Python deps go in a venv at `.venv/` (gitignored); `requirements.txt` lists them.

## File Structure

```
computer-course/
  main/A-parts-of-a-computer.md … main/Z-zen.md   # 26 lessons (source of truth)
  course/__init__.py
  course/lesson.py        # parse + validate one lesson file -> Lesson
  course/render.py        # Lesson -> HTML fragments; page templates
  course/static/style.css # site + print styles
  course/static/app.js    # quiz clicks + progress ticks
  build.py                # main/ -> site/  (index, per-lesson pages, handbook)
  scripts/make_images.py  # felt film -> assets/img/*.png
  scripts/check_site.py   # every internal link/img in site/ resolves
  scripts/make_pdf.sh     # site/handbook.html -> handbook.pdf
  assets/img/*.png        # committed character/sticker images
  tests/test_lesson.py tests/test_render.py tests/test_build.py
  .github/workflows/pages.yml
  requirements.txt  .gitignore  README.md  handbook.pdf
```

`site/` is build output: gitignored, built in CI.

---

### Task 1: Lesson parser and validator

**Files:**
- Create: `course/__init__.py`, `course/lesson.py`, `tests/test_lesson.py`, `requirements.txt`, `.gitignore`

**Interfaces:**
- Produces:
  - `SECTIONS: list[str]` = `["Cold open", "The Operator says", "The Mender's way", "Do it now", "Quiz", "Scribble watch"]`
  - `@dataclass Question(q: str, options: list[str], answer: int, why: str)`
  - `@dataclass Lesson(letter: str, title: str, slug: str, image: str | None, sections: dict[str, str], quiz: list[Question])` (sections maps section name → raw Markdown body, excluding the Quiz section)
  - `class LessonError(Exception)` (message always starts with the file name)
  - `parse_lesson(path: pathlib.Path) -> Lesson`

Lesson file format:

````markdown
---
letter: A
title: The Parts of a Computer
image: psych        # optional; one of the names in assets/img without .png
---

## Cold open
**Psych:** ...

## The Operator says
...

## The Mender's way
...
### On Windows
...
### On Android
...

## Do it now
...

## Quiz
```quiz
- q: What is the screen called?
  options: [Monitor, Tower, Mouse]
  answer: 0
  why: The monitor is the screen.
```

## Scribble watch
...
````

`slug` comes from the file name: `A-parts-of-a-computer.md` → `a-parts-of-a-computer`. The letter in the file name must equal front matter `letter`.

- [ ] **Step 1: venv + deps**

```bash
cd ~/computer-course
printf 'markdown==3.7\npyyaml==6.0.2\npillow==11.0.0\npytest==8.3.4\n' > requirements.txt
printf '.venv/\nsite/\n__pycache__/\n*.pyc\n' > .gitignore
python3 -m venv .venv && .venv/bin/pip install -q -r requirements.txt
```

- [ ] **Step 2: Write failing tests** in `tests/test_lesson.py`

```python
import pathlib, textwrap, pytest
from course.lesson import parse_lesson, LessonError, SECTIONS

GOOD = textwrap.dedent('''\
    ---
    letter: A
    title: The Parts of a Computer
    image: psych
    ---

    ## Cold open
    **Psych:** Hello.

    ## The Operator says
    Grim.

    ## The Mender's way
    1. Do it.

    ## Do it now
    Try it.

    ## Quiz
    ```quiz
    - q: One?
      options: [a, b, c]
      answer: 0
      why: Because.
    - q: Two?
      options: [a, b, c]
      answer: 1
      why: Because.
    - q: Three?
      options: [a, b, c, d]
      answer: 3
      why: Because.
    ```

    ## Scribble watch
    Careful.
    ''')

def write(tmp_path, text, name="A-parts-of-a-computer.md"):
    p = tmp_path / name
    p.write_text(text)
    return p

def test_parses_good_lesson(tmp_path):
    l = parse_lesson(write(tmp_path, GOOD))
    assert (l.letter, l.title, l.slug, l.image) == ("A", "The Parts of a Computer", "a-parts-of-a-computer", "psych")
    assert list(l.sections) == [s for s in SECTIONS if s != "Quiz"]
    assert l.sections["Cold open"].strip() == "**Psych:** Hello."
    assert len(l.quiz) == 3 and l.quiz[2].answer == 3 and l.quiz[1].why == "Because."

def test_missing_section(tmp_path):
    with pytest.raises(LessonError, match="Scribble watch"):
        parse_lesson(write(tmp_path, GOOD.split("## Scribble watch")[0]))

def test_sections_out_of_order(tmp_path):
    bad = GOOD.replace("## Do it now", "## TEMP").replace("## The Operator says", "## Do it now").replace("## TEMP", "## The Operator says")
    with pytest.raises(LessonError, match="order"):
        parse_lesson(write(tmp_path, bad))

def test_quiz_needs_three(tmp_path):
    bad = GOOD.replace("- q: Three?\n  options: [a, b, c, d]\n  answer: 3\n  why: Because.\n", "")
    with pytest.raises(LessonError, match="3 questions"):
        parse_lesson(write(tmp_path, bad))

def test_answer_out_of_range(tmp_path):
    with pytest.raises(LessonError, match="answer"):
        parse_lesson(write(tmp_path, GOOD.replace("answer: 3", "answer: 7")))

def test_letter_mismatch(tmp_path):
    with pytest.raises(LessonError, match="letter"):
        parse_lesson(write(tmp_path, GOOD, name="B-mouse.md"))

def test_error_names_file(tmp_path):
    with pytest.raises(LessonError, match="A-parts-of-a-computer.md"):
        parse_lesson(write(tmp_path, GOOD.replace("why: Because.", "", 1)))
```

- [ ] **Step 3: Run, expect failure**: `.venv/bin/pytest tests/test_lesson.py -q` → ImportError.

- [ ] **Step 4: Implement `course/lesson.py`**

```python
"""Parse and validate one lesson Markdown file."""
from __future__ import annotations
import pathlib, re
from dataclasses import dataclass
import yaml

SECTIONS = ["Cold open", "The Operator says", "The Mender's way", "Do it now", "Quiz", "Scribble watch"]


class LessonError(Exception):
    pass


@dataclass
class Question:
    q: str
    options: list[str]
    answer: int
    why: str


@dataclass
class Lesson:
    letter: str
    title: str
    slug: str
    image: str | None
    sections: dict[str, str]
    quiz: list[Question]


def _fail(path, msg):
    raise LessonError(f"{path.name}: {msg}")


def parse_lesson(path: pathlib.Path) -> Lesson:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        _fail(path, "missing front matter")
    meta = yaml.safe_load(m.group(1)) or {}
    body = m.group(2)
    for key in ("letter", "title"):
        if not meta.get(key):
            _fail(path, f"front matter needs '{key}'")
    letter = str(meta["letter"]).upper()
    if path.stem[:1].upper() != letter:
        _fail(path, f"file name letter does not match letter '{letter}'")

    parts = re.split(r"^## (.+?)\s*$", body, flags=re.M)
    found = {}
    order = []
    for name, content in zip(parts[1::2], parts[2::2]):
        order.append(name)
        found[name] = content
    for s in SECTIONS:
        if s not in found:
            _fail(path, f"missing section '## {s}'")
    if order != SECTIONS:
        _fail(path, f"sections out of order: {order}")

    qm = re.search(r"```quiz\n(.*?)```", found["Quiz"], re.S)
    if not qm:
        _fail(path, "Quiz section needs a ```quiz block")
    raw = yaml.safe_load(qm.group(1)) or []
    if len(raw) != 3:
        _fail(path, f"quiz needs exactly 3 questions, has {len(raw)}")
    quiz = []
    for i, item in enumerate(raw, 1):
        for key in ("q", "options", "answer", "why"):
            if item.get(key) in (None, ""):
                _fail(path, f"quiz question {i} missing '{key}'")
        opts = [str(o) for o in item["options"]]
        if not 3 <= len(opts) <= 4:
            _fail(path, f"quiz question {i} needs 3-4 options")
        ans = item["answer"]
        if not isinstance(ans, int) or not 0 <= ans < len(opts):
            _fail(path, f"quiz question {i} answer {ans!r} out of range")
        quiz.append(Question(str(item["q"]), opts, ans, str(item["why"])))

    sections = {s: found[s] for s in SECTIONS if s != "Quiz"}
    return Lesson(letter, str(meta["title"]), path.stem.lower(), meta.get("image"), sections, quiz)
```

`touch course/__init__.py tests/__init__.py`; add `tests/conftest.py` with `import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))`.

- [ ] **Step 5: Run, expect pass**: `.venv/bin/pytest -q` → 7 passed.
- [ ] **Step 6: Commit** `git add -A && git commit -m "Add lesson parser and validator"` (+ co-author line).

---

### Task 2: Renderer, site build, styles and quiz/progress script

**Files:**
- Create: `course/render.py`, `course/static/style.css`, `course/static/app.js`, `build.py`, `tests/test_render.py`, `tests/test_build.py`

**Interfaces:**
- Consumes: `parse_lesson`, `Lesson`, `Question`, `LessonError` from Task 1.
- Produces:
  - `render.md(text: str) -> str` (Markdown → HTML, extensions `extra`, `sane_lists`)
  - `render.lesson_body(lesson: Lesson, img_prefix: str = "img/") -> str` (the `<article>` for one lesson)
  - `render.page(title: str, body: str, nav: str = "") -> str` (full HTML document)
  - `build.build(src: Path, out: Path, assets: Path) -> list[Lesson]` — parses every `src/*.md` sorted by letter, writes `out/index.html`, `out/<slug>.html`, `out/handbook.html`, copies `course/static/*` to `out/` and `assets/img/*` to `out/img/`. Raises `LessonError` on the first bad lesson. CLI: `python build.py` uses `main/`, `site/`, `assets/img/`.

Rendering rules:
- `<article class="lesson" id="<slug>" data-slug="<slug>">` with `<header>`: big letter, title, and the lesson's image if set (`<img class="hero" src="{img_prefix}{image}.png" alt="">`).
- Each section → `<section class="s-<kebab-name>"><h2>{icon} {name}</h2>…</section>`. Icons: Cold open 🎬, The Operator says ☠️, The Mender's way 🧵, Do it now ✋, Quiz ❓, Scribble watch 🖍️.
- Quiz section is rendered after "Do it now" (keeps spec order) from `lesson.quiz`: each question is `<fieldset class="q" data-answer="N"><legend>…</legend>` with one `<button class="opt" data-i="i">` per option and a hidden `<p class="why">`. In print CSS, buttons render as a lettered list and `.why` shows as "Answer: B — why".
- In The Mender's way, an `<h3>` starting "On Windows" or "On Android" plus following content up to the next h3/end is wrapped in `<div class="platform platform-windows|android">`; consecutive platform divs are wrapped in `<div class="platforms">` (CSS grid, 2 columns ≥ 720px, 1 column below).
- Lesson page footer: "✅ I've done this lesson" button (`data-done="<slug>"`), prev/next links.
- `index.html`: title "The Operator's Computer Course", a short intro by the Operator, the cast strip (psych, otic, mender, scribble images with names), an A–Z grid of cards (letter, title, tick state), a progress bar "N / 26 done", a link to the handbook and to `handbook.pdf` on GitHub.
- `handbook.html`: cover + contents + every lesson article in order, one `page-break-before` per lesson, quiz answers visible.

`app.js` (no dependencies):
```js
(function () {
  var KEY = "course-done";
  function load() { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; } }
  function save(d) { try { localStorage.setItem(KEY, JSON.stringify(d)); } catch (e) {} }
  var done = load();
  document.querySelectorAll(".q").forEach(function (fs) {
    var ans = +fs.dataset.answer;
    fs.querySelectorAll(".opt").forEach(function (b) {
      b.addEventListener("click", function () {
        fs.querySelectorAll(".opt").forEach(function (o) { o.classList.remove("right", "wrong"); });
        var ok = +b.dataset.i === ans;
        b.classList.add(ok ? "right" : "wrong");
        fs.classList.toggle("answered", ok);
        if (!ok) b.setAttribute("aria-label", b.textContent + " (not quite)");
      });
    });
  });
  function paint() {
    var n = 0;
    document.querySelectorAll("[data-done]").forEach(function (b) {
      var on = !!done[b.dataset.done];
      b.classList.toggle("on", on);
      if (b.tagName === "BUTTON") b.textContent = on ? "✅ Done! (click to undo)" : "☐ I've done this lesson";
    });
    document.querySelectorAll(".card").forEach(function (c) { var on = !!done[c.dataset.slug]; c.classList.toggle("done", on); if (on) n++; });
    var bar = document.querySelector(".progress");
    if (bar) { bar.querySelector("span").textContent = n + " / 26 done"; bar.style.setProperty("--p", (n / 26 * 100) + "%"); }
  }
  document.querySelectorAll("button[data-done]").forEach(function (b) {
    b.addEventListener("click", function () { var s = b.dataset.done; if (done[s]) delete done[s]; else done[s] = 1; save(done); paint(); });
  });
  paint();
})();
```

`style.css`: color tokens on `:root` (felt palette: warm beige paper `#efe6d2`, ink `#2a2420`, autumn orange `#d9772b`, Whudonk purple `#6b3fa0`, cow red `#c8402e`), dark-mode overrides under `@media (prefers-color-scheme: dark)`; body font "Atkinson Hyperlegible" (Google Fonts; it's designed for readability) at 18px, line-height 1.6; max-width 760px; 16px side gutter; big tappable buttons (min-height 48px); cold open styled as a felt "scene card" with a dashed stitch border; Operator section dark terminal-ish box with monospace heading; Mender section calm, numbered steps large; Scribble watch with a scribbly border; `.opt.right` green, `.opt.wrong` red with an icon (not colour alone); `@media print` hides nav/buttons, shows answers, black on white.

- [ ] **Step 1: Write failing tests** in `tests/test_render.py`

```python
from course.lesson import Lesson, Question
from course import render

def L(**kw):
    base = dict(letter="A", title="Parts", slug="a-parts", image="psych",
        sections={"Cold open": "**Psych:** Hi.", "The Operator says": "Grim.",
                  "The Mender's way": "1. Step\n\n### On Windows\nWin steps\n\n### On Android\nPhone steps\n",
                  "Do it now": "Try.", "Scribble watch": "Careful."},
        quiz=[Question("One?", ["a", "b", "c"], 1, "Because.")] * 3)
    base.update(kw)
    return Lesson(**base)

def test_article_has_all_sections_in_order():
    h = render.lesson_body(L())
    idx = [h.index(s) for s in ["Cold open", "The Operator says", "The Mender&#x27;s way", "Do it now", "Quiz", "Scribble watch"]]
    assert idx == sorted(idx)

def test_platforms_wrapped():
    h = render.lesson_body(L())
    assert '<div class="platforms">' in h
    assert 'platform-windows' in h and 'platform-android' in h

def test_quiz_markup():
    h = render.lesson_body(L())
    assert h.count('class="q"') == 3
    assert 'data-answer="1"' in h and h.count('class="opt"') == 9 and "Because." in h

def test_image_and_escaping():
    h = render.lesson_body(L(title="<Mice & Men>"))
    assert 'src="img/psych.png"' in h and "&lt;Mice &amp; Men&gt;" in h

def test_page_is_full_document():
    p = render.page("T", "<p>x</p>")
    assert p.startswith("<!doctype html>") and 'name="viewport"' in p and "app.js" in p
```

`tests/test_build.py`:

```python
import pathlib, shutil
import build
ROOT = pathlib.Path(__file__).parent.parent

def test_build_fixture(tmp_path):
    src = tmp_path / "src"; src.mkdir()
    fixture = (ROOT / "tests" / "fixtures" / "A-parts-of-a-computer.md")
    shutil.copy(fixture, src / fixture.name)
    shutil.copy(fixture, src / "B-mouse.md")
    (src / "B-mouse.md").write_text((src / "B-mouse.md").read_text().replace("letter: A", "letter: B"))
    out = tmp_path / "site"
    lessons = build.build(src, out, ROOT / "assets" / "img")
    assert [l.letter for l in lessons] == ["A", "B"]
    for f in ["index.html", "handbook.html", "a-parts-of-a-computer.html", "b-mouse.html", "style.css", "app.js"]:
        assert (out / f).exists(), f
    idx = (out / "index.html").read_text()
    assert 'href="a-parts-of-a-computer.html"' in idx and 'href="handbook.html"' in idx
    a = (out / "a-parts-of-a-computer.html").read_text()
    assert 'href="b-mouse.html"' in a  # next link
```

Create `tests/fixtures/A-parts-of-a-computer.md` with the `GOOD` text from Task 1, and `assets/img/psych.png` placeholder (any PNG; Task 3 replaces it).

- [ ] **Step 2: Run, expect failure**: `.venv/bin/pytest -q`.
- [ ] **Step 3: Implement** `course/render.py`, `build.py`, `style.css`, `app.js` per the rules above. `render.md` uses `markdown.markdown(text, extensions=["extra", "sane_lists"])`; titles and quiz text go through `html.escape`. Platform wrapping is done on the HTML with a regex over `<h3>On (Windows|Android)…</h3>` chunks.
- [ ] **Step 4: Run, expect pass**: `.venv/bin/pytest -q`.
- [ ] **Step 5: Commit** "Add renderer, site build, styles and quiz/progress script".

---

### Task 3: Character images

**Files:**
- Create: `scripts/make_images.py`, `assets/img/*.png`

**Interfaces:**
- Produces image names (no extension) that lessons may use in `image:`: `psych`, `psych-up`, `psych-smash`, `otic`, `propellor-boy`, `unicorn-boy`, `mender`, `scribble`, `jar`, and stickers `whudonk`, `mooo`, `ohno`, `huh`, `poof`, `shloop`, `whoosh`, `clink`.

Sources (all under `~/Documents/felt/films/psych-and-otic/`):
- `stills/c-psych.png`, `c-psych-up.png`, `c-psych-smash.png`, `c-otic.png`, `c-pb.png`, `c-ub.png` (800×800 on flat beige): make the background transparent by flood-filling from the corners with tolerance, then crop to content bbox + 12px.
- `assets/whudonk.png`, `mooo.png`, `ohno.png`, `huh1.png`→`huh`, `poof.png`, `shloop.png`, `whoosh.png`, `clink.png`: copy as-is.
- Mender, Scribble, jar: grab frames from `psych-and-otic.mp4` with `ffmpeg -ss <t> -frames:v 1` (Scribble ~36.5 s wide shot; Mender close-up with jar ~63.5 s; Mender standing ~16 s), crop to the subject, save. Keep the felt background (these are scene frames, shown as framed pictures).
- Downscale everything so the longest side ≤ 640px; save optimized PNG.

- [ ] **Step 1:** Write the script, run `.venv/bin/python scripts/make_images.py`.
- [ ] **Step 2:** Open a contact sheet of `assets/img/*` (montage with Pillow to scratchpad) and look at it; fix crops until every subject is whole and centred.
- [ ] **Step 3:** `.venv/bin/pytest -q` still passes. Commit "Add character images from the Psych and Otic film".

---

### Task 4: Exemplar lesson A + style guide

**Files:**
- Create: `main/A-parts-of-a-computer.md`, `docs/lesson-style-guide.md`

`docs/lesson-style-guide.md` captures the voice so every lesson matches:
- **Cold open** (80–150 words): a mini script. Psych & Otic attempt the lesson's task and go wrong in a cartoonish but *realistic* way (the mistake is one real beginners make). Psych escalates to the Whudonk Stick; Otic's cow goes MOOOOO at scary things; Propellor Boy & Unicorn Boy appear when someone falls for a scam/does something reckless. Stage directions in *italics*, dialogue as `**Name:** line`.
- **The Operator says** (60–120 words): first-person, dry, menacing sysadmin. Excuses, the luser list, threats he never carries out, contempt for printers. Ends on the real reason the lesson matters. Never cruel about the learner himself — he's the one person the Operator grudgingly respects.
- **The Mender's way**: calm, plain, numbered steps. One action per step, exact names of buttons/menus in **bold** as they appear on screen in Windows 11 / current Android. Use `### On Windows` / `### On Android` subsections where both platforms apply. Define every new word the first time in plain English. No jokes inside steps.
- **Do it now**: one concrete, safe exercise with a clear "you've done it when…" check.
- **Quiz**: 3 practical questions; distractors are the real mistakes from the cold open.
- **Scribble watch** (40–80 words): one safety habit, framed as the Scribble trying something, ending with what to do.
- Length target: 700–1200 words per lesson. UK English (the author is in Norfolk). Accurate to Windows 11 (24H2) and Android 14/15; where menu names vary by phone maker, say so and give the Settings search fallback.

- [ ] **Step 1:** Write the style guide and lesson A.
- [ ] **Step 2:** `.venv/bin/python build.py` succeeds; open `site/a-parts-of-a-computer.html` and read it rendered.
- [ ] **Step 3:** Commit "Add lesson style guide and lesson A".

---

### Task 5: Lessons B–Z

**Files:** `main/<L>-<slug>.md` for B–Z, slugs:
B-mouse, C-keyboard, D-desktop, E-files-and-folders, F-finding-things, G-getting-online, H-hunting-the-web, I-inbox, J-junk-and-scams, K-keys-and-passwords, L-lifeboats-backups, M-mobile-android, N-notifications-and-settings, O-office-documents, P-printing-and-pdfs, Q-quick-keys, R-running-programs, S-security-updates, T-troubleshooting, U-usb-and-bluetooth, V-video-calls, W-web-money, X-extra-care-privacy, Y-your-accounts, Z-zen.

Content per lesson is the row in the spec's A–Z table; Z's quiz is the "final exam" teaser and its Do it now is a mixed checklist covering the whole course.

Written in four parallel batches (B–H, I–N, O–T, U–Z), each by a subagent given the spec, the style guide and lesson A as the exemplar. Each batch must leave `python build.py` passing.

- [ ] **Step 1:** Dispatch the four batches.
- [ ] **Step 2:** Build passes; review each batch for accuracy (real Windows 11 / Android menu names), voice, and no step depending on a joke. Fix.
- [ ] **Step 3:** Commit per batch.

---

### Task 6: Site checks, PDF, Pages deploy, README

**Files:**
- Create: `scripts/check_site.py`, `scripts/make_pdf.sh`, `.github/workflows/pages.yml`, `handbook.pdf`; Modify: `README.md`

- `check_site.py`: walks `site/*.html`, collects every `href`/`src` that isn't `http(s):`/`mailto:`/`#…`, asserts the target file exists; asserts 26 lesson pages. Exit 1 with a list on failure.
- `make_pdf.sh`: `chromium --headless --no-pdf-header-footer --print-to-pdf=handbook.pdf "file://$PWD/site/handbook.html"`.
- `pages.yml`: on push to `main`: checkout, setup-python 3.12, `pip install markdown==3.7 pyyaml==6.0.2 pytest==8.3.4`, `pytest -q`, `python build.py`, `python scripts/check_site.py`, `cp handbook.pdf site/`, `actions/upload-pages-artifact@v3` with `path: site`, then `actions/deploy-pages@v4`. Permissions `pages: write`, `id-token: write`.
- README: what it is, link to the live course and PDF, how to edit a lesson and rebuild, the cast.

- [ ] **Step 1:** Write scripts; run build + check locally; make the PDF and look at a few pages.
- [ ] **Step 2:** Enable Pages with workflow source: `gh api -X POST repos/NorfolkHacker/computer-course/pages -f build_type=workflow`.
- [ ] **Step 3:** Commit, push, watch the run (`gh run watch`), confirm `https://norfolkhacker.github.io/computer-course/` loads.

---

### Task 7: Live verification

- [ ] Open the live site in the browser at desktop and 375px width: index, lesson A, a quiz (right and wrong answers), tick a lesson and see it on the index, handbook print preview. Fix anything broken, push, recheck.
