#!/usr/bin/env python3

"""Motion class for the CamJam EduKit 3."""

from gpiozero import CamJamKitRobot

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
        pass
