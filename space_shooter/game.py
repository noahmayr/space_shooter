from math import sin, cos
from random import choice, random

from Box2D import b2Vec2
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task
from panda3d.core import TextNode, OrthographicLens, LineSegs, NodePath, TransparencyAttrib
from pandac.PandaModules import WindowProperties

from space_shooter.background import Background
from space_shooter.constants import *
from space_shooter.entity import World, Asteroid
from space_shooter.input import InputController
from space_shooter.ship import Ship


class Game(ShowBase):

    def __init__(self):
        super().__init__()
        props = WindowProperties()
        props.setCursorHidden(True)
        self.win.requestProperties(props)
        base.setFrameRateMeter(True)

        self.bottom_text = OnscreenText(text="Distance: 0",
                                        parent=base.a2dBottomRight, scale=.07,
                                        align=TextNode.ARight, pos=(-0.1, 0.1),
                                        fg=(1, 1, 1, 1), shadow=(0, 0, 0, 0.5))

        self.setBackgroundColor((0, 0, 0, 1))
        self.background = Background()

        self.world = World()
        self.player = Ship(self.world)
        self.input = InputController(self.player)

        self.asteroids = []
        self.closest_asteroid = None
        self.spawnAsteroids()

        self.line = LineSegs()
        self.line.setThickness(15)
        self.line.setColor(1, 0.1, 0.2, 0.4)
        self.line.moveTo(0, 55, 0)
        self.line.drawTo(self.closest_asteroid.getPos() - self.player.getPos())
        self.line_node_path = NodePath(self.line.create(True))
        self.line_node_path.reparentTo(render)
        self.line_node_path.setTransparency(TransparencyAttrib.MAlpha)

        lens = OrthographicLens()
        base.cam.node().setLens(lens)

        self.input.on_window_event(self.win)
        self.gameTask = taskMgr.add(self.gameLoop, "gameLoop", sort=1)

    def gameLoop(self, task):
        dt = globalClock.getDt()

        self.spawnAsteroids()
        self.world.update(dt)
        if self.closest_asteroid:
            self.line_node_path.setPos(self.player.getPos())
            self.line.setVertex(1, self.closest_asteroid.getPos() - self.player.getPos())
        base.cam.setPosHpr(self.player.obj, 0, 0, 0, 0, 0, 0)
        base.cam.setY(-50)
        self.background.update(base.cam.getPos())
        return Task.cont

    def spawnAsteroids(self):
        if len(self.asteroids) < AST_LIMIT:
            for i in range(AST_LIMIT - len(self.asteroids)):
                pos = b2Vec2(choice(tuple(range(-SCREEN_X, -5)) + tuple(range(5, SCREEN_X))),
                             choice(tuple(range(-SCREEN_Y, -5)) + tuple(range(5, SCREEN_Y))))
                player_vel = self.player.body.linearVelocity.copy()
                player_vel.Normalize()
                pos += self.player.body.position + player_vel * 25
                angle = random() * 2 * pi
                asteroid = Asteroid(self.world, pos, angle)
                self.asteroids.append(asteroid)
                asteroid.body.linearVelocity = b2Vec2(sin(angle), cos(angle)) * AST_INIT_VEL
        new_asteroids = []
        closest = 500
        for asteroid in self.asteroids:
            length = (asteroid.body.position - self.player.body.position).length
            if length > 30:
                asteroid.kill()
            else:
                new_asteroids.append(asteroid)
            if length < closest and asteroid.alive:
                closest = length
                self.closest_asteroid = asteroid
        self.asteroids = new_asteroids
        self.bottom_text.text = "Speed: %d | Asteroids: %d | Closest: %dkm" % (
        self.player.body.linearVelocity.copy().Normalize(),
        len(self.asteroids), closest)
