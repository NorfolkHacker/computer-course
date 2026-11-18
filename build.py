"""Build the course website from the lesson files.

    python build.py            # main/ -> site/, linux/ -> site/linux/
"""
from __future__ import annotations
import pathlib, shutil, sys
from dataclasses import dataclass, field
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

LINUX_CAST = [
    ("psych", "Psych", "Runs Arch. Will tell you. Will tell you again."),
    ("otic", "Otic", "Runs Mint. It just works, and his cow likes it."),
    ("mender", "The Mender", "Runs Fedora, quietly. Shows you the right way."),
    ("scribble", "The Scribble", "Malware, broken configs and rm -rf. Never quite gone."),
]

MAIN_INTRO = """
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

LINUX_INTRO = """
<p>Ah. You came back. Most people don't.</p>
<p>This is <strong>Linux</strong>, which is where I actually live. No adverts in the Start menu, no
"let's finish setting up your device", no surprise reboots. Just you, a terminal, and a computer
that does exactly what you tell it to, including the stupid things. <em>Especially</em> the stupid things.</p>
<p>Twenty-six lessons again, in four levels: the desktop, the terminal, power user, and admin. By Z you'll
have built and secured your own server, and you'll be what I am: the person other people ring.
My condolences.</p>
<p>Linux comes in families. Pick yours at the top of any command box (Debian, Fedora or Arch) and I'll
show you your version from then on. Psych uses Arch. He will mention it. Ignore him.</p>
"""


@dataclass
class Course:
    key: str
    sub: str                 # output subfolder ("" for the site root)
    title: str
    kicker: str
    tagline: str
    intro: str
    cast: list
    tabs: bool = False
    levels: dict = field(default_factory=dict)
    pdf: str = "handbook.pdf"  # source PDF at the repo root, published as handbook.pdf
    cover: str = "psych"

    @property
    def root(self) -> str:
        return "../" if self.sub else ""


MAIN = Course(
    key="main", sub="", title=render.SITE_TITLE, kicker="A to Z, for absolute beginners",
    tagline="Windows 11 and Android, explained by a sysadmin who would rather you didn't, starring Psych and Otic.",
    intro=MAIN_INTRO, cast=CAST,
)

LINUX = Course(
    key="linux", sub="linux", title="The Operator's Linux Course", kicker="Part two: beginner to admin",
    tagline="Linux, A to Z, for Debian, Fedora and Arch. The Operator is on home turf, and Psych uses Arch.",
    intro=LINUX_INTRO, cast=LINUX_CAST, tabs=True,
    levels={1: "Level 1 · The desktop", 2: "Level 2 · The terminal", 3: "Level 3 · Power user", 4: "Level 4 · Admin"},
    pdf="linux-handbook.pdf", cover="psych-up",
)


def other_link(c: Course) -> str:
    if c.key == "main":
        return '<a class="other" href="linux/index.html">🐧 Linux course</a>'
    return '<a class="other" href="../index.html">🐄 Main course</a>'


def _page(c: Course, title: str, body: str, nav: str = "", body_class: str = "", links: str = "") -> str:
    return render.page(title, body, nav, body_class, root=c.root, site_title=c.title, home="index.html", links=links)


def lesson_nav(lessons: list[Lesson], i: int) -> str:
    prev = lessons[i - 1] if i > 0 else None
    nxt = lessons[i + 1] if i + 1 < len(lessons) else None
    p = (f'<a class="prev" href="{prev.slug}.html">← {escape(prev.letter)}: {escape(prev.title)}</a>'
         if prev else '<a class="prev" href="index.html">← All lessons</a>')
    n = (f'<a class="next" href="{nxt.slug}.html">{escape(nxt.letter)}: {escape(nxt.title)} →</a>'
         if nxt else '<a class="next" href="index.html">All lessons →</a>')
    return f'<nav class="pager">{p}{n}</nav>'


def lesson_page(c: Course, lessons: list[Lesson], i: int, links: str = "") -> str:
    l = lessons[i]
    done = f'<div class="done-row"><button type="button" class="done-btn" data-done="{l.slug}">☐ I\'ve done this lesson</button></div>'
    body = render.lesson_body(l, img_prefix=f"{c.root}img/", tabs=c.tabs) + done
    return _page(c, f"{l.letter}: {l.title}", body, lesson_nav(lessons, i), "lesson-page", links)


def _cards(lessons: list[Lesson]) -> str:
    return "".join(
        f'<li><a class="card" data-slug="{l.slug}" href="{l.slug}.html"><span class="card-l">{escape(l.letter)}</span>'
        f'<span class="card-t">{escape(l.title)}</span><span class="tick" aria-hidden="true">✓</span></a></li>'
        for l in lessons
    )


def index_page(c: Course, lessons: list[Lesson], assets: pathlib.Path, has_linux: bool = False) -> str:
    cast = "".join(
        f'<figure class="cast-member"><img src="{c.root}img/{key}.png" alt=""><figcaption><strong>{name}</strong><br>{blurb}</figcaption></figure>'
        for key, name, blurb in c.cast if (assets / f"{key}.png").exists()
    )
    if c.levels:
        groups = "".join(
            f'<h3 class="level">{escape(name)}</h3><ol class="cards">{_cards([l for l in lessons if l.level == n])}</ol>'
            for n, name in c.levels.items() if any(l.level == n for l in lessons)
        )
        loose = [l for l in lessons if l.level not in c.levels]
        if loose:
            groups += f'<ol class="cards">{_cards(loose)}</ol>'
    else:
        groups = f'<ol class="cards">{_cards(lessons)}</ol>'
    linux = """
