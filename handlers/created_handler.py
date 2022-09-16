import adsk.core, adsk.fusion

from .browse_btn_handler import browse_btn_handler
from .destroyed_handler import destroy_handler
from .execute_handler import execute_handler
from .validate_input_handler import validate_input_handler
from ..common.util import app, add_handler, handle_error

def create_handler(args: adsk.core.CommandCreatedEventArgs):
    try:
        global app
        design = adsk.fusion.Design.cast(app.activeProduct)

        add_handler(args.command.execute, execute_handler)
        add_handler(args.command.destroy, destroy_handler)
        add_handler(args.command.incomingFromHTML, browse_btn_handler)
        add_handler(args.command.validateInputs, validate_input_handler)

        inputs = args.command.commandInputs
        
        inputs.addBrowserCommandInput('splineDataBtn', 'Spline Data', 'resources/browse.html', 28)

        inputs.addBoolValueInput('centerSpline', 'Center Spline', True, '', True)
        inputs.addBoolValueInput('leftSpline', 'Left Spline', True, '', True)
        inputs.addBoolValueInput('rightSpline', 'Right Spline', True, '', True)

        construction_plane_input = inputs.addSelectionInput('plane', 'Construction Plane', 'Select a Construction Plane')
        construction_plane_input.addSelectionFilter('ConstructionPlanes')
        construction_plane_input.addSelection(design.rootComponent.xZConstructionPlane)

        limit_input = inputs.addIntegerSpinnerCommandInput('limit', 'Points to Sketch', 0, 1000000, 1, 16)
        limit_input.tooltip = 'Number of points to sketch (0 for all points)'

        offset_input = inputs.addIntegerSpinnerCommandInput('offset', 'Point Start', 0, 1000000, 1, 0)
        offset_input.tooltip = 'Point index to start sketching from (0 for beginning)'
    except:
        handle_error('create')

def activate_plane_handler(args: adsk.core.CommandEventArgs):
    try:
        global app
        design = adsk.fusion.Design.cast(app.activeProduct)
        
    except:
        handle_error('create')