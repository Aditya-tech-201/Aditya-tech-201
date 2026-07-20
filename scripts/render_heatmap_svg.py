"""Render data/contributions.json as a self-contained animated SVG."""

import json
from datetime import date, timedelta
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data/contributions.json"
OUTPUT = ROOT / "contrib-heatmap.svg"
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

data = json.loads(INPUT.read_text(encoding="utf-8"))
by_date = {date.fromisoformat(item["date"]): item for item in data["days"]}
last_day = max(by_date)
start = last_day - timedelta(days=370)
start -= timedelta(days=(start.weekday() + 1) % 7)
cell, gap, left, top = 12, 4, 48, 48
rects = []
for offset in range(53 * 7):
    current = start + timedelta(days=offset)
    week, weekday = divmod(offset, 7)
    item = by_date.get(current, {"count": 0, "level": 0})
    x, y = left + week * (cell + gap), top + weekday * (cell + gap)
    delay = min(2.4, (week + weekday) * 0.035)
    label = f"{current.isoformat()}: {item['count']} contributions"
    rects.append(f'''<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{PALETTE[item['level']]}" opacity="0" transform="translate(0 -5)"><title>{escape(label)}</title><animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.22s" fill="freeze"/><animateTransform attributeName="transform" type="translate" from="0 -5" to="0 0" begin="{delay:.2f}s" dur="0.22s" fill="freeze"/></rect>''')

labels = [("Sun", 58), ("Mon", 74), ("Wed", 106), ("Fri", 138)]
day_labels = "".join(f'<text x="8" y="{y}" class="muted">{name}</text>' for name, y in labels)
legend = "".join(f'<rect x="{710 + i * 18}" y="178" width="12" height="12" rx="3" fill="{color}"/>' for i, color in enumerate(PALETTE))
stats = data["stats"]
svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="860" height="225" viewBox="0 0 860 225" role="img" aria-label="GitHub contribution heatmap">
<style>text {{ font-family: Consolas, 'Courier New', monospace; font-size: 12px; }} .title {{ fill:#f0f6fc; font-size:15px; }} .muted {{ fill:#8b949e; }}</style>
<rect width="100%" height="100%" rx="8" fill="#0d1117" stroke="#30363d"/>
<text x="22" y="27" class="title">{escape(data['username'])}'s contribution activity</text>{day_labels}
{''.join(rects)}
<text x="662" y="188" class="muted">Less</text>{legend}<text x="804" y="188" class="muted">More</text>
<text x="22" y="207" class="muted">{stats['total']:,} contributions in the last year  ·  current streak: {stats['current_streak']} days  ·  longest: {stats['longest_streak']} days</text>
</svg>'''
OUTPUT.write_text(svg, encoding="utf-8")
print(f"Generated: {OUTPUT}")
