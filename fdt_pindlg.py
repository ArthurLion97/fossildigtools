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

from qgis.core import *
from qgis.gui import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Ui_fdt_pindlg import Ui_PinDialog


class FdtPinTool(QgsMapToolEmitPoint):
    mouseReleased = pyqtSignal()

    def __init__(self, canvas):
        QgsMapToolEmitPoint.__init__(self, canvas)

    def canvasReleaseEvent(self, e):
        QgsMapToolEmitPoint.canvasReleaseEvent(self, e);
        self.mouseReleased.emit()

class FdtPinDialog(QDialog):
    def __init__(self, parent, iface, kind, origin=None, feat=None):
        QDialog.__init__(self, parent)
        self.setWindowFlags(Qt.Tool|Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.parent = parent
        self.iface = iface
        self.kind = kind
        self.origin = origin
        self.feat = feat
        self.canvas = self.iface.mapCanvas()

        # set up the user interface from Designer.
        self.ui = Ui_PinDialog()
        self.ui.setupUi(self)

        self.ui.buttonBox.clicked[QAbstractButton].connect(self.dialog_action)

        self.init_values()

        self.pinTool = FdtPinTool(self.canvas)
        # connect signal that the canvas was clicked
        self.pinTool.canvasClicked[QgsPoint,Qt.MouseButton].connect(self.place_pin)
        self.pinTool.mouseReleased.connect(self.reset_tool)

        self.set_prev_tool()

        self.restoreGeometry(self.parent.settings.value("/pinDialog/geometry",
                                                        QByteArray(),
                                                        type=QByteArray))

    def save_geometry(self):
        self.parent.settings.setValue("/pinDialog/geometry", self.saveGeometry())

    def closeEvent(self, e):
        self.save_geometry()
        QDialog.closeEvent(self, e)

    def init_values(self):
        # defaults
        origin = ""
        kindtxt = self.tr("Origin")
        if self.kind == "origin":
            self.ui.pinOriginFrame.setVisible(False)
            self.ui.capturePinBtn.setIcon(QIcon(":/plugins/fossildigtools/icons/capturepin-origin.svg"))
        else:
            self.ui.pinOriginFrame.setVisible(True)
            if self.orgin:
                origin = self.orgin
            kindtxt = self.tr("Directional")
            self.ui.capturePinBtn.setIcon(QIcon(":/plugins/fossildigtools/icons/capturepin-directional.svg"))

        name = ""
        x = 0.0
        y = 0.0
        info = ""
        setter = ""
        date = QDate.currentDate().toString("yyyy/MM/dd")

        if self.feat:
            point = self.feat.geometry().asPoint()

            name = self.feat["name"]
            x = point.x()
            y = point.y()
            info = self.feat["info"]
            setter = self.feat["setter"]
            date = self.feat["date"]

        self.ui.pinNameLineEdit.setText(name)
        self.ui.pinKindLabel.setText(kindtxt)
        self.ui.pinOriginLineEdit.setText(origin)
        self.ui.pinXSpinBx.setValue(x)
        self.ui.pinYSpinBx.setValue(y)
        self.ui.pinInfoTextEdit.setPlainText(info)
        self.ui.pinSetByLineEdit.setText(setter)
        self.ui.pinDateEdit.setDate(QDate.fromString(date, "yyyy/MM/dd"))

    def save_values(self):
        pinLyr = self.parent.get_layer(self.parent.pin_layer_id())
        if not pinLyr:
            return
        pinLyr.startEditing()
        feature = self.feat if self.feat else QgsFeature()
        point = QgsPoint(self.ui.pinXSpinBx.value(), self.ui.pinYSpinBx.value())
        feature.setGeometry(QgsGeometry.fromPoint(point))

        if not self.feat:
            feature["kind"] = self.kind
        feature["name"] = self.ui.pinNameLineEdit.text()
        feature["origin"] = self.origin
        feature["description"] = self.ui.pinInfoTextEdit.toPlainText()
        feature["setter"] = self.ui.pinSetByLineEdit.text()
        feature["date"] = self.ui.pinDateEdit.date().toString("yyyy/MM/dd")

        if not self.feat:
            pinLyr.addFeature(feature, True)
        pinLyr.commitChanges()
        pinLyr.setCacheImage(None)
        pinLyr.triggerRepaint()

    def check_values(self):
        # verify everything is filled out and coords aren't wrong-ish
        pass

    @pyqtSlot(QAbstractButton)
    def dialog_action(self, btn):
        if btn == self.ui.buttonBox.button(QDialogButtonBox.Ok):
            if self.check_values():
                self.save_values()
                self.accept()
        else:
            self.close()

    @pyqtSlot(bool)
    def on_capturePinBtn_clicked(self, chkd):
        self.set_prev_tool()
        if not chkd:
            self.reset_tool()
            return
        self.canvas.setMapTool(self.pinTool)

        # get the x,y and create the pin
    def place_pin(self, point, button):
        # user might remove the layer so we have to check each time

        #QMessageBox.information( self.iface.mainWindow(), "Coords", "X,Y = %s,%s" % (str(point.x()),str(point.y())) )
        self.ui.pinXSpinBx.setValue(point.x())
        self.ui.pinYSpinBx.setValue(point.y())

        if self.ui.capturePinBtn.isCheckable():
            self.ui.capturePinBtn.setChecked(False)

        self.raise_()
        self.activateWindow()

    def set_prev_tool(self):
        if self.canvas.mapTool() != self.pinTool:
            self.prevTool = self.canvas.mapTool()
        if not self.prevTool:  # default to pan tool
            self.iface.actionPan().trigger()
            self.prevTool = self.canvas.mapTool()

    def reset_tool(self):
        self.canvas.setMapTool(self.prevTool)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    settingsDlg = FdtPinDialog()
    settingsDlg.show()
    settingsDlg.raise_()
    settingsDlg.activateWindow()
    sys.exit(app.exec_())
