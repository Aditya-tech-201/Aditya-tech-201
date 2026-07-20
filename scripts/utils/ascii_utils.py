import cv2
import numpy as np

# Bright -> dark. The leading space ensures a white background becomes empty.
ASCII_RAMP = " .`:-=+*cs#%@"


def resize_image(image, width=85):
    """
    Resize while preserving aspect ratio.
    """

    h, w = image.shape

    aspect = h / w

    # Characters are taller than they are wide
    new_height = int(width * aspect * 0.55)

    resized = cv2.resize(
        image,
        (width, new_height),
        interpolation=cv2.INTER_AREA
    )

    return resized


def pixel_to_char(value):
    """
    Convert grayscale value into ASCII character.
    """

    index = int(value / 255 * (len(ASCII_RAMP) - 1))

    return ASCII_RAMP[index]


def image_to_ascii(image):

    rows = []

    for row in image:

        line = ""

        for pixel in row:

            line += pixel_to_char(pixel)

        rows.append(line)

    return rows
