from pygaze import libscreen
from pygaze import eyetracker

class EyeData:
    def __init__(self):
        """Initialize the display and eye tracker."""
        self.disp = libscreen.Display()
        self.tracker = eyetracker.EyeTracker(self.disp)
        self.tracker.calibrate()

    def start(self):
        """Start recording eye tracking data."""
        self.tracker.start_recording()

    def stop(self):
        """Stop recording and clean up resources."""
        self.tracker.stop_recording()
        self.tracker.close()
        self.disp.close()

    def getCoordinates(self):
        """Get the current eye gaze coordinates as a tuple (x, y)."""
        sample = self.tracker.sample()
        if sample is not None:
            return sample[0], sample[1]
        return None, None