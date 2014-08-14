===
wim
===

Window management as inspired by ed(1).  This is a small language for
manipulating your windows.  It is not a window manager but instead an interface
to your window manager.

The wim-gtk(1) program is a GTK+ panel that sits at the bottom of your screen,
awaiting wim(7) commands.  It has the special property that `%` and `#` ignore
wim-gtk(1) itself. All other commands include the relevant running wim-gtk(1)
windows.


Installation
------------

::

    % python setup.py install

Usage
-----

See wim(7) for details on the language and how it's used::

    % man 7 wim

To actually run the program::

    % wim-gtk

Author
------
Copyright 2014 Mike Burns and Rebecca Meritz. Licensed under BSD 3-clause
license.
