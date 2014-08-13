Development
===========

Prerequisites (Debian):

    % sudo apt-get install python-gi libwnck-3-* gir1.2-wnck-3.0

Prerequisites (OpenBSD):

    % sudo pkg_add py-gobject libwnck

Virtualenv:

    % mkvirtualenv --system-site-packages wim

Install dependencies:

    % pip install -r requirements.txt

Build program locally:

    % python setup.py develop

Run it:

    % ~/.virtualenvs/wim/bin/wimsh

Resources
---------

* [Extended Window Manager Hints][ewmh] (EWMH)
* [Wnck Docs for C][docs] (None exist for Python; Wnck is an implementation of
  EWMH)
* xprop(1)
* xwininfo(1)

[ewmh]: http://standards.freedesktop.org/wm-spec/wm-spec-latest.html
[docs]: https://developer.gnome.org/libwnck/stable/core.html
