from rembg import remove
import cv2
import numpy as np
import os

from utils.image_utils import detect_face, clahe

INPUT_IMAGE = "assets/photo.jpg"
OUTPUT_IMAGE = "assets/source-prepped.png"
TEMP_IMAGE = "assets/temp.png"

print("Removing background...")

with open(INPUT_IMAGE, "rb") as inp:
    output = remove(inp.read())

with open(TEMP_IMAGE, "wb") as out:
    out.write(output)

img = cv2.imread(TEMP_IMAGE, cv2.IMREAD_UNCHANGED)

alpha = img[:, :, 3]

gray = cv2.cvtColor(
    img[:, :, :3],
    cv2.COLOR_BGR2GRAY
)

box = detect_face(img[:, :, :3])

if box:

    x1, y1, x2, y2 = box

    gray = gray[y1:y2, x1:x2]
    alpha = alpha[y1:y2, x1:x2]

gray = clahe(gray)

white = np.full(gray.shape, 255, np.uint8)

white[alpha > 0] = gray[alpha > 0]

cv2.imwrite(OUTPUT_IMAGE, white)

os.remove(TEMP_IMAGE)

print("Saved:", OUTPUT_IMAGE)