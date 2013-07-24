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

from qgis.gui import *

import sip
from PyQt4.QtCore import *


class FdtEmitPointTool(QgsMapToolEmitPoint):
    """Canvas point capture, with auto-reset to previous map tool,
    auto-connections to a checkable tool button, and mouse release signal
    """
    mouseReleased = pyqtSignal()
    # base class overriden canvasPressEvent( QMouseEvent * e ) emits:
    # canvasClicked( const QgsPoint& point, Qt::MouseButton button )

    def __init__(self, canvas, button, reset=True):
        QgsMapToolEmitPoint.__init__(self, canvas)
        self.canvas = canvas
        self.button = button
        self.reset = reset
        self.prevtool = None

        self.setButton(self.button)

        if self.button.isCheckable():
            self.button.clicked[bool].connect(self.tool_button_clicked)

    def __del__(self):
        if self.reset and self.prevtool != self:
            self.reset_tool()

    def canvasReleaseEvent(self, e):
        QgsMapToolEmitPoint.canvasReleaseEvent(self, e)
        self.mouseReleased.emit()  # bonus signal
        self.deactivate()

    @pyqtSlot("QgsMapTool *")
    def set_prev_tool(self, tool=None):
        if not tool:
            tool = self.canvas.mapTool()
        if tool != self:
            self.prevtool = tool

    def reset_tool(self):
        self.canvas.setMapTool(self.prevtool)

    def deactivate(self):
        # don't try to uncheck button if called from __del__ (may not exist)
        if not sip.isdeleted(self.button):
            if self.button.isCheckable():
                self.button.setChecked(False)

        if self.reset:
            self.reset_tool()

    @pyqtSlot(bool)
    def tool_button_clicked(self, chkd):
        if self.button.isChecked():
            if self.reset:
                self.set_prev_tool()
            self.canvas.setMapTool(self)
        else:
            self.deactivate()
