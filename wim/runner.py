import cmd
from .language import parser, RunnerFor


class InteractiveWim(cmd.Cmd):
    prompt = ': '
    use_rawinput = True

    def do_EOF(self, _line):
        print
        return True

    def default(self, line):
        command = parser.parseString(line)
        runner = RunnerFor(command)
        return runner.run()
