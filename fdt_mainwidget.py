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

PYDEV_DIR = '/Users/larrys/QGIS/PluginProjects/fossildigtools/pydev'
if not PYDEV_DIR in sys.path:
    sys.path.insert(2, PYDEV_DIR)
import pydevd

class FdtMainWidget(QWidget):
    def __init__(self, parent, iface, settings):
        QWidget.__init__(self, parent)
        self.iface = iface
        self.msgbar = self.iface.messageBar()
        self.settings = settings
        self.qgsettings = QSettings()
        self.proj = QgsProject.instance()
        self.splayers = {}
        self.active = False
        self.curorigin = ''
        self.datadelim = '|'
        self.init_bad_value_stylesheets()

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

        # reference to the canvas
        self.canvas = self.iface.mapCanvas()

        # point tool
        self.pointTool = QgsMapToolEmitPoint(self.canvas)

        self.init_spatialite_layers()
        self.check_plugin_ready()

        # track projects and layer changes
        self.iface.projectRead.connect(self.check_plugin_ready)
        self.iface.newProjectCreated.connect(self.invalid_project)

        QgsMapLayerRegistry.instance().layersAdded["QList<QgsMapLayer *>"].connect(self.layers_added)
        QgsMapLayerRegistry.instance().layersWillBeRemoved["QStringList"].connect(self.layers_to_be_removed)

    def pydev(self):
        pydevd.settrace('localhost', port=53100, stdoutToServer=True, stderrToServer=True)

    def setup_toolbar(self):
        self.pinPlotAct = QAction(
            QIcon(":/plugins/fossildigtools/icons/pinplot.svg"),
            '', self)
        self.pinPlotAct.setToolTip(self.tr('Plot point from pins'))
        self.tb.addAction(self.pinPlotAct)


        spacer = QWidget(self)
        spacer.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Preferred)
        self.tb.addWidget(spacer)

        self.settingsAct = QAction(
            QIcon(":/plugins/fossildigtools/icons/settings.svg"),
            '', self)
        self.settingsAct.setToolTip(self.tr('Settings'))
        self.settingsAct.triggered.connect(self.open_settings_dlg)
        self.tb.addAction(self.settingsAct)

    def is_spatialite_layer(self, layer):
        return (layer.type() == QgsMapLayer.VectorLayer and
                layer.storageType().lower().find("spatialite") > -1)

    def spatialite_layers_dict(self):
        lyrdict = {}
        lyrMap = QgsMapLayerRegistry.instance().mapLayers()
        for lyrid, layer in lyrMap.iteritems():
            if self.is_spatialite_layer(layer):
                lyrdict[lyrid] = layer
        return lyrdict

    def init_spatialite_layers(self):
        self.splayers = self.spatialite_layers_dict()

    def split_data(self, data):
        return data.split(self.datadelim)

    def join_data(self, a, b):
        return "{0}{1}{2}".format(a, self.datadelim, b)

    def get_layer(self, layerid):
        return QgsMapLayerRegistry.instance().mapLayer(layerid)

    def get_feature(self, layerid, featid):
        layer = self.get_layer(str(layerid))
        req = QgsFeatureRequest().setFilterFid(int(featid))
        feat = QgsFeature()
        layer.getFeatures(req).nextFeature(feat)
        return feat

    def get_features(self, layer, expstr):
        exp = QgsExpression(expstr)
        fields = layer.pendingFields()
        exp.prepare(fields)

        # # works
        # feats = []
        # for feat in layer.getFeatures():
        #     # err = exp.evalErrorString()
        #     if exp.evaluate(feat):
        #         feats.append(feat)
        #
        # # doesn't work!!
        # fit = layer.getFeatures()
        # feat = QgsFeature()
        # while fit.nextFeature(feat):
        #     if exp.evaluate(feat) == 1:
        #         feats.append(feat)
        # fit.close()
        # return feats

        return filter(exp.evaluate, layer.getFeatures())

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

    def valid_pin_layer(self, lid=None):
        if id == "invalid":
            return False
        lyrId = lid if lid else self.pin_layer_id()
        if lyrId == "" or lyrId not in self.splayers:
            return False
        lyr = self.get_layer(lyrId)
        if lyr.geometryType() != QGis.Point:
            return False
        attrs = ['pkuid', 'kind', 'name', 'date', 'setter', 'description', 'origin']
        return self.valid_layer_attributes(lyr, attrs)

    def valid_grid_layer(self, lid=None):
        return True

