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
