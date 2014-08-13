from gi.repository import Gtk, Gdk
import sys
import signal
from pyparsing import ParseException

from .model import Model
from .language import parser
from .runner import Runner


class Main(object):
    def run(self):
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        Gtk.init(sys.argv)

        window = self._prepare_window()

        self.model = Model(avoid=window)
        self.model.startup()

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
        self._run_line(line)

    def _run_line(self, line):
        command = self._parse(line)
        runner = Runner(command, self.model)
        runner.run()

    def _parse(self, line):
        try:
            return parser.parseString(line)
        except ParseException, e:
            print "ParseException:", e
            return {}

    def _set_window_on_bottom(self, window):
        screen_width = Gdk.Screen.width()
        screen_height = Gdk.Screen.height()

        width = screen_width
        height = 20
        x = 0
        y = screen_height - height

        window.set_default_size(width, height)
        window.move(x, y)



def main():
    m = Main()
    m.run()