<section class="next-course s">
  <h2>🐧 Finished? Part two: Linux</h2>
  <p>The same cast, a different computer. Beginner to admin, with commands for Debian, Fedora and Arch.</p>
  <p><a href="linux/index.html">Start the Linux course →</a></p>
</section>""" if has_linux else ""
    body = f"""
<header class="hero-head">
  <p class="kicker">{escape(c.kicker)}</p>
  <h1>{escape(c.title)}</h1>
  <p class="sub">{escape(c.tagline)}</p>
</header>
<section class="intro s s-the-operator-says"><h2><span class="ico" aria-hidden="true">☠️</span> The Operator says</h2>{c.intro}</section>
<section class="cast"><h2>The cast</h2><div class="cast-row">{cast}</div></section>
<section class="toc">
  <h2>The lessons</h2>
  <div class="progress" style="--p:0%"><span>0 / {len(lessons)} done</span></div>
  {groups}
</section>
<section class="print-it">
  <h2>Prefer paper?</h2>
  <p><a href="handbook.html">Open the whole course as one printable handbook</a>, or <a href="handbook.pdf">download it as a PDF</a>.</p>
</section>
{linux}
"""
    return _page(c, c.title, body, body_class="index-page", links=other_link(c) if (has_linux or c.key != "main") else "")


def handbook_page(c: Course, lessons: list[Lesson], links: str = "") -> str:
    contents = "".join(f'<li><a href="#{l.slug}">{escape(l.letter)}: {escape(l.title)}</a></li>' for l in lessons)
    articles = "".join(render.lesson_body(l, img_prefix=f"{c.root}img/", tabs=c.tabs) for l in lessons)
    body = f"""
<header class="cover">
  <p class="kicker">The handbook</p>
  <h1>{escape(c.title)}</h1>
  <p class="sub">{escape(c.tagline)}</p>
  <img class="cover-img" src="{c.root}img/{c.cover}.png" alt="">
</header>
<section class="contents"><h2>Contents</h2><ol class="contents-list">{contents}</ol></section>
{articles}
"""
    return _page(c, "Handbook", body, body_class="handbook", links=links)


def copy_shared(out: pathlib.Path, assets: pathlib.Path) -> None:
    (out / "img").mkdir(parents=True, exist_ok=True)
    for f in STATIC.iterdir():
        shutil.copy(f, out / f.name)
    for f in assets.glob("*.png"):
        shutil.copy(f, out / "img" / f.name)


def build_course(c: Course, src: pathlib.Path, out: pathlib.Path, assets: pathlib.Path,
                 has_linux: bool = False) -> list[Lesson]:
    """Write one course's pages into out (shared CSS/JS/images live at the site root)."""
    lessons = sorted((parse_lesson(p) for p in src.glob("*.md")), key=lambda l: l.letter)
    out.mkdir(parents=True, exist_ok=True)
    links = other_link(c) if (has_linux or c.key != "main") else ""
    pdf = ROOT / c.pdf
    if pdf.exists():
        shutil.copy(pdf, out / "handbook.pdf")
    for i, _ in enumerate(lessons):
        (out / f"{lessons[i].slug}.html").write_text(lesson_page(c, lessons, i, links), encoding="utf-8")
    (out / "index.html").write_text(index_page(c, lessons, assets, has_linux), encoding="utf-8")
    (out / "handbook.html").write_text(handbook_page(c, lessons, links), encoding="utf-8")
    return lessons


def build(src: pathlib.Path, out: pathlib.Path, assets: pathlib.Path) -> list[Lesson]:
    """Build the main course alone into a fresh out/ (used by tests)."""
    if out.exists():
        shutil.rmtree(out)
    copy_shared(out, assets)
    return build_course(MAIN, src, out, assets)


def build_all(root: pathlib.Path = ROOT, out: pathlib.Path | None = None) -> dict[str, list[Lesson]]:
    out = out or root / "site"
    assets = root / "assets" / "img"
    if out.exists():
        shutil.rmtree(out)
    copy_shared(out, assets)
    linux_src = root / "linux"
    has_linux = linux_src.is_dir() and any(linux_src.glob("*.md"))
    built = {"main": build_course(MAIN, root / "main", out, assets, has_linux)}
    if has_linux:
        built["linux"] = build_course(LINUX, linux_src, out / "linux", assets)
    return built


if __name__ == "__main__":
    try:
        result = build_all()
    except LessonError as e:
        sys.exit(f"Lesson error: {e}")
    print(", ".join(f"{k}: {len(v)} lessons" for k, v in result.items()), "-> site/")
