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

from qgis.core import *
from qgis.gui import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Ui_fdt_settingsdlg import Ui_SettingsDialog


class FdtSettingsDialog(QDialog, Ui_SettingsDialog):
    def __init__(self, parent, iface, settings):
        QDialog.__init__(self, parent)
        self.parent = parent
        self.iface = iface
        self.settings = settings
        self.qgsettings = QSettings()
        self.proj = QgsProject.instance()

        # set up the user interface from Designer.
        self.setupUi(self)

        self.lyrCmbxs = [
            self.pinsCmbBx,
            self.gridsCmbBx,
            self.featuresCmbBx,
            self.sketchCmbBx
        ]
        self.pinsCmbBx.currentIndexChanged[int].\
            connect(self.validate_pins_combobox)
        self.gridsCmbBx.currentIndexChanged[int].\
            connect(self.validate_grids_combobox)
        self.featuresCmbBx.currentIndexChanged[int].\
            connect(self.validate_features_combobox)
        self.sketchCmbBx.currentIndexChanged[int]. \
            connect(self.validate_sketch_combobox)

        self.populate_comboboxes()

        self.gridsMajorSpnBx.valueChanged[int].connect(self.check_grid_squares)
        self.gridsMinorSpnBx.valueChanged[int].connect(self.check_grid_squares)

        self.init_values()

        self.check_layer_comboboxes()
        self.check_grid_squares()

        self.buttonBox.clicked[QAbstractButton].connect(self.dialog_action)

        self.restoreGeometry(self.settings.value("/settingsDialog/geometry",
                                                 QByteArray(),
                                                 type=QByteArray))

    def save_geometry(self):
        self.settings.setValue("/settingsDialog/geometry", self.saveGeometry())

    def closeEvent(self, e):
        self.save_geometry()
        QDialog.closeEvent(self, e)

    def populate_comboboxes(self):
        lyrsdict = self.parent.spatialite_layers_dict()
        for cmbx in self.lyrCmbxs:
            cmbx.clear()
            cmbx.addItem("", "invalid")
            for lyrid, lyr in lyrsdict.iteritems():
                cmbx.addItem(lyr.name(), lyrid)

    def init_values(self):
        # load values from project
        self.pinsCmbBx.setCurrentIndex(
            self.pinsCmbBx.findData(self.parent.pin_layer_id()))
        self.gridsCmbBx.setCurrentIndex(
            self.gridsCmbBx.findData(self.parent.grid_layer_id()))
        self.featuresCmbBx.setCurrentIndex(
            self.featuresCmbBx.findData(self.parent.feature_layer_id()))
        self.sketchCmbBx.setCurrentIndex(
            self.sketchCmbBx.findData(self.parent.sketch_layer_id()))

        self.gridsUnitCmdBx.setCurrentIndex(self.parent.grid_unit_index())
        self.gridsMajorSpnBx.setValue(self.parent.major_grid())
        self.gridsMinorSpnBx.setValue(self.parent.minor_grid())
        self.gridsBufferMajor.setChecked(self.parent.buffer_major_grid())

    def save_values(self):
        # store values in project
        self.proj.writeEntry("fdt", "pinsLayerId",
            self.pinsCmbBx.itemData(self.pinsCmbBx.currentIndex()))
        self.proj.writeEntry("fdt", "gridsLayerId",
            self.gridsCmbBx.itemData(self.gridsCmbBx.currentIndex()))
        self.proj.writeEntry("fdt", "featuresLayerId",
            self.featuresCmbBx.itemData(self.featuresCmbBx.currentIndex()))
        self.proj.writeEntry("fdt", "sketchLayerId",
            self.sketchCmbBx.itemData(self.sketchCmbBx.currentIndex()))

        self.proj.writeEntry("fdt", "gridSquaresUnit",
                             self.gridsUnitCmdBx.currentIndex())
        self.proj.writeEntry("fdt", "gridSquaresMajor",
                             self.gridsMajorSpnBx.value())
        self.proj.writeEntry("fdt", "gridSquaresMinor",
                             self.gridsMinorSpnBx.value())
        self.proj.writeEntry("fdt", "gridsBufferMajor",
                             self.gridsBufferMajor.isChecked())

    def combobox_stylesheet(self, valid):
        return "" if valid else self.parent.badValueLabel

    def validate_pins_combobox(self):
        lyrId = self.pinsCmbBx.itemData(self.pinsCmbBx.currentIndex())
        check = self.parent.valid_pin_layer(lyrId)
        self.pinsLabel.setStyleSheet(self.combobox_stylesheet(check))
        return check

    def validate_grids_combobox(self):
        lyrId = self.gridsCmbBx.itemData(self.gridsCmbBx.currentIndex())
        check = (self.parent.valid_grid_layer(lyrId))
        self.gridsLabel.setStyleSheet(self.combobox_stylesheet(check))
        return check

    def validate_features_combobox(self):
        lyrId = self.featuresCmbBx.itemData(self.featuresCmbBx.currentIndex())
        check = (self.parent.valid_feature_layer(lyrId))
        self.featuresLabel.setStyleSheet(self.combobox_stylesheet(check))
        return check

    def validate_sketch_combobox(self):
        lyrId = self.sketchCmbBx.itemData(self.sketchCmbBx.currentIndex())
        check = (self.parent.valid_sketch_layer(lyrId))
        self.sketchLabel.setStyleSheet(self.combobox_stylesheet(check))
        return check

    def check_layer_comboboxes(self):
        return (
            self.validate_pins_combobox() and
            self.validate_grids_combobox() and
            self.validate_features_combobox() and
            self.validate_sketch_combobox()
        )

    def check_grid_squares(self):
        check = self.parent.valid_squares(self.gridsMajorSpnBx.value(),
                                          self.gridsMinorSpnBx.value())
        ss = "" if check else self.parent.badSpinBoxValue
        self.gridsMajorSpnBx.setStyleSheet(ss)
        self.gridsMinorSpnBx.setStyleSheet(ss)
        return check

    def check_values(self):
        return self.check_grid_squares() and self.check_layer_comboboxes()

    @pyqtSlot(QAbstractButton)
    def dialog_action(self, btn):
        if btn == self.buttonBox.button(QDialogButtonBox.Ok):
            if self.check_values():
                self.save_values()
                self.accept()
        elif btn == self.buttonBox.button(QDialogButtonBox.Reset):
            self.init_values()
        else:
            self.save_geometry()
            self.reject()


if __name__ == "__main__":
    pass
