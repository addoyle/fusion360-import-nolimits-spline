from __future__ import annotations
from enum import Enum
from .Component import Component
from .Colorable import Colorable
from .Node import Node
from .Util import point3d_from_string

# Track-support connector


class RailSupportConnector(Colorable, Component):
    # Nodes involved in connector (typically one)
    class SubNode(Node):
        rsc: RailSupportConnector

    # Connector variant
    class ConnectorType(Enum):
        SIMPLE = 0
        TRACK_DEFAULT = 2
        TWISTED_STRAIGHT_DOWN = 256
        TWISTED_HORIZONTAL = 257
        TWISTED_VERTCAL = 258
        CORKSCREW_STRAIGHT_DOWN = 259
        _4D_HORIZONTAL = 260
        _4D_VERTICAL = 261
        _4D_ALIGNED = 262
        _4D_SPECIAL = 263
        SUSPENDED_HORIZONTAL = 264
        SUSPENDED_VERTICAL = 265

    type: ConnectorType = ConnectorType.TRACK_DEFAULT
    center_rails_coord: float
    custom_track_index: int = 0
    size: float = 0
    sub_nodes: SubNode = []

    def __init__(self):
        self.sub_nodes = []

    def fromXml(xml) -> RailSupportConnector:
        rsc = RailSupportConnector()
        rsc.type = RailSupportConnector.ConnectorType(int(xml.get('type')))
        rsc.center_rails_coord = float(xml.get('center_rails_coord'))
        rsc.custom_track_index = int(xml.get('custom_track_index'))
        rsc.size = float(xml.get('size')) if xml.get('size') else None

        def make_rsc(node):
            sub_node = RailSupportConnector.SubNode()
            sub_node.id = node.get('id')
            sub_node.pos = point3d_from_string(node.find('pos').text)
            sub_node.rsc = rsc
            return sub_node

        rsc.sub_nodes = list(map(make_rsc, xml.findall('subnode')))

        return rsc

    def __str__(self):
        return ' '.join([
            f'type={self.type.name}',
            f'center_rails_coord={self.center_rails_coord}',
            f'custom_track_intex={self.custom_track_index}',
            f'size={self.size}',
            f'sub_nodes={self.sub_nodes}'
        ])

    def __repr__(self):
        return self.__str__()
