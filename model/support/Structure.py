from ...common.util import log
from .Beam import Beam
from .FooterNode import FooterNode
from .RailSupportConnector import RailSupportConnector
from .FreeNode import FreeNode

# Represents a single support structure
class Structure:
    footers: FooterNode = []
    rail_support_connectors: RailSupportConnector = []
    free_nodes: FreeNode = []
    beams: Beam = []
