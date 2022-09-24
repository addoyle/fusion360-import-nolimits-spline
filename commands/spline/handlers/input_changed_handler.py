import adsk.core, adsk.fusion
from ....common.util import spline

def input_changed_handler(args: adsk.core.InputChangedEventArgs):
    start_point_input: adsk.core.IntegerSpinnerCommandInput = args.inputs.itemById('startPoint')
    end_point_input: adsk.core.IntegerSpinnerCommandInput = args.inputs.itemById('endPoint')
    num_points_input: adsk.core.IntegerSpinnerCommandInput = args.inputs.itemById('numPoints')
    plane_input: adsk.core.SelectionCommandInput = args.inputs.itemById('plane')

    # Update numPoints based on start/end point
    if args.input.id == 'startPoint' or args.input.id == 'endPoint':
        start_point_input.value = min(start_point_input.value, spline.count)
        end_point_input.value = min(end_point_input.value, spline.count)
        num_points_input.value = end_point_input.value - start_point_input.value + 1
    
    # Update endPoint based on start/numPoints
    if args.input.id == 'numPoints':
        num_points_input.value = min(num_points_input.value, spline.count - start_point_input.value + 1)
        end_point_input.value = start_point_input.value + num_points_input.value - 1
