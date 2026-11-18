"""Check the built site: every local link and image resolves, and each course has 26 lessons.

    python scripts/check_site.py [site_dir]
"""
import pathlib, re, sys
from urllib.parse import urlparse

SITE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / "site")
REF = re.compile(r'(?:href|src)="([^"]+)"')
COURSES = {"main": SITE, "linux": SITE / "linux"}


def main():
    problems = []
    for name, d in COURSES.items():
        if not (d / "index.html").exists():
            if name == "main":
                problems.append("no site/index.html")
            continue
        lessons = [p for p in d.glob("*.html") if re.match(r"[a-z]-", p.name)]
        if len(lessons) != 26:
            problems.append(f"{name}: expected 26 lesson pages, found {len(lessons)}")
    pages = sorted(SITE.rglob("*.html"))
    ids = {p.resolve(): set(re.findall(r'id="([^"]+)"', p.read_text(encoding="utf-8"))) for p in pages}
    for p in pages:
        rel = p.relative_to(SITE)
        for ref in REF.findall(p.read_text(encoding="utf-8")):
            u = urlparse(ref)
            if u.scheme in ("http", "https", "mailto", "data", "tel"):
                continue
            target = (p.parent / u.path).resolve() if u.path else p.resolve()
            if not target.exists():
                problems.append(f"{rel}: missing {ref}")
            elif u.fragment and target.suffix == ".html" and u.fragment not in ids.get(target, set()):
                problems.append(f"{rel}: missing anchor {ref}")
    if problems:
        print("\n".join(problems))
        sys.exit(1)
    print(f"OK: {len(pages)} pages, all links resolve")


if __name__ == "__main__":
    main()
