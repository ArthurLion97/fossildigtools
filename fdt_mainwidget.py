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
from fdt_pindlg import FdtPinDialog


class FdtMainWidget(QWidget):
    def __init__(self, parent, iface, settings):
        QWidget.__init__(self, parent)
        self.iface = iface
        self.msgbar = self.iface.messageBar()
        self.settings = settings
        self.qgsettings = QSettings()
        self.proj = QgsProject.instance()
        self.splayers = {}

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

        self.setup_toolbar()

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

        self.check_plugin_ready()

        #reference to the canvas
        self.canvas = self.iface.mapCanvas()

        #point tool
        self.pointTool = QgsMapToolEmitPoint(self.canvas)

        QgsMapLayerRegistry.instance().layersAdded.connect(self.check_plugin_ready)
        QgsMapLayerRegistry.instance().layersWillBeRemoved.connect(self.check_plugin_ready)

    def setup_toolbar(self):
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
        self.settingsAct.triggered.connect(self.open_settings_dlg)
        self.tb.addAction(self.settingsAct)

    def spatialite_layers_dict(self):
        lyrdict = {}
        lyrMap = QgsMapLayerRegistry.instance().mapLayers()
        for lyrid, layer in lyrMap.iteritems():
            if (layer.type() == QgsMapLayer.VectorLayer and
                layer.dataProvider().storageType().lower().find("spatialite") > -1):
                lyrdict[lyrid] = layer
        return lyrdict

    def get_layer(self, id):
        return QgsMapLayerRegistry.instance().mapLayer(id)

    def pin_layer_id(self):
        return self.proj.readEntry("fdt", "pinsLayerId", "")[0]

    def grids_layer_id(self):
        return self.proj.readEntry("fdt", "gridsLayerId", "")[0]

    def features_layer_id(self):
        return self.proj.readEntry("fdt", "featuresLayerId", "")[0]

    def valid_layer_attributes(self, lyr, attrs):
        flds = lyr.pendingFields()
        for attr in attrs:
            if flds.indexFromName(attr) == -1:
                return False
        return True

    def valid_pin_layer(self, id=None):
        if id == "invalid":
            return False
        lyrId = id if id else self.pin_layer_id()
        if lyrId == "" or lyrId not in self.splayers:
            return False
        lyr = self.get_layer(lyrId)
        if lyr.geometryType() != QGis.Point:
            return False
        attrs = ['kind', 'name', 'date', 'setter', 'description', 'origin']
        return self.valid_layer_attributes(lyr, attrs)

    def valid_grid_layer(self, id=""):
        return True

#        lyrId = self.grids_layer_id()
#        if lyrId == "" or lyrId not in self.splayers:
#            return False
#        attrs = ['name']
#        return self.valid_layer_attributes(lyrId, attrs)

    def valid_feature_layer(self, id=""):
        return True

#        lyrId = self.features_layer_id()
#        if lyrId == "" or lyrId not in self.splayers:
#            return False
#        attrs = ['name']
#        return self.valid_layer_attributes(lyrId, attrs)

    def layers_added(self, ids):
        pass

    def layers_removed(self, ids):
        pass

    def check_linked_layers(self):
        return (self.valid_pin_layer() and
                self.valid_grid_layer() and
                self.valid_feature_layer())

    def valid_squares(self, major, minor):
        if (major == 0 or
            minor == 0 or
            major < minor or
            major%minor != 0):
            return False
        return True

    def check_grid_squares(self):
        majSq = self.proj.readNumEntry("fdt", "gridSquaresMajor", 0)[0]
        minSq = self.proj.readNumEntry("fdt", "gridSquaresMinor", 0)[0]
        return self.valid_squares(majSq, minSq)

    def check_plugin_ready(self):
        self.splayers = self.spatialite_layers_dict()

        spLyrs = "Spatialite layers\n"
        for lyrid, lyr in self.splayers.iteritems():
            spLyrs += "  Name: {0}\n  Id: {1}\n\n".format(lyr.name(), lyrid)
        QgsMessageLog.logMessage(spLyrs, self.tr("Fdt"), QgsMessageLog.INFO)

        checks = (self.check_grid_squares() and
                  self.check_linked_layers())

        self.ui.tabWidget.setEnabled(checks)
        for act in self.tb.actions():
            if act != self.settingsAct:
                act.setEnabled(checks)

    def active_feature_layer(self):
        avl = self.iface.activeLayer()
        if not avl:
           self.msg_bar(self.tr("No active layer"), QgsMessageBar.INFO)
           return False
        if avl.id() != self.features_layer_id():
           self.msg_bar(self.tr("Features layer not active"), QgsMessageBar.INFO)
           return False
        return True

    def selected_features(self):
        ids = []
        if not self.active_feature_layer():
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

    def open_settings_dlg(self):
        settingsDlg = FdtSettingsDialog(self, self.iface, self.settings)
        settingsDlg.exec_()
        self.check_plugin_ready()

    @pyqtSlot()
    def on_originPinAddBtn_clicked(self):
        addPinDlg = FdtPinDialog(self, self.iface, 'origin')
        addPinDlg.show()

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    toolwidget = FdtMainWidget()
    toolwidget.show()
    toolwidget.raise_()
    toolwidget.activateWindow()
    sys.exit(app.exec_())
