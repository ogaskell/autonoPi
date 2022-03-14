#!/usr/bin/env python3

"""Computer Vision module."""
import cv2

camera = cv2.VideoCapture(0)


class LineDetector:
    """Canny Line Detector."""

    def __init__(self, cam: cv2.VideoCapture):
        self.cam = cam  # Store reference to the VideoCapture object

    def fetch_image(self, flag: int = 1) -> cv2.OutputArray:
        """Read an image from camera."""
        ret, frame = self.cam.read()
        if ret:
            return frame
        else:
            raise ValueError("Frame not Available.")
