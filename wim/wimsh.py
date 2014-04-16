import readline
from gi.repository import Gdk
import sys
from .runner import InteractiveWim


def main():
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind('bind ^I rl_complete')

    Gdk.init(sys.argv)
    InteractiveWim().cmdloop()
