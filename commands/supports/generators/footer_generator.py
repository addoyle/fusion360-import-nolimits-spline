from ....model.support.FooterNode import FooterNode
import adsk.core
import adsk.fusion
from ....common.util import app


def generate_footer(plane: adsk.core.Plane, footer: FooterNode):
    root = adsk.fusion.Design.cast(app.activeProduct).activeComponent
    extrudes: adsk.fusion.ExtrudeFeatures = root.features.extrudeFeatures

    sketch: adsk.fusion.Sketch = root.sketches.add(plane)
    sketch.name = 'Footer'

    pts = sketch.sketchPoints
    lines = sketch.sketchCurves.sketchLines
    circles = sketch.sketchCurves.sketchCircles
    pts.add(footer.pos)

    footer_width = max((v.size1 for v in footer.edges), default=.4)
    corner: adsk.core.Point3D = footer.pos.copy()

    if footer.base_type == FooterNode.BaseType.SQUARE:
        corner.translateBy(
            adsk.core.Vector3D.create(footer_width, footer_width, 0))
        lines.addCenterPointRectangle(
            footer.pos, corner)
    elif footer.base_type == FooterNode.BaseType.ROUND:
        corner.translateBy(
            adsk.core.Vector3D.create(footer_width, 0, 0))
        circles.addByCenterRadius(footer.pos, corner)

    footer_profile: adsk.fusion.Profile = sketch.profiles.item(0)

    extrudes.addSimple(footer_profile, adsk.core.ValueInput.createByReal(-footer.height_above_terrain),
                       adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
