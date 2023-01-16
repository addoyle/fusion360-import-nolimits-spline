import os, adsk.core, adsk.fusion

# from .destroyed_handler import destroy_handler
# from .execute_handler import execute_handler
# from .input_changed_handler import input_changed_handler
from .open_xml_handler import activated_handler, browse_btn_handler
# from .validate_input_handler import validate_input_handler
from ....common.util import app, add_handler, handle_error, command_inputs

RESOURCES = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../resources', ''))

def create_handler(args: adsk.core.CommandCreatedEventArgs):
    try:
        design = adsk.fusion.Design.cast(app.activeProduct)

        # add_handler(args.command.execute, execute_handler)
        # add_handler(args.command.destroy, destroy_handler)
        add_handler(args.command.incomingFromHTML, browse_btn_handler)
        # add_handler(args.command.validateInputs, validate_input_handler)
        add_handler(args.command.activate, activated_handler)
        # add_handler(args.command.inputChanged, input_changed_handler)

        inputs = args.command.commandInputs
        
        # Open file button
        inputs.addBrowserCommandInput('supportsXmlBtn', 'Supports Data', 'common/resources/browse.html', 28, 28)

        # Construction pane selection
        construction_plane_input = inputs.addSelectionInput('plane', 'Construction Plane', 'Select a Construction Plane')
        construction_plane_input.addSelectionFilter(adsk.core.SelectionCommandInput.ConstructionPlanes)
        construction_plane_input.addSelection(design.rootComponent.xYConstructionPlane)
        command_inputs['plane'] = construction_plane_input
        
    except:
        handle_error('create')