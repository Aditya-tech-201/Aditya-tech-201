"""Create an animated neofetch-style SVG profile card."""

from pathlib import Path
from xml.sax.saxutils import escape

from profile_config import PROFILE

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "info-card.svg"


def reveal(content: str, delay: float) -> str:
    return f'''<g opacity="0" transform="translate(-8 0)"><animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.22s" fill="freeze"/><animateTransform attributeName="transform" type="translate" from="-8 0" to="0 0" begin="{delay:.2f}s" dur="0.22s" fill="freeze"/>{content}</g>'''


y, delay = 76, 0.25
content = []
for label, value in PROFILE["system"]:
    content.append(reveal(f'<text x="24" y="{y}" class="key">{escape(label):<10}</text><text x="132" y="{y}" class="value">: {escape(value)}</text>', delay))
    y, delay = y + 24, delay + 0.10

for heading, items in PROFILE["sections"]:
    y += 12
    content.append(reveal(f'<text x="24" y="{y}" class="heading">{escape(heading)}</text>', delay))
    y, delay = y + 23, delay + 0.10
    for item in items:
        content.append(reveal(f'<text x="40" y="{y}" class="value">• {escape(item)}</text>', delay))
        y, delay = y + 21, delay + 0.08

height = y + 18
svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="490" height="{height}" viewBox="0 0 490 {height}" role="img" aria-label="{escape(PROFILE['name'])} profile card">
<style>
  text {{ font-family: Consolas, 'Courier New', monospace; font-size: 14px; }}
  .key {{ fill: #58a6ff; }} .value {{ fill: #c9d1d9; }} .heading {{ fill: #39d353; font-weight: bold; }} .muted {{ fill: #8b949e; }}
</style>
<rect width="100%" height="100%" rx="8" fill="#0d1117" stroke="#30363d"/>
<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="0s" dur="0.22s" fill="freeze"/>
  <text x="20" y="31" fill="#f0f6fc">{escape(PROFILE['name']).upper()}</text>
  <text x="20" y="53" class="muted">{escape(PROFILE['role'])}</text>
</g>
{''.join(content)}
</svg>'''
OUTPUT.write_text(svg, encoding="utf-8")
print(f"Generated: {OUTPUT}")
