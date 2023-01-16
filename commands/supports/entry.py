#Author-Andy Doyle
#Description-Imports support XML data from NoLimits

import adsk.core, adsk.fusion, adsk.cam, os

from .handlers.created_handler import create_handler
from ... import config
from ...common.util import add_handler, ui

CMD_NAME = 'Import Supports'
CMD_ID = f'{config.ADDIN_NAME}_{CMD_NAME}'
CMD_Desc = 'Import Supports'

ICON_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', '')

def start():
    cmd_def = ui.commandDefinitions.itemById(CMD_ID)
    if cmd_def is None:
        cmd_def = ui.commandDefinitions.addButtonDefinition(CMD_ID, CMD_NAME, CMD_Desc, ICON_FOLDER)
    
    add_handler(cmd_def.commandCreated, create_handler)

    workspace = ui.workspaces.itemById(config.WORKSPACE_ID)

    toolbar_tab = workspace.toolbarTabs.itemById(config.TAB_ID)
    if toolbar_tab is None:
        toolbar_tab = workspace.toolbarTabs.add(config.TAB_ID, config.TAB_NAME)

    panel = toolbar_tab.toolbarPanels.itemById(config.PANEL_ID)
    if panel is None:
        panel = workspace.toolbarPanels.add(config.PANEL_ID, config.PANEL_NAME, '', False)
    
    control: adsk.core.CommandControl = panel.controls.addCommand(cmd_def)
    control.isPromoted = False

def stop():
    workspace = ui.workspaces.itemById(config.WORKSPACE_ID)
    panel = workspace.toolbarPanels.itemById(config.PANEL_ID)
    toolbar_tab = workspace.toolbarTabs.itemById(config.TAB_ID)
    command_control = panel.controls.itemById(CMD_ID)
    command_definition = ui.commandDefinitions.itemById(CMD_ID)

    if command_control:
        command_control.deleteMe()
    if command_definition:
        command_definition.deleteMe()
    if panel.controls.count == 0:
        panel.deleteMe()
    if toolbar_tab and toolbar_tab.toolbarPanels.count == 0:
        toolbar_tab.deleteMe()