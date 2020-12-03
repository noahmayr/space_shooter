from math import sin, cos
from random import randint

import Box2D as b2D
from panda3d.core import LPoint3, NodePath

from space_shooter.constants import *
from space_shooter.util import load_object


class ContactListener(b2D.b2ContactListener):
    def __init__(self):
        super().__init__()

    def BeginContact(self, contact):
        a = contact.fixtureA.userData
        b = contact.fixtureB.userData
        if (isinstance(a, Bullet) and not a.shooter == b) or (isinstance(b, Bullet) and not b.shooter == a):
            b.kill()
            a.kill()

    def EndContact(self, contact):
        pass

    def PreSolve(self, contact, oldManifold):
        a = contact.fixtureA.userData
        b = contact.fixtureB.userData
        if (isinstance(a, Bullet) and a.shooter == b) or (isinstance(b, Bullet) and b.shooter == a):
            contact.enabled = False

    def PostSolve(self, contact, impulse):
        pass


class World:

    def __init__(self):
        self.entities = []
        self.dead = []
        self.contactListener = ContactListener()
        self.physics = b2D.b2World(gravity=(0, -0), doSleep=True, contactListener=self.contactListener)
        pass

    def update(self, dt):
        self.delete(*self.dead)
        self.dead.clear()
        for entity in self.entities:
            entity.update(dt)
        self.physics.Step(dt, 10, 10)

    def delete(self, *entities):
        for entity in entities:
            if entity in self.entities:
                self.entities.remove(entity)
                self.physics.DestroyBody(entity.body)
                entity.obj.removeNode()


class Entity:
    body: b2D.b2Body
    obj: NodePath
    alive = True

    def __init__(self, world: World, file, bodyDef: dict = {}, *args, **kwargs):
        self.world = world
        self.body = world.physics.CreateBody(**({"type": b2D.b2_dynamicBody, "userData": self} | bodyDef))
        self.obj = load_object(file, *args, **kwargs)
        self.box = self.body.CreateCircleFixture(radius=0.5 * self.obj.get_scale().x, userData=self, density=1,
                                                 friction=0.3)
        world.entities.append(self)

    def update(self, dt):
        pos = self.body.position
        self.obj.setPos(pos.x, SPRITE_POS, pos.y)
        self.obj.setR(self.body.angle)

    def kill(self):
        self.alive = False
        self.world.dead.append(self)

    def on_destruction(self):
        pass


class Player(Entity):

    def __init__(self, world):
        super().__init__(world, "assets/img/playerShip2_red.png")
        self.body.angularDamping = 0.5
        self.nextBullet = 0.0
        self.fireRate = 10

    def fire(self):
        if globalClock.long_time >= self.nextBullet:
            self.nextBullet = globalClock.long_time + 1 / self.fireRate
            direction = DEG_TO_RAD * self.body.angle
            vel = (self.body.linearVelocity + (b2D.b2Vec2(sin(direction), cos(direction)) * BULLET_SPEED))
            bullet = Bullet(self.world, self, position=self.body.position, angle=self.body.angle)
            bullet.body.linearVelocity = vel


class Bullet(Entity):

    def __init__(self, world, shooter, *args, position: b2D.b2Vec2 = b2D.b2Vec2(0, 0), angle: float = 0):
        self.expires = globalClock.long_time + BULLET_LIFE
        self.shooter = shooter
        super().__init__(world, "assets/img/Lasers/laserRed01.png",
                         {"position": position, "angle": angle, "bullet": True}, scale=.2)

    def update(self, dt):
        super().update(dt)
        if self.expires < globalClock.long_time:
            self.kill()


class Asteroid(Entity):

    def __init__(self, world, position: b2D.b2Vec2, angle: float = 0, scale=AST_INIT_SCALE):
        super().__init__(world, "assets/img/Meteors/meteorGrey_big%d.png" % randint(1, 3),
                         {"position": position, "angle": angle}, scale=scale)
