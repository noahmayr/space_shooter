from direct.showbase import DirectObject
from direct.task.Task import Task
from math import sin, cos
import space_shooter.entity
from space_shooter.constants import *
from Box2D import b2Vec2


class Input(DirectObject.DirectObject):

    def __init__(self, entity: space_shooter.entity.Entity):
        super().__init__()
        self.entity = entity

        self.keys = {"turnLeft": 0, "turnRight": 0,
                     "accel": 0, "fire": 0, "brake": 0}

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

    def update(self, task):

        dt = globalClock.getDt()
        spin = self.entity.body.angularVelocity
        turn = (self.keys["turnRight"] - self.keys["turnLeft"])
        if turn != 0:
            dif = turn - spin
            spin += dif * dt
            self.entity.body.angularVelocity = min(TURN_RATE, max(-TURN_RATE, spin))

        if self.keys["accel"]:
            vel = self.entity.body.linearVelocity
            heading_rad = DEG_TO_RAD * self.entity.obj.getR()
            vel += b2Vec2(sin(heading_rad), cos(heading_rad)) * ACCELERATION * dt
            if vel.lengthSquared > MAX_VEL_SQ:
                vel.Normalize()
                vel *= MAX_VEL
            self.entity.body.linearVelocity = vel

        if self.keys["brake"]:
            self.entity.body.linearDamping = 1
        else:
            self.entity.body.linearDamping = 0


        if self.keys["fire"]:
            self.entity.fire()
        return Task.cont

    def set_key(self, key, val):
        self.keys[key] = val

    def on_window_event(self, window):
        width = window.getProperties().getXSize()
        height = window.getProperties().getYSize()
        base.cam.node().getLens().setFilmSize(width / 64, height / 64)
        base.cam.node().getLens().setFocalLength(200)
