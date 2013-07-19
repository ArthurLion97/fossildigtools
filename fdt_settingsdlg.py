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
from Ui_fdt_settingsdlg import Ui_SettingsDialog


class FdtSettingsDialog(QDialog):
    def __init__(self, parent, iface, settings):
        QDialog.__init__(self, parent)
        self.parent = parent
        self.iface = iface
        self.settings = settings
        self.qgsettings = QSettings()
        self.proj = QgsProject.instance()

        # set up the user interface from Designer.
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)

        self.lyrCmbxs = [self.ui.pinsCmbBx,
                         self.ui.gridsCmbBx,
                         self.ui.featuresCmbBx]
        self.ui.pinsCmbBx.currentIndexChanged[int].\
            connect(self.validate_pins_combobox)
        self.ui.gridsCmbBx.currentIndexChanged[int].\
            connect(self.validate_grids_combobox)
        self.ui.featuresCmbBx.currentIndexChanged[int].\
            connect(self.validate_features_combobox)

        self.populate_comboboxes()

        self.ui.gridsMajorSpnBx.valueChanged[int].\
            connect(self.check_grid_squares)
        self.ui.gridsMinorSpnBx.valueChanged[int].\
            connect(self.check_grid_squares)

        self.init_values()

        self.check_layer_comboboxes()
        self.check_grid_squares()

        self.ui.buttonBox.clicked[QAbstractButton].connect(self.dialog_action)

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
        self.ui.pinsCmbBx.setCurrentIndex(
            self.ui.pinsCmbBx.findData(self.parent.pin_layer_id()))
        self.ui.gridsCmbBx.setCurrentIndex(
            self.ui.gridsCmbBx.findData(self.parent.grid_layer_id()))
        self.ui.featuresCmbBx.setCurrentIndex(
            self.ui.featuresCmbBx.findData(self.parent.feature_layer_id()))

        self.ui.gridsUnitCmdBx.setCurrentIndex(self.parent.grid_unit_index())
        self.ui.gridsMajorSpnBx.setValue(self.parent.major_grid())
        self.ui.gridsMinorSpnBx.setValue(self.parent.minor_grid())

    def save_values(self):
        # store values in project
        self.proj.writeEntry("fdt", "pinsLayerId",
            self.ui.pinsCmbBx.itemData(self.ui.pinsCmbBx.currentIndex()))
        self.proj.writeEntry("fdt", "gridsLayerId",
            self.ui.gridsCmbBx.itemData(self.ui.gridsCmbBx.currentIndex()))
        self.proj.writeEntry("fdt", "featuresLayerId",
            self.ui.featuresCmbBx.itemData(
                self.ui.featuresCmbBx.currentIndex()))

        self.proj.writeEntry("fdt", "gridSquaresUnit",
                             self.ui.gridsUnitCmdBx.currentIndex())
        self.proj.writeEntry("fdt", "gridSquaresMajor",
                             self.ui.gridsMajorSpnBx.value())
        self.proj.writeEntry("fdt", "gridSquaresMinor",
                             self.ui.gridsMinorSpnBx.value())

    def combobox_stylesheet(self, valid):
        return "" if valid else self.parent.badValueLabel

    def validate_pins_combobox(self):
        lyrId = self.ui.pinsCmbBx.itemData(self.ui.pinsCmbBx.currentIndex())
        check = self.parent.valid_pin_layer(lyrId)
        self.ui.pinsLabel.setStyleSheet(self.combobox_stylesheet(check))
        return check

    def validate_grids_combobox(self):
        lyrId = self.ui.gridsCmbBx.itemData(self.ui.gridsCmbBx.currentIndex())
        check = (self.parent.valid_grid_layer(lyrId))
        self.ui.gridsLabel.setStyleSheet(self.combobox_stylesheet(check))
        return check

    def validate_features_combobox(self):
        lyrId = self.ui.featuresCmbBx.itemData(
            self.ui.featuresCmbBx.currentIndex())
        check = (self.parent.valid_feature_layer(lyrId))
        self.ui.featuresLabel.setStyleSheet(self.combobox_stylesheet(check))
        return check

    def check_layer_comboboxes(self):
        return (self.validate_pins_combobox() and
                self.validate_grids_combobox() and
                self.validate_features_combobox())

    def check_grid_squares(self):
        check = self.parent.valid_squares(self.ui.gridsMajorSpnBx.value(),
                                          self.ui.gridsMinorSpnBx.value())
        ss = "" if check else self.parent.badSpinBoxValue
        self.ui.gridsMajorSpnBx.setStyleSheet(ss)
        self.ui.gridsMinorSpnBx.setStyleSheet(ss)
        return check

    def check_values(self):
        return (self.check_grid_squares() and
                self.check_layer_comboboxes())

    @pyqtSlot(QAbstractButton)
    def dialog_action(self, btn):
        if btn == self.ui.buttonBox.button(QDialogButtonBox.Ok):
            if self.check_values():
                self.save_values()
                self.accept()
        elif btn == self.ui.buttonBox.button(QDialogButtonBox.Reset):
            self.init_values()
        else:
            self.save_geometry()
            self.reject()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    settingsDlg = FdtSettingsDialog()
    settingsDlg.show()
    settingsDlg.raise_()
    settingsDlg.activateWindow()
    sys.exit(app.exec_())
