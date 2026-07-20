from pathlib import Path

import cv2

from utils.ascii_utils import resize_image
from utils.ascii_utils import image_to_ascii
from utils.svg_utils import ascii_to_svg

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "assets/source-prepped.png"
OUTPUT = ROOT / "avi-ascii.svg"

img = cv2.imread(str(INPUT), cv2.IMREAD_GRAYSCALE)
if img is None:
    raise FileNotFoundError(f"Could not read {INPUT}. Run prep_photo.py first.")

img = resize_image(img, width=85)

ascii_rows = image_to_ascii(img)

svg = ascii_to_svg(ascii_rows)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(svg)

print("Generated:", OUTPUT)
