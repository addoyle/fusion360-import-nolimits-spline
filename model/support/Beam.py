from __future__ import annotations
import adsk.core
from enum import Enum
from .Colorable import Colorable
from .Component import Component
from .Node import Node

# Beam which connects two nodes


class Beam(Colorable, Component):
    # Node constrained to a beam
    class BeamNode(Node):
        # Node type, includes decorative types (e.g. Flange)
        class BeamNodeType(Enum):
            NODE = 0
            FLANGE = 1
            SMALL_NUTS = 2
            MEDIUM_NUTS = 3
            LEDGER_NUTS = 4
            LEDGER_NUTS_SPECIAL = 5
            LEDGER_BOLTS = 6

        pos: adsk.core.Point3D
        time: float
        type: BeamNodeType = BeamNodeType.NODE
    # Beam type

    class BeamType(Enum):
        PIPE = 1
        LOOP_BOX_BEAM = 2
        L_BEAM = 3
        I_BEAM = 4
        BOX_BEAM = 5
        WOOD_BEAM = 6
        WOOD_CATWALK = 7
        C_BEAM = 8
        CABLE = 9

    start: Node
    end: Node
    nodes: BeamNode = []

    type: BeamType = BeamType.PIPE
    rotation: float = 0
    start_extra_length: float = 0
    end_extra_length: float = 0
    offset_rel_x: float = 0
    offset_rel_y1: float = 0
    offset_rel_y2: float = 0
    vertical: bool = False
    open_start_cap: bool = False
    open_end_cap: bool = False
    display_bolts: bool = False
    size1: float = 0
    size2: float = 0

    # Ignored fields, only specified for completeness
    open_caps_for_lods: bool = False
    lod: str = ''
    dim_tunnel: bool = False

    def fromXml(xml) -> Beam:
        beam = Beam()
        beam.start = int(xml.get('start'))
        beam.end = int(xml.get('end'))
        beam.type = Beam.BeamType(int(xml.get('type')))
        beam.size1 = float(xml.get('size1'))
        beam.size2 = float(xml.get('size2')) if xml.get('size2') else None

        # TODO add other props

        def make_beam_node(node):
            beamnode = Beam.BeamNode()
            beamnode.id = int(node.get('id'))
            beamnode.time = float(node.get('pos'))
            beamnode.type = Beam.BeamNode.BeamNodeType(int(node.get('type')))
            beamnode.edges = [beam]
            return beamnode

        beam.nodes = map(make_beam_node, xml.findall('beamnode'))

        return beam
