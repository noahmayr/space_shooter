from space_shooter.util import loadObject
from panda3d.core import NodePath, Texture, TextureStage


class Layer:
    obj: NodePath

    def __init__(self, file, mod, depth, transparent=True):
        self.obj = loadObject(file, scale=64, depth=depth, transparency=transparent)
        self.obj.setBin("background", 100 - depth)
        tex = self.obj.get_texture()
        tex.setWrapU(Texture.WM_repeat)
        tex.setWrapV(Texture.WM_repeat)
        self.mod = mod

    def update(self, pos):
        self.obj.setPos(pos.x, self.obj.getY(), pos.z)
        self.obj.set_tex_offset(TextureStage.getDefault(),
                                pos.x * self.mod,
                                pos.z * self.mod)


class Background:

    def __init__(self):
        self.layers = []
        self.layers.append(Layer("assets/img/background/bg_nebula_1.png", 0.002, 100, False))
        self.layers.append(Layer("assets/img/background/stars_small_1.png", 0.003, 99))
        self.layers.append(Layer("assets/img/background/stars_small_2.png", 0.004, 98))
        self.layers.append(Layer("assets/img/background/stars_big_1.png", 0.005, 97))
        self.layers.append(Layer("assets/img/background/stars_big_2.png", 0.006, 96))

    def update(self, pos):
        for layer in self.layers:
            layer.update(pos)
