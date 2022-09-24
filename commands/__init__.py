from .spline import entry as spline

commands = [
    spline
]

def start():
    for command in commands:
        command.start()

def stop():
    for command in commands:
        command.stop()