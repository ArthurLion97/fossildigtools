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
import re

from qgis.core import *
from qgis.gui import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Ui_fdt_pindlg import Ui_PinDialog
from fdt_emitpoint import FdtEmitPointTool


class FdtPinDialog(QDialog, Ui_PinDialog):
    def __init__(self, parent, iface, pinkind, feat=None):
        QDialog.__init__(self, parent)
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.p = parent
        self.iface = iface
        self.pinkind = pinkind
        self.origin = pinkind == "origin"
        self.originfeat = None if self.origin else self.p.current_origin_feat()
        self.originpt = None if self.origin else self.p.current_origin_point()
        self.feat = feat
        self.canvas = self.iface.mapCanvas()

        # set up the user interface from Designer.
        # self.ui = Ui_PinDialog()
        self.setupUi(self)

        self.init_values()
        self.check_values()

        self.pinNameLineEdit.textChanged.connect(self.check_values)
        self.pinXDblSpinBx.valueChanged.connect(self.check_values)
        self.pinYDblSpinBx.valueChanged.connect(self.check_values)
        self.pinSetByLineEdit.textChanged.connect(self.check_values)

        self.pinTool = FdtEmitPointTool(self.canvas, self.capturePinBtn)
        self.pinTool.canvasClicked[QgsPoint,Qt.MouseButton].connect(
            self.place_pin)

        self.buttonBox.clicked[QAbstractButton].connect(self.dialog_action)
        self.restoreGeometry(self.p.settings.value(
            "/pinDialog/geometry",
            QByteArray(),
            type=QByteArray))

        self.pinNameLineEdit.setFocus()

    def save_geometry(self):
        self.p.settings.setValue("/pinDialog/geometry", self.saveGeometry())

    def closeEvent(self, e):
        self.pinTool.deactivate()
        del self.pinTool
        self.save_geometry()
        QDialog.closeEvent(self, e)

    def init_values(self):
        # defaults
        originname = ""
        kindtxt = self.tr("Origin")
        if self.origin:
            self.pinOriginLabel.setVisible(False)
            self.pinOriginLineEdit.setVisible(False)
            self.calcFrame.setVisible(False)
            self.capturePinBtn.setIcon(
                QIcon(":/plugins/fossildigtools/icons/"
                      "capturepin-origin.svg"))
        else:  # directional
            self.pinOriginLabel.setVisible(True)
            self.pinOriginLineEdit.setVisible(True)
            self.calcFrame.setVisible(True)
            self.calcTabWidget.setTabEnabled(
                self.calcTabWidget.indexOf(self.calcOffset), False)
            self.calcTabWidget.setTabEnabled(
                self.calcTabWidget.indexOf(self.calcAzimuth), False)
            originname = self.originfeat['name']
            kindtxt = self.tr("Directional")
            self.capturePinBtn.setIcon(
                QIcon(":/plugins/fossildigtools/icons/"
                      "capturepin-directional.svg"))

        name = ""
        x = 0.0
        y = 0.0
        elev = 0.0
        elevu = 0
        info = ""
        setter = ""
        date = QDate.currentDate().toString("yyyy/MM/dd")

        if self.feat:
            point = self.feat.geometry().asPoint()

            name = self.feat["name"]
            x = point.x()
            y = point.y()
            h = self.feat["elevation"]
            if h is not None:
                elev = h
            u = self.feat["elevunit"]
            if u is not None:
                elevu = u
            info = self.feat["description"]
            setter = self.feat["setter"]
            date = self.feat["date"]

        self.pinNameLineEdit.setText(name)
        self.pinKindLabel.setText(kindtxt)
        self.pinOriginLineEdit.setText(originname)
        self.pinXDblSpinBx.setValue(x)
        self.pinYDblSpinBx.setValue(y)
        self.pinElevDblSpnBx.setValue(elev)
        self.pinElevUnitsCmbBx.setCurrentIndex(elevu)
        self.pinInfoTextEdit.setPlainText(info)
        self.pinSetByLineEdit.setText(setter)
        self.pinDateEdit.setDate(QDate.fromString(date, "yyyy/MM/dd"))

    def save_values(self):
        pinLyr = self.p.pin_layer()
        if not pinLyr:
            return
        pinLyr.startEditing()
        feat = self.feat if self.feat else QgsFeature()
        point = QgsPoint(self.pinXDblSpinBx.value(),
                         self.pinYDblSpinBx.value())
        feat.setGeometry(QgsGeometry.fromPoint(point))

        if not self.feat:
            fields = pinLyr.pendingFields()
            feat.setFields(fields)
            feat["kind"] = self.pinkind

        feat["name"] = self.pinNameLineEdit.text()
        feat["origin"] = -1 if self.origin else self.originfeat['pkuid']
        feat["elevation"] = self.pinElevDblSpnBx.value()
        feat["elevunit"] = self.pinElevUnitsCmbBx.currentIndex()
        feat["description"] = self.pinInfoTextEdit.toPlainText()
        feat["setter"] = self.pinSetByLineEdit.text()
        feat["date"] = self.pinDateEdit.date().toString("yyyy/MM/dd")

        if self.feat:
            pinLyr.updateFeature(feat)
        else:
            pinLyr.addFeature(feat, True)
        pinLyr.commitChanges()
        pinLyr.setCacheImage(None)
        pinLyr.triggerRepaint()

    def check_values(self):
        # verify everything is filled out and coords aren't wrong-ish
        badle = self.p.badLineEditValue
        baddblsb = self.p.badDblSpinBoxValue

        nameok = self.pinNameLineEdit.text() != ""
        self.pinNameLineEdit.setStyleSheet("" if nameok else badle)

        setbyok = self.pinSetByLineEdit.text() != ""
        self.pinSetByLineEdit.setStyleSheet("" if setbyok else badle)

        p = re.compile('\d+\.\d+')
        x = self.pinXDblSpinBx.value()
        xok = (int(x) != 0 and p.match(str(x)) is not None)
        self.pinXDblSpinBx.setStyleSheet("" if xok else baddblsb)

        y = self.pinYDblSpinBx.value()
        yok = (int(y) != 0 and p.match(str(y)) is not None)
        self.pinYDblSpinBx.setStyleSheet("" if yok else baddblsb)

        return nameok and setbyok and xok and yok

    @pyqtSlot(QAbstractButton)
    def dialog_action(self, btn):
        if btn == self.buttonBox.button(QDialogButtonBox.Ok):
            if self.check_values():
                self.save_values()
                self.accept()
        else:
            self.close()

    def offset_origin_coords(self, offset=(0.0, 0.0)):
        dist = self.p.to_meters(self.fromOriginDistDblSpnBx.value(),
                                self.fromOriginUnitsCmbBx.currentText())
        if int(dist) == 0:
            return
        self.pinXDblSpinBx.setValue(self.originpt.x() + dist * offset[0])
        self.pinYDblSpinBx.setValue(self.originpt.y() + dist * offset[1])

    @pyqtSlot()
    def on_toNBtn_clicked(self):
        self.offset_origin_coords((0.0, 1.0))

    @pyqtSlot()
    def on_toSBtn_clicked(self):
        self.offset_origin_coords((0.0, -1.0))

    @pyqtSlot()
    def on_toEBtn_clicked(self):
        self.offset_origin_coords((1.0, 0.0))

    @pyqtSlot()
    def on_toWBtn_clicked(self):
        self.offset_origin_coords((-1.0, 0.0))

    def place_pin(self, point, button):
        #TODO: user might remove the layer so we have to check each time

        # QMessageBox.information(
        #     self.iface.mainWindow(),
        #     "Coords",
        #     "X,Y = %s,%s" % (str(point.x()), str(point.y())))
        self.pinXDblSpinBx.setValue(point.x())
        self.pinYDblSpinBx.setValue(point.y())

        self.raise_()
        self.activateWindow()


if __name__ == "__main__":
    pass
