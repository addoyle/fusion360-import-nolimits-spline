#Author-Andy Doyle
#Description-Imports spline data exported from NoLimits

import adsk.core, adsk.fusion, adsk.cam, traceback, os

from .handlers.created_handler import create_handler
from .common.util import add_handler, app, handle_error, ui, handlers

ID = 'ImportNLSplineCMDDef'
TOOLBAR_PANEL = 'SolidScriptsAddinsPanel'

def run(context):
    global app, ui, handlers

    try:
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        if not design:
            ui.messageBox('Not supported in current workspace. Please change to DESIGN and try again.')
            return

        cmdDefs = ui.commandDefinitions
        cmdDef = cmdDefs.itemById(ID)

        if not cmdDef:
            resourceDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources')
            cmdDef = cmdDefs.addButtonDefinition(ID,
                    'Import NL Spline',
                    'Import spline data from NoLimits',
                    resourceDir)

        add_handler(cmdDef.commandCreated, create_handler)
        
        cmdDef.execute()

        adsk.autoTerminate(False)
    except:
        handle_error('run')

def stop(context):
    try:
        # Clean up UI
        cmdDef = ui.commandDefinitions.itemById(ID)
        if cmdDef:
            cmdDef.deleteMe()
    except:
        handle_error('stop')