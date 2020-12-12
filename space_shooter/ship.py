from math import sin, cos
import random

import Box2D as b2D
from panda3d.core import LPoint2

from space_shooter.constants import *
from space_shooter.entity import Entity, Bullet
from space_shooter.util import SelfLoadingNodePath


class ShipController:

    def __init__(self, ship):
        self.ship = ship
        ship.controller = self
        self.keys = {"turnLeft": 0, "turnRight": 0,
                     "accel": 0, "fire": 0, "brake": 0, "strafeLeft": 0, "strafeRight": 0}

    def set_key(self, key, val):
        self.keys[key] = val

    def update(self, dt):

        spin = self.ship.body.angularVelocity
        turn = (self.keys["turnRight"] - self.keys["turnLeft"]) * TURN_RATE
        if turn != 0:
            dif = turn - spin
            spin += dif * dt
            self.ship.body.angularVelocity = min(TURN_RATE, max(-TURN_RATE, spin))

        vel = self.ship.body.linearVelocity
        heading_rad = DEG_TO_RAD * self.ship.getR()
        heading_vec: b2D.b2Vec2 = b2D.b2Vec2(sin(heading_rad), cos(heading_rad))
        if self.keys["strafeLeft"]:
            self.ship.body.ApplyForceToCenter(b2D.b2Vec2(-heading_vec.y, heading_vec.x) * ACCELERATION, True)
        if self.keys["strafeRight"]:
            self.ship.body.ApplyForceToCenter(b2D.b2Vec2(heading_vec.y, -heading_vec.x) * ACCELERATION, True)

        if self.keys["accel"]:
            self.ship.body.ApplyForceToCenter(b2D.b2Vec2(sin(heading_rad), cos(heading_rad)) * ACCELERATION, True)

        self.ship.thruster.thrust(self.keys["accel"], dt)
        self.ship.thruster_right.thrust(self.keys["turnRight"], dt)
        self.ship.thruster_left.thrust(self.keys["turnLeft"], dt)
        self.ship.thruster_right_strafe.thrust(self.keys["strafeRight"], dt)
        self.ship.thruster_left_strafe.thrust(self.keys["strafeLeft"], dt)

        self.ship.body.linearDamping = 1.5 if self.keys["brake"] else 0.5
        self.ship.body.angularDamping = 1.5 if self.keys["turnRight"] and self.keys["turnLeft"] else 0.5

        if self.keys["fire"]:
            self.ship.fire()


class Ship(Entity):
    controller: ShipController

    def __init__(self, world):
        super().__init__(world, "assets/img/playerShip2_red.png")
        self.body.angularDamping = 0.5
        self.nextBullet = 0.0
        self.fireRate = 10
        self.thruster = Thruster(self, LPoint2(0, -.6))
        self.thruster_left_strafe = Thruster(self, LPoint2(.8, -.175), -70)
        self.thruster_right_strafe = Thruster(self, LPoint2(-.8, -.175), 70)
        self.thruster_left = Thruster(self, LPoint2(.4, -.5), 20)
        self.thruster_right = Thruster(self, LPoint2(-.4, -.5), -20)
        self.thruster_left.exhaust_scale.z /= 3
        self.thruster_right.exhaust_scale.z /= 3

    def update(self, dt):
        super().update(dt)
        if self.controller:
            self.controller.update(dt)

    def fire(self, deviation=5):
        if globalClock.long_time >= self.nextBullet:
            self.nextBullet = globalClock.long_time + 1 / self.fireRate
            angle = self.body.angle + random.uniform(-1, 1) * deviation
            direction = DEG_TO_RAD * angle
            vel = (self.body.linearVelocity + (b2D.b2Vec2(sin(direction), cos(direction)) * BULLET_SPEED))
            bullet = Bullet(self.world, self, position=self.body.position, angle=angle)
            bullet.body.linearVelocity = vel


class Thruster(SelfLoadingNodePath):

    def __init__(self, parent, pos, angle=0, tex="down_blue02.png"):
        super().__init__("assets/img/effects/fire/%s" % tex, pos=pos,
                         parent=parent,
                         model="assets/models/plane_top_pivot.egg")
        self.setBin("fixed", -1)
        self.exhaust_scale = self.getScale()
        self.setR(angle)
        self.thrust_time = 0

    def thrust(self, enabled, dt):
        thrust = 0
        if enabled:
            self.thrust_time = min(self.thrust_time + dt, 1)
            thrust = 1 - 1 / (pow(3 * self.thrust_time + .1, 3) + 1)
            self.show()
        else:
            self.thrust_time = 0
            self.hide()
        self.setScale(self.exhaust_scale.x, self.exhaust_scale.y, self.exhaust_scale.z * thrust)
