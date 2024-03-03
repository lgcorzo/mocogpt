from .core.actual_server import ActualGptServer
from .core.base_server import GptServer
from .core.base_typing import AnyOf, NoneOf, Contains, Startswith, Endswith, Regex

__all__ = [
    'any_of',
    'none_of',
    'gpt_server'
]


def any_of(*args):
    return AnyOf(*args)


def none_of(*args):
    return NoneOf(*args)


def contains(arg):
    return Contains(arg)


def startswith(arg):
    return Startswith(arg)


def endswith(arg):
    return Endswith(arg)


def regex(arg):
    return Regex(arg)


def gpt_server(port) -> GptServer:
    return ActualGptServer(port)
