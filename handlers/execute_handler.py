from array import array
import adsk.core, adsk.fusion
from ..common.util import app, ui, spline

def execute_handler(args: adsk.core.CommandEventArgs):
    global app, ui, spline

    root = adsk.fusion.Design.cast(app.activeProduct).rootComponent

    inputs = args.command.commandInputs

    show_left_spline: adsk.core.BoolValueCommandInput = inputs.itemById('leftSpline')
    show_right_spline: adsk.core.BoolValueCommandInput = inputs.itemById('rightSpline')
    plane_selection_input: adsk.core.SelectionCommandInput = inputs.itemById('plane')

    limit_input: adsk.core.IntegerSpinnerCommandInput = inputs.itemById('limit')
    offset_input: adsk.core.IntegerSpinnerCommandInput = inputs.itemById('offset')
    
    if plane_selection_input.selectionCount:
        sketch: adsk.fusion.Sketch = root.sketches.add(plane_selection_input.selection(0).entity)
        sketch.name = 'Track Reference'

        if spline.center.count:
            center_points = adsk.core.ObjectCollection.create()
            for pt in points_in_range(spline.center, limit_input.value, offset_input.value):
                center_points.add(pt)

            sketch.sketchCurves.sketchFittedSplines.add(center_points)

        if (spline.left.count and show_left_spline.value):
            left_points = adsk.core.ObjectCollection.create()
            for pt in points_in_range(spline.left, limit_input.value, offset_input.value):
                left_points.add(pt)

            sketch.sketchCurves.sketchFittedSplines.add(left_points)
            
        if (spline.right.count and show_right_spline.value):
            right_points = adsk.core.ObjectCollection.create()
            for pt in points_in_range(spline.right, limit_input.value, offset_input.value):
                right_points.add(pt)

            sketch.sketchCurves.sketchFittedSplines.add(right_points)

def points_in_range(pts: array, limit: int, offset: int):
    if (limit == 0):
        return pts[offset:]
    else:
        return pts[offset:offset + limit]
