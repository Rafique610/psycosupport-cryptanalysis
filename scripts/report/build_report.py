"""Assemble report/sections/*.md into report.pdf with WeasyPrint. Standard-library + markdown + weasyprint."""

from pathlib import Path

import markdown
from weasyprint import HTML

ROOT = Path(__file__).resolve().parents[2]
SECTIONS = ROOT / "report/sections"
OUT = ROOT / "report.pdf"

ORDER = [
    "00-front.md", "01-deployment.md", "02-capture.md", "02b-input-analysis.md",
    "03a-frequency.md", "03b-key-recovery.md", "03c-decryption.md",
    "04-security-analysis.md", "05-reflection.md", "06-references.md", "07-appendix.md",
]

CSS = """
@page { size: A4; margin: 2cm; @bottom-center { content: counter(page); color: #52514e; font-size: 9pt; } }
body { font-family: "DejaVu Sans", sans-serif; font-size: 10.5pt; line-height: 1.45; color: #0b0b0b; }
h1 { font-size: 17pt; border-bottom: 2px solid #2a78d6; padding-bottom: 3px; page-break-before: always; }
h1:first-of-type, .title-page + h1 { page-break-before: auto; }
h2 { font-size: 13pt; color: #11315c; margin-top: 1.1em; }
h3, h4 { font-size: 11pt; color: #11315c; }
p, li { text-align: justify; }
a { color: #2a78d6; text-decoration: none; }
table { border-collapse: collapse; width: 100%; margin: 0.8em 0; font-size: 9.2pt; }
th, td { border: 1px solid #c9c8c3; padding: 3px 6px; text-align: left; vertical-align: top; }
th { background: #eef3fb; }
code { font-family: "DejaVu Sans Mono", monospace; font-size: 8.8pt; background: #f4f4f2; padding: 0 2px; }
pre { background: #f6f6f4; border: 1px solid #e0dfdb; border-radius: 4px; padding: 7px 9px;
      font-size: 8.3pt; line-height: 1.3; white-space: pre-wrap; word-break: break-word; page-break-inside: avoid; }
pre code { background: none; padding: 0; }
blockquote { border-left: 3px solid #a9a8a3; margin: 0.6em 0; padding: 0.1em 0 0.1em 12px; color: #333; }
img { max-width: 100%; }
table, figure, img { page-break-inside: avoid; }
.title-page { text-align: center; page-break-after: always; padding-top: 5cm; }
.title-page .uni { color: #52514e; font-size: 11pt; }
.title-page .title { font-size: 30pt; border: none; margin: 0.3em 0 0; page-break-before: auto; }
.title-page .subtitle { font-size: 12pt; color: #333; font-style: italic; margin: 0.4em 2cm 1.4em; }
.title-page .meta { font-size: 11pt; margin: 0.3em 0; }
"""


def build():
    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "attr_list", "md_in_html"])
    html_body = "\n".join(md.reset().convert((SECTIONS / name).read_text()) for name in ORDER)
    doc = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{html_body}</body></html>"
    HTML(string=doc, base_url=str(SECTIONS)).write_pdf(OUT)
    print(f"wrote {OUT.relative_to(ROOT)} from {len(ORDER)} sections")


if __name__ == "__main__":
    build()
