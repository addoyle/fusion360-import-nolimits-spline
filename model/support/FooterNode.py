from __future__ import annotations
import adsk.core
from enum import Enum
from .Component import Component
from .Node import Node
from .Colorable import Colorable
from .Util import point3d_from_string

# Node to connect a beam to the ground
class FooterNode(Node, Colorable, Component):
    # Footer shape
    class BaseType(Enum):
        SQUARE = 0
        ROUND = 1
        WOOD_SQUARE = 2
        WOOD_ROUND = 3
    # Beam-to-footer connection type
    class ConnectionType(Enum):
        SIMPLE = 0
        EXTENDED_A = 1
        EXTENDED_B = 2
    pos: adsk.core.Point3D
    rotation: float
    height_above_terrain: float
    base_type: BaseType = BaseType.SQUARE
    connection_type: ConnectionType = ConnectionType.SIMPLE

    def fromXml(xml) -> FooterNode:
        footer = FooterNode()
        footer.id = int(xml.get('id'))
        footer.pos = point3d_from_string(xml.find('pos').text)
        footer.rotation = float(xml.find('rotation').text)
        footer.height_above_terrain = float(xml.find('height_above_terrain').text)
        footer.base_type = FooterNode.BaseType(int(xml.get('basetype')))
        footer.connection_type = FooterNode.ConnectionType(int(xml.get('contype')))
        return footer