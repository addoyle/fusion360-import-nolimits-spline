from ...common.util import log
from .Beam import Beam
from .FooterNode import FooterNode
from .RailSupportConnector import RailSupportConnector
from .FreeNode import FreeNode
from .Node import Node

# Represents a single support structure


class Structure:
    footers: FooterNode = []
    rail_support_connectors: RailSupportConnector = set()
    free_nodes: FreeNode = []
    beams: Beam = set()
    nodes: Node = {}

    def __init__(self, head: Node):
        self.footers = []
        self.rail_support_connectors = set()
        self.free_nodes = []
        self.beams = set()
        self.nodes = {}

        def add_node(node: Node):
            if (node.id in self.nodes):
                return

            self.nodes[node.id] = node

            if isinstance(node, FooterNode):
                self.footers.append(node)
            if isinstance(node, FreeNode):
                self.free_nodes.append(node)
            if (isinstance(node, RailSupportConnector.SubNode)):
                self.rail_support_connectors.add(node.rsc)

            for beam in node.edges:
                beam: Beam = beam
                self.beams.add(beam)

                add_node(beam.start)
                add_node(beam.end)
                for beam_node in beam.nodes:
                    add_node(beam_node)

        add_node(head)

    def __str__(self):
        sep = '    \n'
        return '\n'.join([
            'footers=[{}{}\n]'.format(sep,
                                      sep.join(str(v) for v in self.footers)),
            'rail_support_connectors=[{}{}\n]'.format(sep,
                                                      sep.join(str(v) for v in self.rail_support_connectors)),
            'free_nodes=[{}{}\n]'.format(sep,
                                         sep.join(str(v) for v in self.free_nodes)),
            'beams=[{}{}\n]'.format(sep,
                                    sep.join(str(v) for v in self.beams))
        ])
