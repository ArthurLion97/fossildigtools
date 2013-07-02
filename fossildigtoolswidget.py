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

from PyQt4 import QtCore, QtGui
from ui_fossildigtools import Ui_FossilDigTools
# create the dialog for zoom to point


class FossilDigToolsWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_FossilDigTools()
        self.ui.setupUi(self)
