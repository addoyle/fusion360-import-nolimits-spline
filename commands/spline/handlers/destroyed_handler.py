import adsk.core
from ....common.util import log


def destroy_handler(args: adsk.core.CommandEventArgs):
    log('Destroyed')
