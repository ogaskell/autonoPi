#!/usr/bin/env python3

"""Management system module."""


from .cv import LineDetector
from .hardware.motion import Motion
from .navigation import Navigation


class Manager:
    """Management system base class. This will also include base classes for any components.

    In order to implement autonoPi, create a class which inherits from this class.
    """

    def __init__(self):
        self.setup_components()

    def setup_components(self) -> None:
        """Setup components required by the system.

        This only uses the base classes for most systems so should be overwritten in an implmentation.
        """
        self.line_detector = LineDetector()
        self.motion = Motion()
        self.navigation = Navigation()

    def mainloop(self) -> None:
        """Main event loop of the program.

        Will simply run self.run continuously.
        """
        while True:
            self.run()

    def run(self) -> None:
        """The main event loop code goes here.

        Note that this function should run and return, since the loop is done elsewhere.
        """
        raise NotImplementedError("Manager() is the base management class, and subclasses must overwrite run().")
