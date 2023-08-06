#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from glob import glob

name = "urwid_satext"

setup(
    name=name,
    version="0.7.0",
    description=u"SàT extension widgets for Urwid",
    long_description=(u"Urwid SàT extension widgets is a set of widgets for the console "
                      u"user interface library Urwid (http://excess.org/urwid/). This "
                      u"library, originaly made for the SàT project, was eventually "
                      u"separated so other softwares can use it. Widgets provided "
                      u"include password text box, tab container, dialogs, file chooser "
                      u"etc. Feel free to go to the project page for more informations."),
    author="Goffi (Jérôme Poisson)",
    author_email="goffi@goffi.org",
    url="http://wiki.goffi.org/wiki/Urwid-satext",
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Intended Audience :: Developers",
    ],
    packages=["urwid_satext"],
    data_files=[
        (
            "share/locale/fr/LC_MESSAGES",
            ["i18n/fr/LC_MESSAGES/urwid_satext.mo"],
        ),
        ("share/doc/%s/examples" % name, glob("examples/*.py")),
        ("share/doc/%s" % name, ["COPYING", "COPYING.LESSER", "README", "CHANGELOG"]),
    ],
    install_requires=["urwid >= 1.2.0"],
)
