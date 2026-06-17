import cv2
import numpy as np

def detect_lane(frame):

    height, width = frame.shape[:2]

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    blur = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    edges = cv2.Canny(
        blur,
        50,
        150
    )

    mask = np.zeros_like(edges)

    polygon = np.array([[

        (0, height),
        (width, height),
        (width, int(height * 0.6)),
        (0, int(height * 0.6))

    ]])

    cv2.fillPoly(mask, polygon, 255)

    roi = cv2.bitwise_and(
        edges,
        mask
    )

    lines = cv2.HoughLinesP(
        roi,
        1,
        np.pi / 180,
        50,
        minLineLength=100,
        maxLineGap=50
    )

    left_x = []
    right_x = []

    crossed = False

    if lines is not None:

        for line in lines:

            x1, y1, x2, y2 = line[0]

            slope = (y2 - y1) / (x2 - x1 + 1e-6)

            if abs(slope) < 0.5:
                continue

            if slope < 0:
                left_x.extend([x1, x2])
            else:
                right_x.extend([x1, x2])

        if left_x and right_x:

            left_boundary = int(np.mean(left_x))
            right_boundary = int(np.mean(right_x))

            lane_center = (
                left_boundary +
                right_boundary
            ) // 2

            car_center = width // 2

            offset = abs(
                car_center -
                lane_center
            )

            if offset > 80:
                crossed = True

    return crossed
