from . import Beam
import adsk.core

# A node connects beams together


class Node():
    id: str
    pos: adsk.core.Point3D
    edges: Beam = set()

    def __init__(self):
        self.edges = set()

    def __str__(self):
        return ' '.join([
            f'id={self.id}',
            f'pos={self.pos.asArray()}',
            f'edges={list(map(lambda beam: f"{beam.start.id} => {beam.end.id}", self.edges))}'
        ])

    def __repr__(self):
        return self.__str__()
