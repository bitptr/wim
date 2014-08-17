import sys
import signal

from gi.repository import Gtk, Gdk

from .wnck_wrapper import WnckWrapper
from .parser import parse
from .runner import Runner
from .exception import WimException


class WimGtk(object):
    def run(self):
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        Gtk.init(sys.argv)
        window = self._prepare_window()
        self.wnck_wrapper = WnckWrapper(avoid=window).startup()
        Gtk.main()

    def _prepare_window(self):
        window = Gtk.Window.new(Gtk.WindowType.TOPLEVEL)
        window.connect("delete-event", Gtk.main_quit)
        window.set_decorated(False)
        window.set_keep_above(True)
        self._set_window_on_bottom(window)

        text = Gtk.Entry.new()
        text.connect("activate", self._run_entry)

        window.add(text)
        window.show_all()

        return window

    def _run_entry(self, entry):
        line = entry.get_text()
        try:
            Runner(parse(line), self.wnck_wrapper).run()
            entry.set_text("")
            entry.set_icon_from_stock(0)
        except WimException, e:
            entry.set_icon_from_stock(0, Gtk.STOCK_DIALOG_ERROR)
            entry.set_text(line + "  " + e.message)

    def _set_window_on_bottom(self, window):
        screen_height = Gdk.Screen.height()
        height = 20
        window.set_default_size(Gdk.Screen.width(), height)
        window.move(0, screen_height - height)


def main():
    WimGtk().run()
