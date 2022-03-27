#!/usr/bin/env python3

"""Motion class for the CamJam EduKit 3."""

from gpiozero import CamJamKitRobot
from numpy import cos, pi, sin

from . import Motion


class EduKit3(Motion):
    """Two powered wheels, with differential steering, using hardware from the CamJam EduKit3.

    Supports reverse.
    """

    reverse = True

    def __init__(self, left_pol: bool = False, right_pol: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Run the parent class init method, passing through any args.

        self.robot = CamJamKitRobot()

        self.pol = (left_pol, right_pol)  # Polarity of motors. If True, reverse any motion of that motor.

    def move(self) -> None:
        """Move the car.

        This will take into account self.speed and self.direction and adjust the robot's `value` accordingly.
        """
        theta = - pi * self.direction + (pi/4)  # Angle assumes right is negative, while negative direction is right

        left_v = self.power * cos(theta)
        right_v = self.power * sin(theta)

        if self.pol[0]:
            left_v = -left_v
        if self.pol[1]:
            right_v = -right_v

        if left_v > 1.0:  # Values sometimes were outside the acceptable range [-1, 1]
            left_v = 1.0  # These lines ensure it is within the correct range.
        if right_v > 1.0:
            right_v = 1.0
        if left_v < -1.0:
            left_v = -1.0
        if right_v < -1.0:
            right_v = -1.0

        self.robot.value = (left_v, right_v)

    def stop_move(self) -> None:
        """Stop movement.

        This overwrites the base class to ensure that the motors are reset when the vehicle stops.
        """
        super().stop_move()

        self.robot.value = (0, 0)
