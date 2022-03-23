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
        self.setup_variables()

    def setup_components(self) -> None:
        """Setup components required by the system.

        This only uses the base classes for most systems so should be overwritten in an implmentation.
        """
        self.line_detector = LineDetector()
        self.motion = Motion()
        self.navigation = Navigation()

    def setup_variables(self) -> None:
        """Setup variables required by the system.

        This base class doesn't require any variables so this function is blank. It is still required however, so that
         it can be included in __init__ without potentially causing undefined errors. This also means any classes which
         don't need variables needn't worry about creating this function.
        """
        pass

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
