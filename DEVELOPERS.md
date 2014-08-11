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

Style Guide
-----------

- [PEP8][pep8]

- Imports should be divide into 3 sections with a line break in between:
1) Python imports
2) Third Party library imports
3) Local imports (always proceded by a . or ..)

- No space should be left btw class declarions and the first method


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
[pep8]: http://legacy.python.org/dev/peps/pep-0008/
