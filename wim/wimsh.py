import readline
from gi.repository import Gdk, GObject
import sys
import thread
from .runner import InteractiveWim
from .model import Model


def main():
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind('bind ^I rl_complete')

    model = Model()
    interact = InteractiveWim()
    interact.onEOF(model.shutdown)
    interact.setModel(model)

    Gdk.init(sys.argv)
    model.startup()
    thread.start_new_thread(GObject.MainLoop().run, ())
    interact.cmdloop()
