from array import array
import adsk.core
import adsk.fusion
from ....common.util import app
from ..state import supports
from ....model.support.Structure import Structure
from ..generators.footer_generator import generate_footer


def execute_handler(args: adsk.core.CommandEventArgs):
    design = adsk.fusion.Design.cast(app.activeProduct)

    inputs = args.command.commandInputs

    # spline_chooser: adsk.core.ButtonRowCommandInput = inputs.itemById(
    #     'railSplines')
    # show_left_spline = spline_chooser.listItems.item(0).isSelected
    # show_center_spline = spline_chooser.listItems.item(1).isSelected
    # show_right_spline = spline_chooser.listItems.item(2).isSelected
    plane_selection_input = inputs.itemById('plane')

    # start_point_input: adsk.core.IntegerSpinnerCommandInput = inputs.itemById(
    #     'startPoint')
    # end_point_input: adsk.core.IntegerSpinnerCommandInput = inputs.itemById(
    #     'endPoint')

    if plane_selection_input.selectionCount:
        plane = plane_selection_input.selection(0).entity

        if supports.structures.count:
            struc: Structure = supports.structures[0]

            for footer in struc.footers:
                generate_footer(plane, footer)


def points_in_range(pts: array, start: int, end: int):
    return pts[start - 1:end]
