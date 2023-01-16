# Represents all supports
from .Beam import Beam
from .FooterNode import FooterNode
from .FreeNode import FreeNode
from .Node import Node
from .RailSupportConnector import RailSupportConnector
from .Structure import Structure

class Supports:
    nodes: Node = {}
    rail_connectors: RailSupportConnector = []

    @property
    def count(self) -> int:
        return len(self.structures)

    def clear(self):
        self.structures = {}
    
    def add_footer(self, xml):
        footer: FooterNode = FooterNode.fromXml(xml)
        self.nodes[footer.id] = footer
        
    def add_rail_support_connector(self, xml):
        rsc: RailSupportConnector = RailSupportConnector.fromXml(xml)
        self.rail_connectors.append(rsc)
        for node in rsc.sub_nodes:
            self.nodes[node.id] = node

    def add_free_node(self, xml):
        node: FreeNode  = FreeNode.fromXml(xml)
        self.nodes[node.id] = node
        
    def add_beam(self, xml):
        beam: Beam = Beam.fromXml(xml)

        start = self.nodes[beam.start]
        end = self.nodes[beam.end]
        start.edges.append(beam)
        end.edges.append(beam)
        
        for node in beam.nodes:
            # TODO calculate point
            # (x1,y1,z1) + (x2-x1,y2-y1,z2-z1) * t
            node.pos = None
            self.nodes[node.id] = node

    @property
    def structures(self):
        return []