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

def test_build_linux_course(tmp_path):
    src = tmp_path / "linux"; src.mkdir()
    fixture = ROOT / "tests" / "fixtures" / "A-parts-of-a-computer.md"
    (src / "A-what-is-linux.md").write_text(fixture.read_text().replace("image: psych", "image: psych\nlevel: 1"))
    out = tmp_path / "site"
    lessons = build.build_course(build.LINUX, src, out / "linux", ROOT / "assets" / "img")
    assert [l.letter for l in lessons] == ["A"]
    for f in ["index.html", "handbook.html", "a-what-is-linux.html"]:
        assert (out / "linux" / f).exists(), f
    page = (out / "linux" / "a-what-is-linux.html").read_text()
    assert 'href="../style.css"' in page and 'src="../img/psych.png"' in page
    idx = (out / "linux" / "index.html").read_text()
    assert "Level 1" in idx
