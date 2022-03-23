#!/usr/bin/env python3

"""Motion hardware interfaces.

This file will include classes for available hardware interfaces for motion devices, eg motors.
"""

import threading as thr


class Motion:
    """Base motion interface class."""

    reverse = False  # Does this interface support reverse?

    def __init__(self):
        ## Current movement parameters
        # Are we currently moving?
        self.inmotion = False
        # Power as a fraction (0.0 - 1.0) of the max power. Note if reverse is true, this can be negative
        self.power = 0
        # Direction as a signed fraction (-1.0 - 1.0) of the smallest turn radius
        self.direction = 0

        # Movement thread
        # Defined as a daemon since it is simply providing functionality to the main program
        # Nothing critical happens in this thread so it is completely safe to make it a daemon
        self.movement_thread = thr.Thread(target=self.movement, daemon=True)
        self.movement_thread.start()

    def start_move(self) -> None:
        """Begin movement.

        Move according to self.power and self.direction.
        If the thread isn't running, start it. Otherwise, just set self.inmotion.
        """
        if not self.movement_thread.is_alive():
            raise Exception("Motion Thread Died")

        self.inmotion = True

    def stop_move(self) -> None:
        """Stop movement.

        When this is called, until start_move is called self.power and self.direction are ignored.
        Since it is not simple to just kill the movement thread, this function simply sets self.inmotion, so the thread
         will stop the car when this is false, and the thread will exit.
        """
        self.inmotion = False

    def movement(self) -> None:
        """Movement thread function

        This function will be run in a thread in order to allow for constant updates to how the car is moved in the
         main thread, and they can be applied without blocking execution. It will simply call self.move, while inmotion
         is true.
        """
        while True:
            if self.inmotion:
                self.move()

    def move(self) -> None:
        """Move the device.

        This function will be run by self.movement, continually while inmotion is true. This thread will simply move
         the car once, or update how it is moving, before exiting.
        """
        raise NotImplementedError("Motion base class is not associated with any hardware. Cannot Stop Movement.")
