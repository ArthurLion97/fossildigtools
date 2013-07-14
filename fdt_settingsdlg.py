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

        # set up the user interface from Designer.
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)

        self.ui.buttonBox.clicked[QAbstractButton].connect(self.dialogAction)

        self.initValues()

        self.ui.gridsMajorSpnBx.valueChanged[int].connect(self.checkGridSquares)
        self.ui.gridsMinorSpnBx.valueChanged[int].connect(self.checkGridSquares)
        self.checkGridSquares()

    def initValues(self):
        self.ui.gridsUnitCmdBx.setCurrentIndex(self.settings.value("gridSquaresUnit", 0, type=int))
        self.ui.gridsMajorSpnBx.setValue(self.settings.value("gridSquaresMajor", 0, type=int))
        self.ui.gridsMinorSpnBx.setValue(self.settings.value("gridSquaresMinor", 0, type=int))

    def saveValues(self):
        self.settings.setValue("gridSquaresUnit", self.ui.gridsUnitCmdBx.currentIndex())
        self.settings.setValue("gridSquaresMajor", self.ui.gridsMajorSpnBx.value())
        self.settings.setValue("gridSquaresMinor", self.ui.gridsMinorSpnBx.value())

    def checkGridSquares(self):
        gridCheck = self.parent.squaresCheck(self.ui.gridsMajorSpnBx.value(),
                                             self.ui.gridsMinorSpnBx.value())
        ss = "" if gridCheck else "QSpinBox {background-color: rgb(255, 210, 208);}"
        self.ui.gridsMajorSpnBx.setStyleSheet(ss)
        self.ui.gridsMinorSpnBx.setStyleSheet(ss)
        return gridCheck

    def checkValues(self):
        if not self.checkGridSquares():
            return False
        return True

    @pyqtSlot(QAbstractButton)
    def dialogAction(self, btn):
        if btn == self.ui.buttonBox.button(QDialogButtonBox.Ok):
            if self.checkValues():
                self.saveValues()
                self.accept()
        elif btn == self.ui.buttonBox.button(QDialogButtonBox.Reset):
            self.initValues()
        else:
            self.reject()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    settingsDlg = FdtSettingsDialog()
    settingsDlg.show()
    settingsDlg.raise_()
    settingsDlg.activateWindow()
    sys.exit(app.exec_())
