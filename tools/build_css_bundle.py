#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ("v4.css", "01 CORE / LEGACY CASCADE"),
    ("v4-locale-v1.css", "02 LOCALE UI"),
    ("v4-request-modal-v1.css", "03 REQUEST MODAL"),
    ("v4-typography-v1.css", "04 STAGE 2 FUNCTIONAL TYPOGRAPHY"),
    ("v4-visual-v1.css", "05 STAGE 4 VISUAL UX"),
    ("v4-impact-v1.css", "06 STAGE 5 PORTFOLIO IMPACT"),
]
OUTPUT = ROOT / "v4-bundle-v1.css"
INDEX = ROOT / "index.html"


def read(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"Missing CSS source: {path.name}")
    return path.read_text(encoding="utf-8").strip()


parts = [
    "/* VANTA R1 — generated CSS bundle v1.\n"
    "   Source order is contractual: do not reorder without visual-regression QA.\n"
    "   Regenerate with: python3 tools/build_css_bundle.py */"
]
for filename, label in SOURCES:
    parts.append(f"/* ===== {label}: {filename} ===== */\n{read(ROOT / filename)}")

OUTPUT.write_text("\n\n".join(parts) + "\n", encoding="utf-8")

html = INDEX.read_text(encoding="utf-8")
old_links = (
    '<link href="v4.css?v=23" rel="stylesheet"/>'
    '<link href="v4-locale-v1.css?v=3" rel="stylesheet"/>'
    '<link href="v4-request-modal-v1.css?v=6" rel="stylesheet"/>'
    '<link href="v4-typography-v1.css?v=1" rel="stylesheet"/>'
)
previous_link = '<link href="v4-bundle-v1.css?v=1" rel="stylesheet"/>'
new_link = '<link href="v4-bundle-v1.css?v=2" rel="stylesheet"/>'

if old_links in html:
    html = html.replace(old_links, new_link, 1)
elif previous_link in html:
    html = html.replace(previous_link, new_link, 1)
elif new_link not in html:
    raise SystemExit("Expected stylesheet link sequence was not found in index.html")

INDEX.write_text(html, encoding="utf-8")
print(f"Built {OUTPUT.name} from {len(SOURCES)} sources and normalized index.html")