#        lyrId = self.grids_layer_id()

    def valid_feature_layer(self, lid=None):
        return True

#        lyrId = self.features_layer_id()

    @pyqtSlot("QList<QgsMapLayer *>")
    def layers_added(self, layers):
        check = False
        for layer in layers:
            if self.is_spatialite_layer(layer):
                self.splayers[layer.id()] = layer
                check = True
        if check:
            self.check_plugin_ready()

    @pyqtSlot("QStringList")
    def layers_to_be_removed(self, lids):
        check = False
        for lid in lids:
            if self.splayers.has_key(lid):
                del self.splayers[lid]
                check = True
        if check:
            self.check_plugin_ready()

    def check_linked_layers(self):
        return (self.valid_pin_layer() and
                self.valid_grid_layer() and
                self.valid_feature_layer())

    def valid_squares(self, major, minor):
        if (major == 0 or minor == 0 or major < minor or major % minor != 0):
            return False
        return True

    def check_grid_squares(self):
        majSq = self.proj.readNumEntry("fdt", "gridSquaresMajor", 0)[0]
        minSq = self.proj.readNumEntry("fdt", "gridSquaresMinor", 0)[0]
        return self.valid_squares(majSq, minSq)

    @pyqtSlot()
    def check_plugin_ready(self):
        # log splayers
        spLyrs = "Spatialite layers\n"
        for lyrid, lyr in self.splayers.iteritems():
            spLyrs += "  Name: {0}\n  Id: {1}\n\n".format(lyr.name(), lyrid)
        QgsMessageLog.logMessage(spLyrs, self.tr("Fdt"), QgsMessageLog.INFO)

        checks = (self.check_grid_squares() and
                  self.check_linked_layers())
        if checks:
            self.enable_plugin(True)
            self.init_plugin()
            self.clear_notice()
        else:
            self.invalid_project()

    def enable_plugin(self, enable):
        self.ui.tabWidget.setEnabled(enable)
        for act in self.tb.actions():
            if act != self.settingsAct:
                act.setEnabled(enable)

    @pyqtSlot()
    def invalid_project(self):
        self.active = False
        self.clear_plugin()
        self.enable_plugin(False)

    def clear_plugin(self):
        if not self.active:
            self.notice(self.tr("Project unsupported. Define settings."))
        # location pins
        self.ui.originPinCmbBx.clear()
        self.ui.originEditFrame.setEnabled(False)
        self.ui.directPinList.clear()
        self.ui.directPinFrame.setEnabled(False)
        self.ui.directPinEditFrame.setEnabled(False)
        # grids
        self.ui.gridsCmbBx.clear()
        self.ui.gridsRemoveBtn.setEnabled(False)
        self.ui.gridFrame.setEnabled(False)

    def init_plugin(self):
        if self.active:
            return
        self.active = True
        self.load_pins()

    @pyqtSlot()
    def load_pins(self):
        if not self.active:
            return

        self.clear_plugin()

        # load origins
        self.load_origin_pins()
        if self.ui.originPinCmbBx.count() > 0:
            self.curorigin = self.ui.originPinCmbBx.itemData(
                             self.ui.originPinCmbBx.currentIndex())
            # load directional pins associated with the current origin
            self.load_directional_pins()
            # load grids associated with the current origin
            self.load_origin_grids()

    def current_origin(self):
        return self.split_data(self.curorigin)[1]

    def current_origin_fid(self):
        return self.split_data(self.curorigin)[0]

    def current_origin_feat(self):
        #self.pydev()
        return self.get_feature(self.pin_layer_id(), self.current_origin_fid())

    def origin_pins(self):
        expstr = " \"kind\"='origin' "
        layer = self.get_layer(self.pin_layer_id())
        return self.get_features(layer, expstr)

    def load_origin_pins(self):
        self.ui.originPinCmbBx.clear()
        pins = self.origin_pins()
        haspins = len(pins) > 0
        if haspins:
            self.ui.originEditFrame.setEnabled(True)
            self.ui.originPinCmbBx.blockSignals(True)
            for pin in pins:
                self.ui.originPinCmbBx.addItem(
                    pin['name'], self.join_data(pin.id(), pin['pkuid']))
            self.ui.originPinCmbBx.blockSignals(False)

        self.ui.directPinFrame.setEnabled(haspins)

    def directional_pins(self, origin=-1):
        if origin == -1:
            origin = self.current_origin()
        if origin == -1:
            return
        expstr = " \"kind\"='directional' AND \"origin\"={0} ".format(origin)
        layer = self.get_layer(self.pin_layer_id())
        return self.get_features(layer, expstr)

    def load_directional_pins(self):
        self.ui.directPinList.clear()
        pins = self.directional_pins(self.current_origin())
        haspins = len(pins) > 0
        if haspins:
            self.ui.directPinList.blockSignals(True)
            for pin in pins:
                lw = QListWidgetItem(pin['name'])
                lw.setData(Qt.UserRole, self.join_data(pin.id(), pin['pkuid']))
                self.ui.directPinList.addItem(lw)
            self.ui.directPinList.blockSignals(False)

    def origin_grids(self, origin=-1):
        pass

    def load_origin_grids(self):
        pass

    def init_bad_value_stylesheets(self):
        self.badLineEditValue = \
            "QLineEdit {background-color: rgb(255, 210, 208);}"
        self.badSpinBoxValue = \
            "QSpinBox {background-color: rgb(255, 210, 208);}"
        self.badDblSpinBoxValue = \
            "QDoubleSpinBox {background-color: rgb(255, 210, 208);}"
        self.badValueLabel = "QLabel {color: rgb(225, 0, 0);}"

    def active_feature_layer(self):
        avl = self.iface.activeLayer()
        if not avl:
            self.msg_bar(self.tr("No active layer"),
                         QgsMessageBar.INFO)
            return False
        if avl.id() != self.features_layer_id():
            self.msg_bar(self.tr("Features layer not active"),
                         QgsMessageBar.INFO)
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

    def notice(self, notice):
        self.ui.noticeLabel.show()
        self.ui.noticeLabel.setText(notice)

    def clear_notice(self):
        self.ui.noticeLabel.setText("")
        self.ui.noticeLabel.hide()

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
        pinDlg = FdtPinDialog(self, self.iface, 'origin')
        pinDlg.accepted.connect(self.load_pins)
        pinDlg.show()

    @pyqtSlot()
    def on_originPinEditBtn_clicked(self):
        feat = self.current_origin_feat()
        if feat.isValid():
            pinDlg = FdtPinDialog(self, self.iface, 'origin', -1, feat)
            pinDlg.accepted.connect(self.load_pins)
            pinDlg.show()

    @pyqtSlot()
    def on_attributesOpenFormBtn_clicked(self):
        for f in self.selected_features():
            self.iface.openFeatureForm(self.iface.activeLayer(), f)

    @pyqtSlot(QAbstractButton)
    def on_addGridRadioGrp_buttonClicked(self, btn):
        self.reset_add_grid_btns()
        origin = False
        if btn is self.ui.addGridGridRadio:
            self.ui.addGridIconLabel.setPixmap(
                QPixmap(":/plugins/fossildigtools/icons/grid.svg"))
        elif btn is self.ui.addGridOriginRadio:
            self.ui.addGridIconLabel.setPixmap(
                QPixmap(":/plugins/fossildigtools/icons/origin.svg"))
            origin = True
        self.set_grid_btns(origin)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    toolwidget = FdtMainWidget()
    toolwidget.show()
    toolwidget.raise_()
    toolwidget.activateWindow()
    sys.exit(app.exec_())
