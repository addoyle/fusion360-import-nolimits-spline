from __future__ import annotations
from .Component import Component
from .Node import Node
from .Util import point3d_from_string

# Free node not constrained by other structures


class FreeNode(Node, Component):
    def fromXml(xml) -> FreeNode:
        node = FreeNode()
        node.id = xml.get('id')
        node.pos = point3d_from_string(xml.find('pos').text)
        return node
