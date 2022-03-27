#!/usr/bin/env python3

"""Implementation of autonoPi for the testing vehicle.

Hardware:
- Raspberry Pi 4
- Waveshare LiPo hat
- Raspberry Pi Camera v1.3
- CamJam EduKit 3
- Custom 3D printed chassis
"""

from math import floor

import cv2
import numpy as np

from autonopi.cv import LineDetector, camera
from autonopi.hardware.motion.edukit import EduKit3 as EK3Motion
from autonopi.management import Manager
from autonopi.navigation import Navigation


class EduKit3Manager(Manager):
    """This is the implementation of the management system that will run on this hardware."""

    def __init__(self, vis: bool = False):
        super().__init__()

        self.visualise = vis  # Whether or not to display CV Visualisations.

    def setup_components(self) -> None:
        """Setup the components this implementation uses."""
        self.navigation = Navigation()
        self.line_detector = LineDetector(camera, rotate=cv2.ROTATE_180)
        self.motion = EK3Motion()

    def setup_variables(self) -> None:
        """Setup variables the class will use."""
        # This may be updated by the navigation or CV systems as different lanes are travelled.
        # Equal to 210 degrees hue, halfway between cyan and blue.
        self.target_hue = 105

    def get_lane_angle(self) -> float:
        """Get the angle of the lane in front of the camera.

        Uses the Computer Vision component.
        """
        frame = self.line_detector.fetch_image()

        mask = self.line_detector.filter_hsv(frame,
                                             hue=self.target_hue,
                                             sat=[38, 255],
                                             val=[38, 255],
                                             hue_tol=15,
                                             )

        edges = self.line_detector.canny(mask)
        cropped = self.line_detector.v_crop(edges, 0.35, 0.01, True)
        hough_lines = self.line_detector.houghP(cropped)

        if hough_lines is not None:  # Ensure some lines have been detected
            hough_lines = hough_lines.reshape(1, -1, 4)[0]
            l_split, r_split = self.line_detector.split_lines(hough_lines, frame.shape[1], bounds=[0, 0.4])

            lane_t, lane_c = self.line_detector.lane_slope(l_split, r_split)

            if self.visualise:
                if len(l_split) > 0:
                    for x1, y1, x2, y2 in l_split:
                        cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

                if len(r_split) > 0:
                    for x1, y1, x2, y2 in r_split:
                        cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

                lane_m = 1 / np.tan(lane_t)
                bottom_x, bottom_y = (frame.shape[0] - lane_c) / lane_m, frame.shape[0]
                top_x, top_y = - lane_c / lane_m, 0

                cv2.line(frame, (floor(bottom_x), bottom_y), (floor(top_x), top_y), (0, 255, 0), 5)
        else:
            lane_t = 0.0
            l_split, r_split = [], []

        if self.visualise:
            cv2.imshow("CV Visualisation", frame)
            cv2.waitKey(20)

        return lane_t

    def angle_to_steering(self, angle: float) -> float:
        """Convert a lane angle to a steering amount.

        Takes an angle in radians and outputs a float from -1.0 to 1.0
        """
        # return (- angle / 15) # Diving by pi would allow full steering lock, however I would like to reduce max lock

        A = -0.12
        B = 0.4
        C = 0.12

        return A * np.log((B + C*angle) / (B - C*angle))

    def run(self) -> None:
        """Move the vehicle."""
        angle = self.get_lane_angle()
        steering = self.angle_to_steering(angle)

        self.motion.start_move()
        self.motion.power = 0.3
        self.motion.direction = steering

    def exit(self) -> None:
        """Ran when the program exists to ensure vehicle is stopped."""
        self.motion.stop_move()
