import adsk.core
from .Beam import Beam
from .FooterNode import FooterNode
from .FreeNode import FreeNode
from .Node import Node
from .RailSupportConnector import RailSupportConnector
from .Structure import Structure
from ...common.util import log


class Supports:
    nodes: Node = {}
    _structs: Node = []

    def __init__(self):
        self.nodes = {}
        self.rail_connectors = []
        self._structs = []

    @property
    def count(self) -> int:
        return len(self.structures)

    def clear(self):
        self._structs = []

    def add_footer(self, xml):
        self.clear()
        footer: FooterNode = FooterNode.fromXml(xml)
        self.nodes[footer.id] = footer

    def add_rail_support_connector(self, xml):
        self.clear()
        rsc: RailSupportConnector = RailSupportConnector.fromXml(xml)
        for node in rsc.sub_nodes:
            node: RailSupportConnector.SubNode
            self.nodes[node.id] = node

    def add_free_node(self, xml):
        self.clear()
        node: FreeNode = FreeNode.fromXml(xml)
        self.nodes[node.id] = node

    def add_beam(self, xml):
        self.clear()
        beam: Beam = Beam.fromXml(xml)

        # Set start/end
        beam.start: Node = self.nodes[beam._start]
        beam.end: Node = self.nodes[beam._end]

        # Add new beam to start/end's edges
        beam.start.edges.add(beam)
        beam.end.edges.add(beam)

        for node in beam.nodes:
            node: Beam.BeamNode = node

            # (x1,y1,z1) + (x2-x1,y2-y1,z2-z1) * t
            node.pos = adsk.core.Point3D.create(
                beam.start.pos.x + (beam.end.pos.x -
                                    beam.start.pos.x) * node.time,
                beam.start.pos.y + (beam.end.pos.y -
                                    beam.start.pos.y) * node.time,
                beam.start.pos.z + (beam.end.pos.z -
                                    beam.start.pos.z) * node.time
            )
            self.nodes[node.id] = node

    @property
    def structures(self):
        if not bool(self.nodes):
            return []

        if self._structs:
            return self._structs

        ungrouped = self.nodes.copy()

        def remove_connected(node: Node):
            if node == None or node.id not in ungrouped:
                return

            ungrouped.pop(node.id)

            for beam in node.edges:
                beam: Beam = beam
                remove_connected(beam.start)
                remove_connected(beam.end)
                for beamnode in beam.nodes:
                    remove_connected(beamnode)

        heads: Node = []
        while ungrouped:
            # First node in struct is considered the "head"
            head = list(ungrouped.values())[0]
            heads.append(head)

            # Remove connected nodes
            remove_connected(head)

        self._structs = list(map(lambda head: Structure(head), heads))

        return self._structs
