#!/usr/bin/env python3

"""Computer Vision module."""
import cv2
import numpy

camera = cv2.VideoCapture(0)


class LineDetector:
    """Canny Line Detector."""

    def __init__(self, cam: cv2.VideoCapture):
        self.cam = cam  # Store reference to the VideoCapture object

    def fetch_image(self, flag: int = 1) -> numpy.ndarray:
        """Read an image from camera."""
        ret, frame = self.cam.read()
        if ret:
            return frame
        else:
            raise ValueError("Frame not Available.")


if __name__ == "__main__":
    ll = LineDetector(camera)
    try:
        while True:
            frame = ll.fetch_image()
            cv2.imshow("frame", frame)
            cv2.waitKey(0)
    except KeyboardInterrupt:
        cv2.destroyAllWindows()
