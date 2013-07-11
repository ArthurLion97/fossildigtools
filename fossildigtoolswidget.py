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
from Ui_fossildigtoolswidget import Ui_DigToolsWidget


class FossilDigToolsWidget(QWidget):
    def __init__(self, parent, iface, settings):
        QWidget.__init__(self, parent)
        self.iface = iface
        self.msgbar = self.iface.messageBar()
        self.settings = settings

        # set up the user interface from Designer.
        self.ui = Ui_DigToolsWidget()
        self.ui.setupUi(self)

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

    @pyqtSlot()
    def on_openFormBtn_clicked(self):
        for f in self.selected_features():
            self.iface.openFeatureForm(self.iface.activeLayer(), f)

    @pyqtSlot(QAbstractButton)
    def on_addGridRadioGrp_buttonClicked(self, btn):
        self.reset_add_grid_btns()
        origin = False
        if btn is self.ui.addGridGridRadio:
            self.ui.addGridLabel.setPixmap(QPixmap(":/plugins/fossildigtools/icons/grid.png"))
        elif btn is self.ui.addGridOriginRadio:
            self.ui.addGridLabel.setPixmap(QPixmap(":/plugins/fossildigtools/icons/origin.png"))
            origin = True
        self.set_grid_btns(origin)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    toolwidget = FossilDigToolsWidget()
    toolwidget.show()
    toolwidget.raise_()
    toolwidget.activateWindow()
    sys.exit(app.exec_())
