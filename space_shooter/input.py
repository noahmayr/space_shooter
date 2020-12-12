from direct.showbase.DirectObject import DirectObject

from space_shooter.constants import *
from space_shooter.ship import ShipController

KEYMAP = {
    "accel": ["arrow_up", "w"],
    "turnLeft": ["arrow_left", "a"],
    "brake": ["arrow_down", "s"],
    "turnRight": ["arrow_right", "d"],
    "strafeLeft": ["q"],
    "strafeRight": ["e"],
    "fire": ["space"],
}


class InputController(ShipController, DirectObject):

    def __init__(self, ship):
        DirectObject.__init__(self)
        ShipController.__init__(self, ship)

        self.accept(base.win.getWindowEvent(), self.on_window_event)
        for action, keys in KEYMAP.items():
            for key in keys:
                self.accept("%s" % key, self.set_key, [action, 1])
                self.accept("%s-up" % key, self.set_key, [action, 0])

    def on_window_event(self, window):
        width = window.getProperties().getXSize()
        height = window.getProperties().getYSize()
        base.cam.node().getLens().setFilmSize(width / 64, height / 64)
        base.cam.node().getLens().setFocalLength(200)
