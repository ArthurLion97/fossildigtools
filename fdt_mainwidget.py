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
from Ui_fdt_mainwidget import Ui_MainWidget
from fdt_settingsdlg import FdtSettingsDialog


class FdtMainWidget(QWidget):
    def __init__(self, parent, iface, settings):
        QWidget.__init__(self, parent)
        self.iface = iface
        self.msgbar = self.iface.messageBar()
        self.settings = settings
        self.qgsettings = QSettings()

        # set up the user interface from Designer.
        self.ui = Ui_MainWidget()
        self.ui.setupUi(self)

        # setup toolbar
        self.tb = QToolBar(self)
        self.tb.setOrientation(Qt.Horizontal)
        self.tb.setMovable(False)
        self.tb.setFloatable(False)
        self.tb.setFocusPolicy(Qt.NoFocus)
        self.tb.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.tb.setLayoutDirection(Qt.LeftToRight)
        self.tb.setIconSize(QSize(20, 20))
        self.ui.toolBarFrameLayout.addWidget(self.tb)

        self.setupToolbar()

        # set collapsible groupboxes settings property
        for gpbx in self.findChildren(QgsCollapsibleGroupBox):
            gpbx.setSettingGroup("digtools")
            gpbx.setSettings(settings)

        self.ui.addGridBtnGrp.setExclusive(False)
        self.set_grid_btns(True)  # default to origin

        # restore current tab
        curtab = self.settings.value("currentTab", 0, type=int)
        if not (curtab + 1) > self.ui.tabWidget.count():
            self.ui.tabWidget.setCurrentIndex(curtab)

        self.checkPluginReady()

    def setupToolbar(self):
        self.pinPlotAct = QAction(
            QIcon(":/plugins/fossildigtools/icons/pinplot.svg"),
            '', self)
        self.pinPlotAct.setToolTip(self.tr('Plot point from pins'))
        self.tb.addAction(self.pinPlotAct)


        spacer = QWidget(self);
        spacer.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Preferred);
        self.tb.addWidget(spacer);

        self.settingsAct = QAction(
            QIcon(":/plugins/fossildigtools/icons/settings.svg"),
            '', self)
        self.settingsAct.setToolTip(self.tr('Settings'))
        self.settingsAct.triggered.connect(self.openSettingsDialog)
        self.tb.addAction(self.settingsAct)

    def valid_bone_layer(self):
        avl = self.iface.activeLayer()
        if not avl:
           self.msg_bar(self.tr("No active layer"), QgsMessageBar.INFO)
           return False
        if avl.name() != u'Bones_view':
           self.msg_bar(self.tr("Active layer not 'Bones_view'"), QgsMessageBar.INFO)
           return False
        return True

    def selected_features(self):
        ids = []
        if not self.valid_bone_layer():
            return ids
        fids = self.iface.activeLayer().selectedFeatures()
        if not fids:
            self.msg_bar(self.tr("Nothing selected"), QgsMessageBar.INFO)
        return fids

    def msg_bar(self, msg, kind):
        self.msgbar.pushMessage(self.tr( "Fossil Dig Tools" ),
                                msg,
                                kind,
                                self.iface.messageTimeout())

    def reset_add_grid_btns(self):
        for btn in self.ui.addGridBtnGrp.buttons():
            btn.setEnabled(True)
            if btn.isCheckable():
                btn.setChecked(False)

    def set_grid_btns(self, origin=False):
        if origin:
            self.ui.addGridNBtn.setEnabled(False)
            self.ui.addGridSBtn.setEnabled(False)
            self.ui.addGridWBtn.setEnabled(False)
            self.ui.addGridEBtn.setEnabled(False)

    def squaresCheck(self, major, minor):
        if (major == 0 or
            minor == 0 or
            major < minor or
            major%minor != 0):
            return False
        return True

    def checkGridSquares(self):
        majSq = self.settings.value("gridSquaresMajor", 0, type=int)
        minSq = self.settings.value("gridSquaresMinor", 0, type=int)
        return self.squaresCheck(majSq, minSq)

    def checkPluginReady(self):
        checks = (self.checkGridSquares())
        self.ui.tabWidget.setEnabled(checks)
        for act in self.tb.actions():
            if act != self.settingsAct:
                act.setEnabled(checks)

    @pyqtSlot()
    def on_attributesOpenFormBtn_clicked(self):
        for f in self.selected_features():
            self.iface.openFeatureForm(self.iface.activeLayer(), f)

    @pyqtSlot(QAbstractButton)
    def on_addGridRadioGrp_buttonClicked(self, btn):
        self.reset_add_grid_btns()
        origin = False
        if btn is self.ui.addGridGridRadio:
            self.ui.addGridIconLabel.setPixmap(QPixmap(":/plugins/fossildigtools/icons/grid.svg"))
        elif btn is self.ui.addGridOriginRadio:
            self.ui.addGridIconLabel.setPixmap(QPixmap(":/plugins/fossildigtools/icons/origin.svg"))
            origin = True
        self.set_grid_btns(origin)

    def openSettingsDialog(self):
        settingsDlg = FdtSettingsDialog(self, self.iface, self.settings)
        settingsDlg.exec_()
        self.checkPluginReady()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    toolwidget = FdtMainWidget()
    toolwidget.show()
    toolwidget.raise_()
    toolwidget.activateWindow()
    sys.exit(app.exec_())
