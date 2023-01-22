from . import Beam
import adsk.core

# A node connects beams together


class Node():
    id: int
    pos: adsk.core.Point3D
    edges: Beam = []
