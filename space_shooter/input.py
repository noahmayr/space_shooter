from direct.showbase.DirectObject import DirectObject

from space_shooter.constants import *
from space_shooter.ship import ShipController


class InputController(ShipController, DirectObject):

    def __init__(self, ship):
        DirectObject.__init__(self)
        ShipController.__init__(self, ship)

        self.accept(base.win.getWindowEvent(), self.on_window_event)
        self.accept("arrow_left", self.set_key, ["turnLeft", TURN_RATE])
        self.accept("arrow_left-up", self.set_key, ["turnLeft", 0])
        self.accept("arrow_right", self.set_key, ["turnRight", TURN_RATE])
        self.accept("arrow_right-up", self.set_key, ["turnRight", 0])
        self.accept("arrow_up", self.set_key, ["accel", 1])
        self.accept("arrow_up-up", self.set_key, ["accel", 0])
        self.accept("arrow_down", self.set_key, ["brake", 1])
        self.accept("arrow_down-up", self.set_key, ["brake", 0])
        self.accept("space", self.set_key, ["fire", 1])
        self.accept("space-up", self.set_key, ["fire", 0])

    def on_window_event(self, window):
        width = window.getProperties().getXSize()
        height = window.getProperties().getYSize()
        base.cam.node().getLens().setFilmSize(width / 64, height / 64)
        base.cam.node().getLens().setFocalLength(200)
