from .spline import entry as spline
from .supports import entry as supports

commands = [
    spline,
    supports
]


def start():
    for command in commands:
        command.start()


def stop():
    for command in commands:
        command.stop()
