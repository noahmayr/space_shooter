from direct.gui.OnscreenText import OnscreenText
from panda3d.core import LPoint2, TextNode, TransparencyAttrib

from space_shooter.constants import *


def load_object(tex=None, pos=LPoint2(0, 0), depth=SPRITE_POS, scale=1,
                transparency=True, parent=None):
    obj = loader.loadModel("assets/models/plane")
    obj.reparentTo(parent or camera.parent)

    obj.setPos(pos.getX(), depth, pos.getY())
    obj.setScale(0.015 * scale)

    obj.setBin("unsorted", 0)
    obj.setDepthTest(False)

    if transparency:
        obj.setTransparency(TransparencyAttrib.MAlpha)

    if tex:
        tex = loader.loadTexture(tex)
        vec = obj.getScale()
        vec.x *= tex.getOrigFileXSize()
        vec.z *= tex.getOrigFileYSize()
        obj.setScale(vec)
        obj.setTexture(tex, 1)

    return obj


def gen_label_text(text, i):
    return OnscreenText(text=text, parent=base.a2dTopLeft, pos=(0.07, -.06 * i - 0.1),
                        fg=(1, 1, 1, 1), align=TextNode.ALeft, shadow=(0, 0, 0, 0.5), scale=.05)
