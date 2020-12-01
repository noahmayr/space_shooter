#from direct.showbase.ShowBase import ShowBase
from panda3d.core import LPoint3
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode, TransparencyAttrib
from space_shooter.constants import *

def loadObject(tex=None, pos=LPoint3(0, 0), depth=SPRITE_POS, scale=1,
               transparency=True, parent=None):
    obj = loader.loadModel("assets/models/plane")
    obj.reparentTo(parent or camera.parent)

    obj.setPos(pos.getX(), depth, pos.getY())
    obj.setScale(scale)

    obj.setBin("unsorted", 0)
    obj.setDepthTest(False)

    if transparency:
        obj.setTransparency(TransparencyAttrib.MAlpha)

    if tex:
        tex = loader.loadTexture(tex)
        obj.setTexture(tex, 1)

    return obj

def genLabelText(text, i):
    return OnscreenText(text=text, parent=base.a2dTopLeft, pos=(0.07, -.06 * i - 0.1),
                        fg=(1, 1, 1, 1), align=TextNode.ALeft, shadow=(0, 0, 0, 0.5), scale=.05)
