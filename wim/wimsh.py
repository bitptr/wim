import readline
from .runner import InteractiveWim


def main():
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind('bind ^I rl_complete')

    InteractiveWim().cmdloop()
