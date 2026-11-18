"""Check the built site: every local link and image resolves, and all 26 lessons exist.

    python scripts/check_site.py [site_dir]
"""
import pathlib, re, sys
from urllib.parse import urlparse

SITE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / "site")
REF = re.compile(r'(?:href|src)="([^"]+)"')


def main():
    problems = []
    pages = sorted(SITE.glob("*.html"))
    lessons = [p for p in pages if re.match(r"[a-z]-", p.name)]
    if len(lessons) != 26:
        problems.append(f"expected 26 lesson pages, found {len(lessons)}")
    ids = {}
    for p in pages:
        ids[p.name] = set(re.findall(r'id="([^"]+)"', p.read_text(encoding="utf-8")))
    for p in pages:
        for ref in REF.findall(p.read_text(encoding="utf-8")):
            u = urlparse(ref)
            if u.scheme in ("http", "https", "mailto", "data", "tel"):
                continue
            target = u.path or p.name
            if not (SITE / target).exists():
                problems.append(f"{p.name}: missing {ref}")
            elif u.fragment and target.endswith(".html") and u.fragment not in ids.get(target, set()):
                problems.append(f"{p.name}: missing anchor {ref}")
    if problems:
        print("\n".join(problems))
        sys.exit(1)
    print(f"OK: {len(pages)} pages, {len(lessons)} lessons, all links resolve")


if __name__ == "__main__":
    main()
