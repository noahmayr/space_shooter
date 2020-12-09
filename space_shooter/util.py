from direct.gui.OnscreenText import OnscreenText
from panda3d.core import LPoint2, TextNode, TransparencyAttrib, NodePath

from space_shooter.constants import *


def load_object(*args, **kwargs):
    return SelfLoadingNodePath(*args, **kwargs)


class SelfLoadingNodePath(NodePath):

    def __init__(self, tex=None, pos=LPoint2(0, 0), depth=SPRITE_POS, scale=1,
                 transparency=True, parent=None, model="assets/models/plane"):
        node = loader.loadModelNode(model)
        super().__init__(node)
        self.reparentTo(parent or camera.parent)

        self.setPos(pos.getX(), depth, pos.getY())
        self.setScale(0.015 * scale)

        self.setBin("fixed", 0)
        self.setDepthTest(False)

        if transparency:
            self.setTransparency(TransparencyAttrib.MAlpha)

        if tex:
            tex = loader.loadTexture(tex)
            vec = self.getScale()
            vec.x *= tex.getOrigFileXSize()
            vec.z *= tex.getOrigFileYSize()
            self.setScale(vec)
            self.setTexture(tex, 1)


def gen_label_text(text, i):
    return OnscreenText(text=text, parent=base.a2dTopLeft, pos=(0.07, -.06 * i - 0.1),
                        fg=(1, 1, 1, 1), align=TextNode.ALeft, shadow=(0, 0, 0, 0.5), scale=.05)
