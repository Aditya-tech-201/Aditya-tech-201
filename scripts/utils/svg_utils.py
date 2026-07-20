"""
svg_utils.py

Converts ASCII rows into an animated SVG.
"""

import html

from utils.animation_utils import row_delay, row_duration


FONT_SIZE = 10
LINE_HEIGHT = 12
CHAR_WIDTH = 7
FONT = "Consolas, 'Courier New', monospace"

BACKGROUND = "#0d1117"
FOREGROUND = "#c9d1d9"


def ascii_to_svg(ascii_rows):

    width = max(len(r) for r in ascii_rows) * CHAR_WIDTH + 20
    height = len(ascii_rows) * LINE_HEIGHT + 20

    svg = []

    svg.append(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"
viewBox="0 0 {width} {height}" role="img" aria-label="Animated ASCII portrait">
<rect width="100%" height="100%" rx="8" fill="{BACKGROUND}"/>
<style>
  .cursor {{ fill: #58a6ff; }}
</style>''')

    y = 15

    for i, row in enumerate(ascii_rows):

        row = html.escape(row)

        delay = row_delay(i)

        duration = row_duration()

        clip_id = f"row-{i}"
        svg.append(f'''
<clipPath id="{clip_id}"><rect x="10" y="{y - FONT_SIZE}" width="0" height="{LINE_HEIGHT}">
  <animate attributeName="width" from="0" to="{width - 20}" begin="{delay}s" dur="{duration}s" fill="freeze"/>
</rect></clipPath>
<text x="10" y="{y}" font-family="{FONT}" font-size="{FONT_SIZE}" fill="{FOREGROUND}" xml:space="preserve" clip-path="url(#{clip_id})">{row}</text>''')

        y += LINE_HEIGHT

    svg.append("</svg>")

    return "\n".join(svg)
