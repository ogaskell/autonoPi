#!/usr/bin/env python3

"""Computer Vision module."""
from math import floor

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

    def v_crop(self, image: np.ndarray, top: float, bottom: float = 0.0, blkbar: bool = False) -> np.ndarray:
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
        blkbar : bool, default False
            If this is false, normal behavior is used.
            Otherwise, instead of cropping the original image and chaning the dimensions, the areas that would be
            cropped are simply replaced with black bars. This means the coordinates are retained between the input and
            output images, in case and references need to be maintained between them.

        Returns
        -------
        np.ndarray
            The cropped image.
        """
        if bottom > top:
            raise ValueError("Image bottom > top ({:1.2f} > {:1.2f})".format(bottom, top))
        height, width, _ = image.shape

        # Top and bottom in pixels
        # Note, 1 - (top, bottom) is used since numpy indexes from the top of the image.
        top_pix, bottom_pix = floor((1 - top) * height), floor((1 - bottom) * height)

        if not blkbar:
            return image[top_pix:bottom_pix, 0:width]
        else:
            result = image.copy()  # Create copy of image so I don't overwrite the input image unintentionally

            # Top bar
            if top_pix != 0:  # Don't need to do anything if top_pix is 0, since this would crop nothing
                top_box = [[0, 0],
                           [width - 1, 0],
                           [width - 1, top_pix - 1],  # Ensure top_pix isn't included
                           [0, top_pix - 1],
                           ]

                # Needs to be an ndarray, with dtype int32.
                top_box_np = np.array(top_box, dtype=np.int32)
                # OpenCV wants it nested and since it's an ndarray this is the easiest way
                top_box_np = top_box_np.reshape(1, -1, 2)

                result = cv2.fillPoly(result,
                                      top_box_np,
                                      [0] * result.ndim,  # Fill with black. Works on RGB and monochrome images.
                                      )

            if bottom_pix != 0:
                bottom_box = [[0, height - 1],
                              [width - 1, height - 1],
                              [width - 1, bottom_pix + 1],  # Ensure bottom_pix isn't included
                              [0, bottom_pix + 1],
                              ]

                bottom_box_np = np.array(bottom_box, dtype=np.int32)
                bottom_box_np = bottom_box_np.reshape(1, -1, 2)

                result = cv2.fillPoly(result,
                                      bottom_box_np,
                                      [0] * result.ndim,  # Fill with black
                                      )

            return result
