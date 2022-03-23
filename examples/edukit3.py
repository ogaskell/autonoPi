#!/usr/bin/env python3

"""Implementation of autonoPi for the testing vehicle.

Hardware:
- Raspberry Pi 4
- Waveshare LiPo hat
- Raspberry Pi Camera v1.3
- CamJam EduKit 3
- Custom 3D printed chassis
"""

import cv2

from autonopi.cv import LineDetector
from autonopi.hardware.motion.edukit import EduKit3 as EK3Motion
from autonopi.management import Manager
from autonopi.navigation import Navigation


class EduKit3Manager(Manager):
    """This is the implementation of the management system that will run on this hardware."""

    def setup_components(self) -> None:
        """Setup the components this implementation uses."""
        self.navigation = Navigation()
        self.line_detector = LineDetector(rotation=cv2.ROTATE_180)
        self.motion = EK3Motion()
