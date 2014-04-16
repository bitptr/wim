import cmd
from .language import parser, RunnerFor
from pyparsing import ParseException


class InteractiveWim(cmd.Cmd):
    prompt = ':'
    use_rawinput = True

    def do_EOF(self, _line):
        print
        return True

    def default(self, line):
        command = self._parse(line)
        runner = RunnerFor(command)
        return runner.run()

    def _parse(self, line):
        try:
            return parser.parseString(line)
        except ParseException:
            return '?'
