from array import array
import adsk.core, adsk.fusion
from ..common.util import app, ui, spline

def execute_handler(args: adsk.core.CommandEventArgs):
    root = adsk.fusion.Design.cast(app.activeProduct).rootComponent

    inputs = args.command.commandInputs

    spline_chooser: adsk.core.ButtonRowCommandInput = inputs.itemById('railSplines')
    show_left_spline = spline_chooser.listItems.item(0).isSelected
    show_center_spline = spline_chooser.listItems.item(1).isSelected
    show_right_spline = spline_chooser.listItems.item(2).isSelected
    plane_selection_input = inputs.itemById('plane')

    start_point_input: adsk.core.IntegerSpinnerCommandInput = inputs.itemById('startPoint')
    end_point_input: adsk.core.IntegerSpinnerCommandInput = inputs.itemById('endPoint')
    
    if plane_selection_input.selectionCount:
        sketch: adsk.fusion.Sketch = root.sketches.add(plane_selection_input.selection(0).entity)
        sketch.name = 'Track Reference'

        if spline.count:
            if show_center_spline:
                center_points = adsk.core.ObjectCollection.create()
                for pt in points_in_range(spline.center, start_point_input.value, end_point_input.value):
                    center_points.add(pt)

                sketch.sketchCurves.sketchFittedSplines.add(center_points)

            if show_left_spline:
                left_points = adsk.core.ObjectCollection.create()
                for pt in points_in_range(spline.left, start_point_input.value, end_point_input.value):
                    left_points.add(pt)

                sketch.sketchCurves.sketchFittedSplines.add(left_points)
                
            if show_right_spline:
                right_points = adsk.core.ObjectCollection.create()
                for pt in points_in_range(spline.right, start_point_input.value, end_point_input.value):
                    right_points.add(pt)

                sketch.sketchCurves.sketchFittedSplines.add(right_points)

def points_in_range(pts: array, start: int, end: int):
    return pts[start - 1:end]
