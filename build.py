"""Build the course website from the lesson files.

    python build.py            # main/ -> site/
"""
from __future__ import annotations
import pathlib, shutil, sys
from html import escape

from course.lesson import Lesson, LessonError, parse_lesson
from course import render

ROOT = pathlib.Path(__file__).parent
STATIC = ROOT / "course" / "static"

CAST = [
    ("psych", "Psych", "Student. Fixes things with the Whudonk Stick. Mostly breaks them."),
    ("otic", "Otic", "Student. His T-shirt cow goes MOOOOO at anything scary."),
    ("mender", "The Mender", "Of small weathers. Calm. Shows you the right way."),
    ("scribble", "The Scribble", "Scams, viruses, mess and lost files. Never quite gone."),
]

INTRO = """
<p>Right. Sit down. No, not on the keyboard.</p>
<p>I am <strong>the Operator</strong>. I run the computers round here, and I have been asked,
very politely, by someone I owe a favour, to teach you how to use one. Twenty-six lessons,
A to Z. By the end you'll be able to do everything a normal person does with a computer and a phone,
and, more importantly, you'll stop ringing me about it.</p>
<p>Each lesson goes the same way: Psych and Otic have a go and make a mess of it, I explain why that
annoys me, then the Mender shows you how to do it properly. Then <em>you</em> do it, for real, on your own
computer. Then there's a little quiz. Then I warn you about the Scribble.</p>
<p>Do them in order. Tick each one off when you've done it. I'll know if you cheat. I always know.</p>
"""


def lesson_nav(lessons: list[Lesson], i: int) -> str:
    prev = lessons[i - 1] if i > 0 else None
    nxt = lessons[i + 1] if i + 1 < len(lessons) else None
    p = (f'<a class="prev" href="{prev.slug}.html">← {escape(prev.letter)}: {escape(prev.title)}</a>'
         if prev else '<a class="prev" href="index.html">← All lessons</a>')
    n = (f'<a class="next" href="{nxt.slug}.html">{escape(nxt.letter)}: {escape(nxt.title)} →</a>'
         if nxt else '<a class="next" href="index.html">All lessons →</a>')
    return f'<nav class="pager">{p}{n}</nav>'


def lesson_page(lessons: list[Lesson], i: int) -> str:
    l = lessons[i]
    done = f'<div class="done-row"><button type="button" class="done-btn" data-done="{l.slug}">☐ I\'ve done this lesson</button></div>'
    return render.page(f"{l.letter}: {l.title}", render.lesson_body(l) + done, lesson_nav(lessons, i), "lesson-page")


def index_page(lessons: list[Lesson], assets: pathlib.Path) -> str:
    cast = "".join(
        f'<figure class="cast-member"><img src="img/{key}.png" alt=""><figcaption><strong>{name}</strong><br>{blurb}</figcaption></figure>'
        for key, name, blurb in CAST if (assets / f"{key}.png").exists()
    )
    cards = "".join(
        f'<li><a class="card" data-slug="{l.slug}" href="{l.slug}.html"><span class="card-l">{escape(l.letter)}</span>'
        f'<span class="card-t">{escape(l.title)}</span><span class="tick" aria-hidden="true">✓</span></a></li>'
        for l in lessons
    )
    body = f"""
<header class="hero-head">
  <p class="kicker">A to Z, for absolute beginners</p>
  <h1>{escape(render.SITE_TITLE)}</h1>
  <p class="sub">Windows 11 and Android, explained by a sysadmin who would rather you didn't, starring Psych and Otic.</p>
</header>
<section class="intro s s-the-operator-says"><h2><span class="ico" aria-hidden="true">☠️</span> The Operator says</h2>{INTRO}</section>
<section class="cast"><h2>The cast</h2><div class="cast-row">{cast}</div></section>
<section class="toc">
  <h2>The lessons</h2>
  <div class="progress" style="--p:0%"><span>0 / {len(lessons)} done</span></div>
  <ol class="cards">{cards}</ol>
</section>
<section class="print-it">
  <h2>Prefer paper?</h2>
  <p><a href="handbook.html">Open the whole course as one printable handbook</a>, or <a href="handbook.pdf">download it as a PDF</a>.</p>
</section>
"""
    return render.page(render.SITE_TITLE, body, body_class="index-page")


def handbook_page(lessons: list[Lesson]) -> str:
    contents = "".join(f'<li><a href="#{l.slug}">{escape(l.letter)}: {escape(l.title)}</a></li>' for l in lessons)
    articles = "".join(render.lesson_body(l) for l in lessons)
    body = f"""
<header class="cover">
  <p class="kicker">The handbook</p>
  <h1>{escape(render.SITE_TITLE)}</h1>
  <p class="sub">Windows 11 and Android, A to Z, for absolute beginners.</p>
  <img class="cover-img" src="img/psych.png" alt="">
</header>
<section class="contents"><h2>Contents</h2><ol class="contents-list">{contents}</ol></section>
{articles}
"""
    return render.page("Handbook", body, body_class="handbook")


def build(src: pathlib.Path, out: pathlib.Path, assets: pathlib.Path) -> list[Lesson]:
    lessons = sorted((parse_lesson(p) for p in src.glob("*.md")), key=lambda l: l.letter)
    if out.exists():
        shutil.rmtree(out)
    (out / "img").mkdir(parents=True)
    for f in STATIC.iterdir():
        shutil.copy(f, out / f.name)
    for f in assets.glob("*.png"):
        shutil.copy(f, out / "img" / f.name)
    pdf = ROOT / "handbook.pdf"
    if pdf.exists():
        shutil.copy(pdf, out / "handbook.pdf")
    for i, l in enumerate(lessons):
        (out / f"{l.slug}.html").write_text(lesson_page(lessons, i), encoding="utf-8")
    (out / "index.html").write_text(index_page(lessons, assets), encoding="utf-8")
    (out / "handbook.html").write_text(handbook_page(lessons), encoding="utf-8")
    return lessons


if __name__ == "__main__":
    try:
        ls = build(ROOT / "main", ROOT / "site", ROOT / "assets" / "img")
    except LessonError as e:
        sys.exit(f"Lesson error: {e}")
    print(f"Built {len(ls)} lessons into site/")
