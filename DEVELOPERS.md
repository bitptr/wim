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

    % wim-gtk

Resources
---------

* [Extended Window Manager Hints][ewmh] (EWMH)
* [Wnck Docs for C][docs] (None exist for Python; Wnck is an implementation of
  EWMH)
* [The Python GTK+ 3 Tutorial][tutorial]
* [Python GObject Introspection API Reference][gi]
* xprop(1)
* xwininfo(1)

[ewmh]: http://standards.freedesktop.org/wm-spec/wm-spec-latest.html
[docs]: https://developer.gnome.org/libwnck/stable/core.html
[tutorial]: http://python-gtk-3-tutorial.readthedocs.org/en/latest/index.html
[gi]: http://lazka.github.io/pgi-docs/
