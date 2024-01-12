from ....model.support.RailSupportConnector import RailSupportConnector
import adsk.core
import adsk.fusion
from ....common.util import app


def generate_rasc(plane: adsk.core.Plane, rasc: RailSupportConnector):
    root = adsk.fusion.Design.cast(app.activeProduct).activeComponent
    extrudes: adsk.fusion.ExtrudeFeatures = root.features.extrudeFeatures

    sketch: adsk.fusion.Sketch = root.sketches.add(plane)
    sketch.name = 'Rail Support Connectors'

    pts = sketch.sketchPoints
    for sub_node in rasc.sub_nodes:
        sub_node: RailSupportConnector.SubNode = sub_node
        pts.add(sub_node.pos)
