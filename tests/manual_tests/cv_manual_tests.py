"""Non-automated test methods for cv.py."""

import os
import sys

import cv2

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


if __name__ == "__main__":
    test_filter()
