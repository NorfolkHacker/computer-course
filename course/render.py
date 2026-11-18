"""Turn Lesson objects into HTML."""
from __future__ import annotations
import re
from html import escape

import markdown as _markdown

from .lesson import Lesson

SITE_TITLE = "The Operator's Computer Course"

ICONS = {
    "Cold open": "🎬",
    "The Operator says": "☠️",
    "The Mender's way": "🧵",
    "Do it now": "✋",
    "Quiz": "❓",
    "Scribble watch": "🖍️",
}

# Order the sections are shown in (matches the spec; Quiz comes from lesson.quiz).
ORDER = ["Cold open", "The Operator says", "The Mender's way", "Do it now", "Quiz", "Scribble watch"]


def md(text: str) -> str:
    return _markdown.markdown(text, extensions=["extra", "sane_lists"])


def kebab(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


_PLATFORM_H3 = re.compile(r"<h3>\s*On (Windows|Android)\b.*?</h3>", re.S)


def wrap_platforms(html: str) -> str:
    """Wrap each '### On Windows/Android' chunk in a div; group neighbours in .platforms."""
    chunks = re.split(r"(?=<h3>)", html)
    out, group = [], []

    def flush():
        if group:
            out.append('<div class="platforms">' + "".join(group) + "</div>")
            group.clear()

    for chunk in chunks:
        m = _PLATFORM_H3.match(chunk)
        if m:
            group.append(f'<div class="platform platform-{m.group(1).lower()}">{chunk}</div>')
        else:
            flush()
            out.append(chunk)
    flush()
    return "".join(out)


def quiz_html(lesson: Lesson) -> str:
    parts = []
    for n, q in enumerate(lesson.quiz, 1):
        opts = "".join(
            f'<button type="button" class="opt" data-i="{i}"><span class="opt-l">{"ABCD"[i]}</span> {escape(o)}</button>'
            for i, o in enumerate(q.options)
        )
        parts.append(
            f'<fieldset class="q" data-answer="{q.answer}">'
            f"<legend>{n}. {escape(q.q)}</legend>"
            f'<div class="opts">{opts}</div>'
            f'<p class="why"><strong>Answer: {"ABCD"[q.answer]}.</strong> {escape(q.why)}</p>'
            "</fieldset>"
        )
    return "".join(parts)


def section(name: str, inner: str) -> str:
    return (
        f'<section class="s s-{kebab(name)}">'
        f'<h2><span class="ico" aria-hidden="true">{ICONS[name]}</span> {escape(name)}</h2>'
        f"{inner}</section>"
    )


def lesson_body(lesson: Lesson, img_prefix: str = "img/") -> str:
    hero = (
        f'<img class="hero" src="{img_prefix}{escape(lesson.image)}.png" alt="">' if lesson.image else ""
    )
    head = (
        f'<header class="lesson-head"><div class="big-letter" aria-hidden="true">{escape(lesson.letter)}</div>'
        f'<div><p class="kicker">Lesson {escape(lesson.letter)}</p><h1>{escape(lesson.title)}</h1></div>{hero}</header>'
    )
    secs = []
    for name in ORDER:
        if name == "Quiz":
            secs.append(section(name, quiz_html(lesson)))
        else:
            inner = md(lesson.sections[name])
            if name == "The Mender's way":
                inner = wrap_platforms(inner)
            secs.append(section(name, inner))
    return (
        f'<article class="lesson" id="{lesson.slug}" data-slug="{lesson.slug}">{head}{"".join(secs)}</article>'
    )


def page(title: str, body: str, nav: str = "", body_class: str = "") -> str:
    full = escape(title) if title == SITE_TITLE else f"{escape(title)} · {escape(SITE_TITLE)}"
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&family=Patrick+Hand&display=swap">
<link rel="stylesheet" href="style.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🐄</text></svg>">
</head>
<body class="{body_class}">
<a class="skip" href="#main">Skip to the lesson</a>
<nav class="top"><a href="index.html" class="home">🐄 {escape(SITE_TITLE)}</a></nav>
<main id="main">
{body}
</main>
{nav}
<script src="app.js"></script>
</body>
</html>
"""
