import cmd
from pyparsing import ParseException

from .language import parser
from .runner import Runner


class InteractiveWim(cmd.Cmd):
    prompt = ':'
    use_rawinput = True

    def onEOF(self, f):
        self.onEOF = f

    def setModel(self, m):
        self.model = m

    def do_EOF(self, _line):
        print
        if self.onEOF is not None:
            self.onEOF()
        return True

    def default(self, line):
        command = self._parse(line)
        runner = Runner(command, self.model)
        return runner.run()

    def _parse(self, line):
        try:
            return parser.parseString(line)
        except ParseException, e:
            print "ParseException:", e
            return {}
