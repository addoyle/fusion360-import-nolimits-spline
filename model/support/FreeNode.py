from __future__ import annotations
import adsk.core
from .Component import Component
from .Node import Node
from .Util import point3d_from_string

# Free node not constrained by other structures


class FreeNode(Node, Component):
    pos: adsk.core.Point3D

    def fromXml(xml) -> FreeNode:
        node = FreeNode()
        node.id = int(xml.get('id'))
        node.pos = point3d_from_string(xml.find('pos').text)
        return node
