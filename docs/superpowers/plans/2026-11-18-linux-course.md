# Linux Course Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Add the Linux A–Z course at `site/linux/` with Debian/Fedora/Arch tabs.

**Architecture:** Generalise `build.py` around a `Course` config so it builds both courses; extend parser (fenced-code safety, `level`) and renderer (tabs, asset prefix).

**Tech Stack:** as main course.

**Spec:** `docs/superpowers/specs/2026-11-18-linux-course-design.md`

## Global Constraints

- Main course URLs and output unchanged.
- Tabs: Debian / Fedora / Arch; remembered under localStorage key `linux-distro` (try/catch); all visible without JS and in print.
- Lesson sections and quiz rules exactly as the main course; Linux lessons need `level: 1–4`.
- Commit as NorfolkHacker, messages end with the Co-Authored-By line.

---

### Task 1: Parser — fenced-code safety and `level`
- [ ] Test: a lesson whose Mender section contains a ```bash block with a `## comment` line parses, and the comment stays in the section.
- [ ] Test: `level: 2` front matter → `Lesson.level == 2`; missing → `None`.
- [ ] Implement: mask fenced blocks before splitting on `^## `; add `level: int | None` to `Lesson` (last field, default None).

### Task 2: Renderer + build generalisation
- [ ] `render.lesson_body(lesson, img_prefix, tabs=False)`: when `tabs`, platform groups get `class="platforms tabs"` and each platform div gets `data-tab="<name>"`.
- [ ] `_PLATFORM_H3` matches `On (Windows|Android|Debian|Fedora|Arch)`.
- [ ] `render.page(..., root="")` prefixes `style.css`, `app.js`, `index.html` home link; adds a link to the other course in the top nav.
- [ ] `build.Course` dataclass (key, src, out_sub, title, intro, tabs, levels, pdf_name); `build.build(src, out, assets)` keeps working for the main course (tests unchanged); new `build.build_all(root, out)` builds both.
- [ ] Linux index groups cards by level; main index gets a "Next: the Linux course" section.
- [ ] `app.js`: builds a tab bar for each `.platforms.tabs` from `data-tab`, shows the remembered distro, saves the choice; progress/quiz unchanged.
- [ ] CSS: tab bar, `pre` code blocks (scrollable, copy-friendly), print shows all tabs.
- [ ] Tests: tab markup, root prefix, build of a fixture Linux course into `out/linux/`.

### Task 3: Linux exemplar + style addendum
- [ ] `linux/A-what-is-linux.md` written by the lead; `docs/linux-style-guide.md` addendum (distro cast, tabs, code-block rules, accuracy notes per family).

### Task 4: Lessons B–Z
- [ ] Four parallel writers: B–F, G–N, O–U, V–Z. Build must pass after each.
- [ ] Lead review: accuracy of commands per family, no destructive commands in "Do it now" outside a VM, voice.

### Task 5: Checks, PDF, deploy
- [ ] `check_site.py` covers both courses; `make_pdf.sh` makes both PDFs; workflow unchanged except check.
- [ ] Push, watch the deploy, verify live at desktop and phone width.
