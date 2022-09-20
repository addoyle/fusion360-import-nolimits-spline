import os, adsk.core, adsk.fusion

from .destroyed_handler import destroy_handler
from .execute_handler import execute_handler
from .input_changed_handler import input_changed_handler
from .open_csv_handler import activated_handler, browse_btn_handler
from .validate_input_handler import validate_input_handler
from ..common.util import app, add_handler, handle_error, command_inputs

RESOURCES = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../resources', ''))

def create_handler(args: adsk.core.CommandCreatedEventArgs):
    try:
        design = adsk.fusion.Design.cast(app.activeProduct)

        add_handler(args.command.execute, execute_handler)
        add_handler(args.command.destroy, destroy_handler)
        add_handler(args.command.incomingFromHTML, browse_btn_handler)
        add_handler(args.command.validateInputs, validate_input_handler)
        add_handler(args.command.activate, activated_handler)
        add_handler(args.command.inputChanged, input_changed_handler)

        inputs = args.command.commandInputs
        
        # Open file button
        inputs.addBrowserCommandInput('splineDataBtn', 'Spline Data', 'resources/browse.html', 28)

        # Spline rail chooser
        railRow = inputs.addButtonRowCommandInput('railSplines', 'Rail Splines', True)
        command_inputs['leftSpline'] = railRow.listItems.add('Left Spline', True, os.path.join(RESOURCES, 'rails', 'left'))
        command_inputs['centerSpline'] = railRow.listItems.add('Center Spline', True, os.path.join(RESOURCES, 'rails', 'center'))
        command_inputs['rightSpline'] = railRow.listItems.add('Right Spline', True, os.path.join(RESOURCES, 'rails', 'right'))

        # Construction pane selection
        construction_plane_input = inputs.addSelectionInput('plane', 'Construction Plane', 'Select a Construction Plane')
        construction_plane_input.addSelectionFilter(adsk.core.SelectionCommandInput.ConstructionPlanes)
        construction_plane_input.addSelection(design.rootComponent.xYConstructionPlane)
        command_inputs['plane'] = construction_plane_input

        # Start point
        start_point_input = inputs.addIntegerSpinnerCommandInput('startPoint', 'Start Point', 0, 1000000, 1, 0)
        start_point_input.tooltip = 'Start point to draw (0 for beginning)'
        command_inputs['startPoint'] = start_point_input

        # End point
        end_point_input = inputs.addIntegerSpinnerCommandInput('endPoint', 'End Point', -1, 1000000, 1, -1)
        end_point_input.tooltip = 'End point to draw (0 for beginning, -1 for end)'
        command_inputs['endPoint'] = end_point_input

        # Num points
        num_points_input = inputs.addIntegerSpinnerCommandInput('numPoints', 'Points to Sketch', 1, 1000000, 1, 1)
        num_points_input.tooltip = 'Points to Draw'
        command_inputs['numPoints'] = num_points_input
        
    except:
        handle_error('create')