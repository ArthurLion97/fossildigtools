# -*- coding: utf-8 -*-
"""
/***************************************************************************
 FossilDigToolsWidget
                                 A QGIS plugin
 Interface and tools to help illustrate fossil digs
                             -------------------
        begin    : 2013-07-02
        copyright: (C) 2013 by Black Hills Institute of Geological Research
        email    : larrys@bhigr.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import sys
import math
from itertools import ifilter
from operator import itemgetter

from qgis.core import *
from qgis.gui import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *

PVDEV = False
try:
    # conditional for when pydev is stripped for release
    from .pydev import pydevd
    PVDEV = True
except ImportError:
    pass


class FdtUtilities(object):

    def __init__(self, parent, iface, settings, qgsettings):
        self.iface = iface
        self.msgbar = self.iface.messageBar()
        self.settings = settings
        self.qgsettings = qgsettings
        self.proj = QgsProject.instance()

        self.redhlcolor = QColor(225, 0, 0)
        self.bluehlcolor = QColor(0, 0, 225)
        self.circlesegments = 32
        self.removehighlightsmilli = 2000
        self.highlights = []


    def pydev(self):
        if not PVDEV:
            return
        try:  # or it crashes QGIS if connection to debug server unavailable
            pydevd.settrace('localhost',
                            port=53100,
                            stdoutToServer=True,
                            stderrToServer=True)
        except:
            pass


if __name__ == "__main__":
    pass
