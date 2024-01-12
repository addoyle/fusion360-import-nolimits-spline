from ....model.support.Beam import Beam
from ....model.support.Node import Node
from ....model.support.FooterNode import FooterNode
import adsk.core
import adsk.fusion
from ....common.util import app


def generate_beam(plane: adsk.core.Plane, beam: Beam):
    root = adsk.fusion.Design.cast(app.activeProduct).activeComponent
    sweeps: adsk.fusion.SweepFeatures = root.features.sweepFeatures
    planes: adsk.fusion.ConstructionPlanes = root.constructionPlanes

    sketch: adsk.fusion.Sketch = root.sketches.add(plane)
    sketch.name = 'Beam'

    lines = sketch.sketchCurves
    linesDrawn = set()

    def recurse(beam: Beam):
        if (beam.__repr__() not in linesDrawn):
            linesDrawn.add(beam.__repr__())
            line: adsk.fusion.SketchLine = lines.sketchLines.addByTwoPoints(
                beam.start.pos, beam.end.pos)

            path = root.features.createPath(line)
            planeInput: adsk.fusion.ConstructionPlaneInput = planes.createInput()
            planeInput.setByDistanceOnPath(
                line, adsk.core.ValueInput.createByReal(0))

            pipePlane: adsk.fusion.ConstructionPlane = planes.add(planeInput)
            pipeSketch: adsk.fusion.Sketch = root.sketches.add(pipePlane)

            pipeSketch.sketchCurves.sketchCircles.addByCenterRadius(
                adsk.core.Point3D.create(0, 0, 0), beam.size1 / 2)

            circle_profile: adsk.fusion.Profile = pipeSketch.profiles.item(0)

            sweepInput: adsk.fusion.SweepFeatureInput = sweeps.createInput(
                circle_profile, path, adsk.fusion.FeatureOperations.NewBodyFeatureOperation if len(
                    linesDrawn) == 1 else adsk.fusion.FeatureOperations.JoinFeatureOperation)
            sweeps.add(sweepInput)

            for node in beam.nodes:
                while node.edges:
                    recurse(node.edges.pop())

    recurse(beam)
