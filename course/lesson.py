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
    found, order = {}, []
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
    try:
        raw = yaml.safe_load(qm.group(1)) or []
    except yaml.YAMLError as e:
        _fail(path, f"quiz YAML error: {e}")
    if not isinstance(raw, list) or len(raw) != 3:
        _fail(path, f"quiz needs exactly 3 questions, has {len(raw) if isinstance(raw, list) else 0}")
    quiz = []
    for i, item in enumerate(raw, 1):
        for key in ("q", "options", "answer", "why"):
            if item.get(key) in (None, ""):
                _fail(path, f"quiz question {i} missing '{key}'")
        opts = [str(o) for o in item["options"]]
        if not 3 <= len(opts) <= 4:
            _fail(path, f"quiz question {i} needs 3-4 options")
        ans = item["answer"]
        if isinstance(ans, bool) or not isinstance(ans, int) or not 0 <= ans < len(opts):
            _fail(path, f"quiz question {i} answer {ans!r} out of range")
        quiz.append(Question(str(item["q"]), opts, ans, str(item["why"])))

    sections = {s: found[s] for s in SECTIONS if s != "Quiz"}
    return Lesson(letter, str(meta["title"]), path.stem.lower(), meta.get("image"), sections, quiz)
