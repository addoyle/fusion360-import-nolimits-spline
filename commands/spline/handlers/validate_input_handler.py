import adsk.core, adsk.fusion
from ....common.util import ui
from ..state import spline

def validate_input_handler(args: adsk.core.ValidateInputsEventArgs):
    args.areInputsValid = len(ui.activeSelections) == 1 and len(spline.center) > 0