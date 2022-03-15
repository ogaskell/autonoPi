"""Non-automated test methods for cv.py."""

import os
import sys

import cv2

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

# noqa required here as there's no way I can comply with E402.
from autonopi import cv  # noqa: E402


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


if __name__ == "__main__":
    test_camera()
