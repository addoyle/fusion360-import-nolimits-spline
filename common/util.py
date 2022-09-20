import sys, traceback, adsk.core
from typing import Callable

from ..model.Spline import Spline

# Handlers should be added here to keep them in scope
handlers = []

# Easier access to form inputs
command_inputs = {}

# Spline data
spline = Spline()

app = adsk.core.Application.get()
ui = app.userInterface

try:
    from .. import config
    DEBUG = config.DEBUG
except:
    DEBUG = False

def add_handler(event: adsk.core.Event, callback: Callable, *, name: str = None, local_handlers: list = None):
    module = sys.modules[event.__module__]
    handler_type = module.__dict__[event.add.__annotations__['handler']]
    handler = create_handler(handler_type, callback, event, name, local_handlers)
    event.add(handler)
    return handler

def clear_handlers():
    global handlers
    handlers = []

def create_handler(handler_type, callback: Callable, event: adsk.core.Event, name: str = None, local_handlers: list = None):
    global handlers

    handler = define_handler(handler_type, callback, name)()
    (local_handlers if local_handlers is not None else handlers).append(handler)
    return handler

def define_handler(handler_type, callback, name: str = None):
    name = name or handler_type.__name__

    class Handler(handler_type):
        def __init__(self):
            super().__init__()
        def notify(self, args):
            try:
                callback(args)
            except:
                handle_error(name)
    
    return Handler

def log(message: str, level: adsk.core.LogLevels = adsk.core.LogLevels.InfoLogLevel, force_console: bool = False):
    try:
        # Print to console, only seen through IDE
        print(message)

        # Log all errors to Fusion log file
        if level == adsk.core.LogLevels.ErrorLogLevel:
            log_type = adsk.core.LogTypes.FileLogType
            app.log(message, level, log_type)
        
        # If config.DEBUG is True, write all log messages to console
        if DEBUG or force_console:
            log_type = adsk.core.LogTypes.ConsoleLogType
            app.log(message, level, log_type)
    except:
        ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def handle_error(name: str, show_message_box: bool = False):
    log('===== Error =====', adsk.core.LogLevels.ErrorLogLevel)
    log(f'{name}\n{traceback.format_exc()}', adsk.core.LogLevels.ErrorLogLevel)

    if show_message_box:
        ui.messageBox(f'{name}\n{traceback.format_exc()}')