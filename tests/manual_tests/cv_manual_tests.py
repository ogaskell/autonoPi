"""Non-automated test methods for cv.py."""

import os
import sys
from math import floor

import cv2
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

# noqa required here as there's no way I can comply with E402.
from autonopi import cv  # noqa: E402


def show(title: str, image: np.ndarray) -> None:
    """Show an image, including handling closing the window."""
    cv2.imshow(title, image)
    key = cv2.waitKey(0)
    while key != 13:
        key = cv2.waitKey(0)
    cv2.destroyAllWindows()


def showmul(title: str, images: list[np.ndarray]) -> None:
    """Show multiple images in separate windows, similarly to show()."""
    for n, im in enumerate(reversed(images)):  # Reversed so the first image is on top.
        cv2.imshow(f"{title}, {len(images) - n}", im)

    key = cv2.waitKey(0)
    while key != 13:
        key = cv2.waitKey(0)
    cv2.destroyAllWindows()


def test_camera() -> None:
    """Test LineDetector.fetch_image()."""
    ll = cv.LineDetector(cv.camera)
    try:
        while True:
            frame = ll.fetch_image()
            cv2.imshow("frame", frame)
            cv2.waitKey(0)
    except KeyboardInterrupt:
        cv2.destroyAllWindows()


def test_filter() -> None:
    """Test LineDetector.filter_hsv()."""
    ll = cv.LineDetector(cv.camera)
    frame = cv2.imread("./CV_test.jpg")

    mask = ll.filter_hsv(frame,
                         hue=105,
                         sat=[38, 255],
                         val=[38, 255],
                         hue_tol=15
                         )

    show("mask", mask)


def test_crop() -> None:
    """Test LineDetector.v_crop()."""
    ll = cv.LineDetector(cv.camera)
    frame = cv2.imread("./CV_test.jpg")

    cropped_frame = ll.v_crop(frame, 0.6, 0.0)

    show("cropped image", cropped_frame)


def test_canny() -> None:
    """Test LineDetector.canny()."""
    ll = cv.LineDetector(cv.camera)
    frame = ll.fetch_image()
    edges = ll.canny(frame)
    show("Edges", edges)


def test_stages() -> None:
    """Show all stages of the CV process."""
    ll = cv.LineDetector(cv.camera)
    img = cv2.imread("./CV_test2.jpg")
    mask = ll.filter_hsv(img,
                         hue=105,
                         sat=[38, 255],
                         val=[38, 255],
                         hue_tol=15
                         )
    crop = ll.v_crop(mask, 0.5, 0, True)
    edge = ll.canny(crop)
    hough = ll.houghP(edge)
    hough_im = img.copy()
    split_im = img.copy()

    if hough is not None:

        hough = hough.reshape(1, -1, 4)
        for x1, y1, x2, y2 in hough[0]:
            cv2.line(hough_im, (x1, y1), (x2, y2), (0, 255, 0), 2)

        l_split, r_split = ll.split_lines(hough[0], img.shape[1], bounds=[0, 0.5])

        if len(l_split > 0):
            for x1, y1, x2, y2 in l_split:
                cv2.line(split_im, (x1, y1), (x2, y2), (255, 0, 0), 2)
        else:
            print("No Left Lines")

        if len(r_split > 0):
            for x1, y1, x2, y2 in r_split:
                cv2.line(split_im, (x1, y1), (x2, y2), (0, 0, 255), 2)
        else:
            print("No Right Lines")

        lane_t, lane_c = ll.lane_slope(l_split, r_split)
        lane_m = 1 / np.tan(lane_t)
        bottom_x, bottom_y = (img.shape[0] - lane_c) / lane_m, img.shape[0]
        top_x, top_y = - lane_c / lane_m, 0

        cv2.line(split_im, (floor(bottom_x), bottom_y), (floor(top_x), top_y), (0, 255, 0), 5)

    showmul("CV Test", [img, mask, crop, edge, hough_im, split_im])


if __name__ == "__main__":
    test_filter()
    test_crop()
    test_canny()
    test_stages()
