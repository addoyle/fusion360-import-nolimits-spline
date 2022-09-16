import adsk.core, adsk.fusion
from ..common.util import app, log, ui, spline

def validate_input_handler(args: adsk.core.ValidateInputsEventArgs):
    global app, ui, spline

    log(str(len(spline.center)))

    args.areInputsValid = len(ui.activeSelections) == 1 and len(spline.center) > 0