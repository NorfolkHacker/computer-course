import pathlib, shutil
import build
ROOT = pathlib.Path(__file__).parent.parent

def test_build_fixture(tmp_path):
    src = tmp_path / "src"; src.mkdir()
    fixture = ROOT / "tests" / "fixtures" / "A-parts-of-a-computer.md"
    shutil.copy(fixture, src / fixture.name)
    (src / "B-mouse.md").write_text(fixture.read_text().replace("letter: A", "letter: B"))
    out = tmp_path / "site"
    lessons = build.build(src, out, ROOT / "assets" / "img")
    assert [l.letter for l in lessons] == ["A", "B"]
    for f in ["index.html", "handbook.html", "a-parts-of-a-computer.html", "b-mouse.html", "style.css", "app.js", "img/psych.png"]:
        assert (out / f).exists(), f
    idx = (out / "index.html").read_text()
    assert 'href="a-parts-of-a-computer.html"' in idx and 'href="handbook.html"' in idx
    a = (out / "a-parts-of-a-computer.html").read_text()
    assert 'href="b-mouse.html"' in a
