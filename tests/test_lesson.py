import textwrap, pytest
from course.lesson import parse_lesson, LessonError, SECTIONS

GOOD = textwrap.dedent('''\
    ---
    letter: A
    title: The Parts of a Computer
    image: psych
    ---

    ## What went wrong
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
    assert l.sections["What went wrong"].strip() == "**Psych:** Hello."
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

def test_hash_lines_inside_code_blocks_are_not_sections(tmp_path):
    text = GOOD.replace("1. Do it.", "1. Do it.\n\n```bash\n## not a heading\nls -l\n```\n")
    l = parse_lesson(write(tmp_path, text))
    assert "## not a heading" in l.sections["The Mender's way"]

def test_level_front_matter(tmp_path):
    assert parse_lesson(write(tmp_path, GOOD)).level is None
    l = parse_lesson(write(tmp_path, GOOD.replace("image: psych", "image: psych\nlevel: 2")))
    assert l.level == 2
