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

import geomag
from qgis.core import *
from qgis.gui import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Ui_fdt_geomagdlg import Ui_GeoMagDialog
from fdt_emitpoint import FdtEmitPointTool


class FdtGeoMagDialog(QDialog, Ui_GeoMagDialog):
    def __init__(self, parent, iface, originfeat=None):
        QDialog.__init__(self, parent)
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.p = parent
        self.iface = iface
        self.originfeat = originfeat
        self.canvas = self.iface.mapCanvas()

        # set up the user interface from Designer.
        self.setupUi(self)

        self.captureTool = FdtEmitPointTool(self.canvas, self.captureLocBtn)
        self.captureTool.canvasClicked[QgsPoint,Qt.MouseButton].connect(
            self.update_coords)

        self.buttonBox.rejected.connect(self.reject)

        self.restoreGeometry(self.p.settings.value(
            "/geoMagDialog/geometry",
            QByteArray(),
            type=QByteArray))

        self.init_values()
        if self.originfeat:
            self.calculate_declination()

        self.decXDblSpinBx.valueChanged.connect(self.calculate_declination)
        self.decYDblSpinBx.valueChanged.connect(self.calculate_declination)
        self.decElevDblSpnBx.valueChanged.connect(self.calculate_declination)
        self.decElevUnitsCmbBx.currentIndexChanged[int].connect(
            self.calculate_declination)

    def closeEvent(self, e):
        self.captureTool.deactivate()
        del self.captureTool
        self.p.settings.setValue("/geoMagDialog/geometry", self.saveGeometry())
        QDialog.closeEvent(self, e)

    def init_values(self):
        # defaults
        originname = ""
        x = 0.0
        y = 0.0
        elev = 0.0
        elevu = 0

        if self.originfeat:
            point = self.originfeat.geometry().asPoint()

            originname = self.originfeat["name"]
            x = point.x()
            y = point.y()
            h = self.originfeat["elevation"]
            if h is not None:
                elev = h
            u = self.originfeat["elevunit"]
            if u is not None:
                elevu = u

        self.decOriginLineEdit.setText(originname)
        self.decXDblSpinBx.setValue(x)
        self.decYDblSpinBx.setValue(y)
        self.decElevDblSpnBx.setValue(elev)
        self.decElevUnitsCmbBx.setCurrentIndex(elevu)

    def update_coords(self, point, button):
        # clear origin name, because no longer referenced
        self.decOriginLineEdit.clear()
        # leave elevation, since it is probably a nearby location?
        #self.decElevationDblSpnBx.clear()

        # QMessageBox.information(
        #     self.iface.mainWindow(),
        #     "Coords",
        #     "X,Y = %s,%s" % (str(point.x()), str(point.y())))
        self.decXDblSpinBx.blockSignals(True)
        self.decYDblSpinBx.blockSignals(True)

        self.decXDblSpinBx.setValue(point.x())
        self.decYDblSpinBx.setValue(point.y())

        self.decXDblSpinBx.blockSignals(False)
        self.decYDblSpinBx.blockSignals(False)

        self.raise_()
        self.activateWindow()
        self.calculate_declination()

    def clear_declination_values(self):
        self.decCurrentDblSpinBox.clear()
        self.decNBearingDblSpnBx.clear()
        self.decEBearingDblSpnBx.clear()
        self.decWBearingDblSpnBx.clear()
        self.decSBearingDblSpnBx.clear()

    def calculate_mag_bearing(self, actual, gmdec):
        return (actual - gmdec + 360.0) % 360

    @pyqtSlot()
    def calculate_declination(self):
        baddblsb = self.p.badDblSpinBoxValue

        p = re.compile('\d+\.\d+')
        x = self.decXDblSpinBx.value()
        xok = (int(x) != 0 and p.match(str(x)) is not None)
        self.decXDblSpinBx.setStyleSheet("" if xok else baddblsb)

        y = self.decXDblSpinBx.value()
        yok = (int(y) != 0 and p.match(str(y)) is not None)
        self.decYDblSpinBx.setStyleSheet("" if yok else baddblsb)

        # NOTE: elevation value can be 0; approx. value will increase accuracy
        if not (xok or yok):
            self.clear_declination_values()
            return

        # transform UTM point to WGS 84, lat/lon
        pt = QgsPoint(self.decXDblSpinBx.value(), self.decYDblSpinBx.value())
        wgs84 = QgsCoordinateReferenceSystem(4326)
        # QgsMessageLog.logMessage("wgs84: {0}".format(wgs84.authid()),
        #                          self.tr("Fdt"), QgsMessageLog.INFO)
        mapcrs = self.canvas.mapRenderer().destinationCrs()
        # QgsMessageLog.logMessage("mapcrs: {0}".format(mapcrs.authid()),
        #                          self.tr("Fdt"), QgsMessageLog.INFO)
        xform = QgsCoordinateTransform(mapcrs, wgs84)
        wgspt = xform.transform(pt)
        # QgsMessageLog.logMessage(
        #     "wgspt:\n  {0}\n  {1}".format(wgspt.y(), wgspt.x()),
        #     self.tr("Fdt"), QgsMessageLog.INFO)

        # ensure height is in US feet
        h = self.decElevDblSpnBx.value()
        hinm = self.decElevUnitsCmbBx.currentIndex()  # 0 = ft, 1 = m
        elev = h if not hinm else h * 3.281

        gmdec = geomag.declination(wgspt.y(), wgspt.x(), elev)
        nb = self.calculate_mag_bearing(0, gmdec)
        eb = self.calculate_mag_bearing(90, gmdec)
        sb = self.calculate_mag_bearing(180, gmdec)
        wb = self.calculate_mag_bearing(270, gmdec)

        self.decCurrentDblSpinBox.setValue(gmdec)
        self.decNBearingDblSpnBx.setValue(nb)
        self.decEBearingDblSpnBx.setValue(eb)
        self.decSBearingDblSpnBx.setValue(sb)
        self.decWBearingDblSpnBx.setValue(wb)

if __name__ == "__main__":
    pass
