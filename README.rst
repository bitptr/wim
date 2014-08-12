===
wim
===

Installation
------------

::

    % python setup.py install

Usage
-----

See wim(7) for details on the language and how it's used::

    % man 7 wim

Development
-----------

Prerequisites (Debian)::

    % sudo apt-get install python-gi libwnck-3-* gir1.2-wnck-3.0

Prerequisites (OpenBSD)::

    % sudo pkg_add py-gobject libwnck

Virtualenv::

    % mkvirtualenv --system-site-packages wim

Author
------
Copyright 2014 Mike Burns. Licensed under BSD 3-clause license.
