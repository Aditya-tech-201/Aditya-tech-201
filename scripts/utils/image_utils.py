import cv2
import mediapipe as mp
import numpy as np


def detect_face(image):
    """
    Detect the largest face using MediaPipe.
    Returns (x1, y1, x2, y2)
    """

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    detector = mp.solutions.face_detection.FaceDetection(
        model_selection=1,
        min_detection_confidence=0.6
    )

    results = detector.process(rgb)

    if not results.detections:
        return None

    h, w = image.shape[:2]

    detection = max(
        results.detections,
        key=lambda d: d.location_data.relative_bounding_box.width
    )

    box = detection.location_data.relative_bounding_box

    x = int(box.xmin * w)
    y = int(box.ymin * h)
    bw = int(box.width * w)
    bh = int(box.height * h)

    padding = int(max(bw, bh) * 0.8)

    x1 = max(0, x - padding)
    y1 = max(0, y - padding)

    x2 = min(w, x + bw + padding)
    y2 = min(h, y + bh + padding)

    return x1, y1, x2, y2


def clahe(gray):

    clahe_filter = cv2.createCLAHE(
        clipLimit=2.5,
        tileGridSize=(8, 8)
    )

    return clahe_filter.apply(gray)