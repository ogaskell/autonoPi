#!/usr/bin/env python3

"""Computer Vision module."""
import cv2
import numpy as np

camera = cv2.VideoCapture(0)


class LineDetector:
    """Canny Line Detector."""

    def __init__(self, cam: cv2.VideoCapture):
        self.cam = cam  # Store reference to the VideoCapture object

    def fetch_image(self, flag: int = 1) -> np.ndarray:
        """Read an image from camera."""
        ret, frame = self.cam.read()
        if ret:
            return frame
        else:
            raise ValueError("Frame not Available.")

    def filter_hsv(self,
                   frame: np.ndarray,
                   hue: float,
                   sat: list[float],
                   val: list[float],
                   hue_tol: float = 45) -> np.ndarray:
        """Filter an image using a given HSV filter.

        Parameters
        ----------
        frame: np.adarray,
            The image to process.
        hue : float
            The target hue, in range 0 - 180.
            Note that since OpenCV uses 0 - 180 for hue, degree values must be halved.
        sat : list of floats
            Inclusive range of saturation values, range 0 - 255.
            Must be of length 2.
        val : list of floats
            Inclusive range of value values, range 0 - 255.
            Must be of length 2.
        hue_tol : float, default 22.5
            Tolerance in hue, defines a range of hues to allow.
            Note that since OpenCV uses 0 - 180 for hue, the default value is equivalent to 45°.

        Returns
        -------
        np.ndarray
            A monochrome image, white representing areas of the image which
             match the filter conditions.
        """
        hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        low_bound = np.array([(hue - hue_tol) % 180,
                              sat[0],
                              val[0],
                              ])

        high_bound = np.array([(hue + hue_tol) % 180,  # Modulus allows hue to "wrap around"
                               sat[1],
                               val[1],
                               ])

        mask = cv2.inRange(hsv_image, low_bound, high_bound)

        return mask

    def v_crop(self, image: np.ndarray, top: float, bottom: float = 0.0) -> np.ndarray:
        """Crop an image vertically between bottom and top.

        Parameters
        ----------
        image : np.ndarray
            The image to crop.
        top : float
            Float between 0.0 and 1.0 representing the position of the top of the crop.
        bottom : float
            Float between 0.0 and 1.0 representing the position of the bottom of the crop.
            Must be less than top.

        Returns
        -------
        np.ndarray
            The cropped image.
        """
        pass
