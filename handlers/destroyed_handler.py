import adsk.core
from ..common.util import handle_error

def destroy_handler(args: adsk.core.CommandEventArgs):
    try:
        adsk.terminate()
    except:
        handle_error('destroy')