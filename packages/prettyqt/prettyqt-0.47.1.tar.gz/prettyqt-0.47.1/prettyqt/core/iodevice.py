# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore

from prettyqt import core


QtCore.QIODevice.__bases__ = (core.Object,)


class IODevice(QtCore.QIODevice):
    pass
