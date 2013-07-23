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
import math
from itertools import ifilter
from operator import itemgetter

from qgis.core import *
from qgis.gui import *
from query import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Ui_fdt_mainwidget import Ui_MainWidget
from fdt_settingsdlg import FdtSettingsDialog
from fdt_pindlg import FdtPinDialog

PYDEV_DIR = '/Users/larrys/QGIS/PluginProjects/fossildigtools/pydev'
if not PYDEV_DIR in sys.path:
    sys.path.insert(2, PYDEV_DIR)
import pydevd


class FdtMainWidget(QWidget, Ui_MainWidget):

    def __init__(self, parent, iface, settings):
        QWidget.__init__(self, parent)
        self.iface = iface
        self.msgbar = self.iface.messageBar()
        self.settings = settings
        self.qgsettings = QSettings()
        self.proj = QgsProject.instance()
        self.splayers = {}
        self.active = False
        self.datadelim = '|'
        self.curorigin = "{0}{1}{0}".format("-1", self.datadelim)
        self.curorigintxt = ""
        self.curgrid = "{0}{1}{0}".format("-1", self.datadelim)
        self.layerconections = False
        self.init_bad_value_stylesheets()

        self.redhlcolor = QColor(225, 0, 0)
        self.bluehlcolor = QColor(0, 0, 225)
        self.circlesegments = 32
        self.removehighlightsmilli = 2000
        self.highlights = []

        # set up the user interface from Designer.
        # self.ui = Ui_MainWidget()
        self.setupUi(self)

        # setup toolbar
        self.tb = QToolBar(self)
        self.tb.setOrientation(Qt.Horizontal)
        self.tb.setMovable(False)
        self.tb.setFloatable(False)
        self.tb.setFocusPolicy(Qt.NoFocus)
        self.tb.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.tb.setLayoutDirection(Qt.LeftToRight)
        self.tb.setIconSize(QSize(20, 20))
        self.toolBarFrameLayout.addWidget(self.tb)

        self.setup_toolbar()

        # set collapsible groupboxes settings property
        for gpbx in self.findChildren(QgsCollapsibleGroupBox):
            gpbx.setSettingGroup("digtools")
            gpbx.setSettings(settings)

        self.addGridBtnGrp.setExclusive(False)
        self.set_grid_btns(True)  # default to origin

        # restore current tab
        curtab = self.settings.value("currentTab", 0, type=int)
        if not (curtab + 1) > self.tabWidget.count():
            self.tabWidget.setCurrentIndex(curtab)

        # reference to the canvas
        self.canvas = self.iface.mapCanvas()

        # point tool
        self.pointTool = QgsMapToolEmitPoint(self.canvas)

        self.init_spatialite_layers()
        self.check_plugin_ready()

        # track projects and layer changes
        self.iface.projectRead.connect(self.check_plugin_ready)
        self.iface.newProjectCreated.connect(self.invalid_project)

        # ensure any highlights are removed on subsequent refreshes
        self.canvas.mapCanvasRefreshed.connect(self.delete_highlights)

        QgsMapLayerRegistry.instance().layersAdded["QList<QgsMapLayer *>"].\
            connect(self.layers_added)
        QgsMapLayerRegistry.instance().layersWillBeRemoved["QStringList"].\
            connect(self.layers_to_be_removed)

    def pydev(self):
        try:  # or it crashes QGIS if connection to debug server unavailable
            pydevd.settrace('localhost',
                            port=53100,
                            stdoutToServer=True,
                            stderrToServer=True)
        except:
            pass

    def setup_toolbar(self):
        self.zoomGridsAct = QAction(
            QIcon(":/plugins/fossildigtools/icons/zoom-grids.svg"),
            '', self)
        self.zoomGridsAct.setToolTip(self.tr('Zoom to grids extent'))
        self.zoomGridsAct.triggered.connect(self.on_gridsZoomToAllBtn_clicked)
        self.tb.addAction(self.zoomGridsAct)

        self.zoomInAct = QAction(
            QIcon(":/plugins/fossildigtools/icons/zoom-in.svg"),
            '', self)
        self.zoomInAct.setToolTip(self.tr('Zoom in'))
        self.zoomInAct.triggered.connect(self.zoom_in)
        self.tb.addAction(self.zoomInAct)

        self.zoomOutAct = QAction(
            QIcon(":/plugins/fossildigtools/icons/zoom-out.svg"),
            '', self)
        self.zoomOutAct.setToolTip(self.tr('Zoom out'))
        self.zoomOutAct.triggered.connect(self.zoom_out)
        self.tb.addAction(self.zoomOutAct)

        self.distToLocationAct = QAction(
            QIcon(":/plugins/fossildigtools/icons/distance-to-location.svg"),
            '', self)
        self.distToLocationAct.setToolTip(
            self.tr('Calculate distances to map location'))
        self.tb.addAction(self.distToLocationAct)

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
        if not layer:
            return None
        req = QgsFeatureRequest().setFilterFid(featid)
        feat = QgsFeature()
        layer.getFeatures(req).nextFeature(feat)
        return feat

    def get_features(self, layerid, expstr, itr=False):
        layer = self.get_layer(str(layerid))
        if not layer:
            return []
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
        if itr:
            return ifilter(exp.evaluate, layer.getFeatures())
        else:
            return filter(exp.evaluate, layer.getFeatures())

    def get_features_iter(self, layerid, expstr):
        return self.get_features(layerid, expstr, True)

    def get_features_query_iter(self, layerid, expstr):
        layer = self.get_layer(str(layerid))
        if not layer:
            return []
        q = (query(layer).where(expstr))
        return q()

    def delete_feature(self, layerid, featid):
        layer = self.get_layer(layerid)
        if not layer:
            return
        layer.startEditing()
        layer.deleteFeature(featid)
        layer.commitChanges()
        layer.setCacheImage(None)
        layer.triggerRepaint()

    def delete_features(self, layerid, feats):
        # NOTE: does not trigger layer.editingStopped signals
        if not feats:
            return
        layer = self.get_layer(layerid)
        if not layer:
            return

        # trigger gui update manually instead of on layer.editingStopped
        # otherwise, on Mac, cpu maxes out updating the gui many times
        layer.blockSignals(True)
        layer.startEditing()
        layer.beginEditCommand("Delete features")
        for feat in feats:
            layer.deleteFeature(feat.id())
        layer.commitChanges()
        layer.endEditCommand()
        layer.blockSignals(False)
        layer.setCacheImage(None)
        layer.triggerRepaint()

    def delete_features_by_expr(self, layerid, expr):
        # NOTE: does not trigger layer.editingStopped signals
        feats = self.get_features(layerid, expr)  # checks for layer
        if feats:
            self.delete_features(layerid, feats)


    def circle_geometry(self, pt, radius=0, segments=0):
        # radius in mm
        if not radius:
            radius = 5
        ctx = self.canvas.mapRenderer().rendererContext()
        # mm (converted to map pixels, then to meters)
        r = radius * ctx.scaleFactor() * ctx.mapToPixel().mapUnitsPerPixel()
        if not segments:
            segments = self.circlesegments
        pts = []
        for i in range(segments):
            theta = i * (2.0 * math.pi / segments)
            p = QgsPoint(pt.x() + r * math.cos(theta),
                         pt.y() + r * math.sin(theta))
            pts.append(p)
        return QgsGeometry.fromPolygon([pts])

    def add_highlight(self, layerid, geom, color):
        layer = self.get_layer(layerid)
        hl = QgsHighlight(self.canvas, geom, layer)
        self.highlights.append(hl)
        hl.setWidth(0)
        hl.setColor(color)
        hl.show()

    def remove_highlights(self, milliseconds=0):
        if not milliseconds:
            milliseconds = self.removehighlightsmilli
        QTimer.singleShot(milliseconds, self.delete_highlights)

    @pyqtSlot()
    def delete_highlights(self):
        for hl in self.highlights:
            del hl
        self.highlights = []

    def pin_layer_id(self):
        return self.proj.readEntry("fdt", "pinsLayerId", "")[0]

    def grid_layer_id(self):
        return self.proj.readEntry("fdt", "gridsLayerId", "")[0]

    def feature_layer_id(self):
        return self.proj.readEntry("fdt", "featuresLayerId", "")[0]

    def valid_layer_attributes(self, lyr, attrs):
        flds = lyr.pendingFields()
        for attr in attrs:
            if flds.indexFromName(attr) == -1:
                return False
        return True

    def valid_pin_layer(self, lid=None):
        if lid == "invalid":
            return False
        lyrId = lid if lid else self.pin_layer_id()
        if lyrId == "" or lyrId not in self.splayers:
            return False
        layer = self.get_layer(lyrId)
        if layer and layer.geometryType() != QGis.Point:
            return False
        attrs = ['pkuid', 'kind', 'name', 'date',
                 'setter', 'description', 'origin']
        return self.valid_layer_attributes(layer, attrs)

    def valid_grid_layer(self, lid=None):
        if lid == "invalid":
            return False
        lyrId = lid if lid else self.grid_layer_id()
        if lyrId == "" or lyrId not in self.splayers:
            return False
        layer = self.get_layer(lyrId)
        if layer and layer.geometryType() != QGis.Polygon:
            return False
        attrs = ['pkuid', 'kind', 'x', 'y',
                 'minor', 'origin', 'name']
        return self.valid_layer_attributes(layer, attrs)

    def valid_feature_layer(self, lid=None):
        return True

#        lyrId = self.features_layer_id()

    @pyqtSlot("QList<QgsMapLayer *>")
    def layers_added(self, layers):
        check = False
        for layer in layers:
            if self.is_spatialite_layer(layer) and layer not in self.splayers:
                self.splayers[layer.id()] = layer
                check = True
        if check:
            self.check_plugin_ready()

    @pyqtSlot("QStringList")
    def layers_to_be_removed(self, lids):
        check = False
        for lid in lids:
            if lid in self.splayers:
                del self.splayers[lid]
                check = True
        if check:
            self.check_plugin_ready()

    def check_linked_layers(self):
        return (self.valid_pin_layer() and
                self.valid_grid_layer() and
                self.valid_feature_layer())

    def zoom_canvas(self, rect):
        self.canvas.setExtent(rect)
        self.canvas.refresh()

    def zoom_in(self):
        self.canvas.zoomIn()

    def zoom_out(self):
        self.canvas.zoomOut()

    def to_meters(self, size, unit):
        if unit == 'cm':
            return size * 0.01
        elif unit == 'in':
            return size * 0.0254
        elif unit == 'feet' or unit == 'ft':
            return size * 0.3048
        # elif unit == 'meter' or unit == 'm':
        return size

    def grid_unit_index(self):
        return self.proj.readNumEntry("fdt", "gridSquaresUnit", 0)[0]

    def grid_unit(self):
        return 'cm' if self.grid_unit_index() == 0 else 'in'

    def major_grid(self):
        return self.proj.readNumEntry("fdt", "gridSquaresMajor", 0)[0]

    def major_grid_m(self):
        return self.to_meters(self.major_grid(), self.grid_unit())

    def minor_grid(self):
        return self.proj.readNumEntry("fdt", "gridSquaresMinor", 0)[0]

    def minor_grid_m(self):
        return self.to_meters(self.minor_grid(), self.grid_unit())

    def buffer_major_grid(self):
        return bool(self.proj.readNumEntry("fdt", "gridsBufferMajor", 1)[0])

    def major_grid_buf(self):
        buf = (2 * self.minor_grid_m()) if self.buffer_major_grid() else 0
        return self.major_grid_m() + buf

    def rect_buf_point(self, pt, size):
        return QgsRectangle(pt.x() - size / 2, pt.y() - size / 2,
                            pt.x() + size / 2, pt.y() + size / 2,)

    def valid_squares(self, major, minor):
        return (major != 0 and minor != 0 and
                major >= minor and major % minor == 0)

    def check_grid_squares(self):
        return self.valid_squares(self.major_grid(), self.minor_grid())

    @pyqtSlot()
    def check_plugin_ready(self):
        # log splayers
        # spLyrs = "Spatialite layers\n"
        # for lyrid, lyr in self.splayers.iteritems():
        #     spLyrs += "  Name: {0}\n  Id: {1}\n\n".format(lyr.name(), lyrid)
        # QgsMessageLog.logMessage(spLyrs, self.tr("Fdt"), QgsMessageLog.INFO)

        checks = (self.check_grid_squares() and
                  self.check_linked_layers())
        if checks:
            self.enable_plugin(True)
            self.init_plugin()
            self.clear_notice()
        else:
            self.invalid_project()

    @pyqtSlot()
    def invalid_project(self):
        self.active = False  # must come first
        self.remove_layer_connections()
        self.clear_plugin()
        self.enable_plugin(False)

    def init_plugin(self):
        if self.active:
            return
        self.active = True  # must come first
        self.load_pins()
        self.make_layer_connections()

    def clear_plugin(self):
        if not self.active:
            self.notice(self.tr("Project unsupported. Define settings."))
        # location pins
        self.originPinCmbBx.blockSignals(True)
        self.originPinCmbBx.clear()
        self.originPinCmbBx.blockSignals(False)
        self.originEditFrame.setEnabled(False)
        self.directPinList.clear()
        self.directPinFrame.setEnabled(False)
        self.directPinEditFrame.setEnabled(False)
        # grids
        self.gridsCmbBx.blockSignals(True)
        self.gridsCmbBx.clear()
        self.gridsCmbBx.blockSignals(False)
        self.gridsGoToCornerFrame.setEnabled(False)
        self.gridsEditFrame.setEnabled(False)
        self.gridFrame.setEnabled(False)
        self.gridsAllFrame.setEnabled(False)

    def enable_plugin(self, enable):
        self.tabWidget.setEnabled(enable)
        for act in self.tb.actions():
            if act != self.settingsAct:
                act.setEnabled(enable)

    def make_layer_connections(self):
        if self.layerconections:
            return

        actions = {self.pin_layer_id(): self.load_pins,
                   self.grid_layer_id(): self.load_origin_major_grids}
        for layerid, method in actions.iteritems():
            layer = self.get_layer(layerid)
            if layer:
                layer.editingStopped.connect(method)
                layer.updatedFields.connect(self.check_plugin_ready)

        self.layerconections = True

    def remove_layer_connections(self):
        if not self.layerconections:
            return

        actions = {self.pin_layer_id(): self.load_pins,
                   self.grid_layer_id(): self.load_origin_major_grids}
        for layerid, method in actions.iteritems():
            layer = self.get_layer(layerid)
            if layer:
                layer.editingStopped.disconnect(method)
                layer.updatedFields.disconnect(self.check_plugin_ready)

    @pyqtSlot()
    def load_pins(self):
        if not self.active:
            return

        self.clear_plugin()

        # load origins
        self.load_origin_pins()
        self.update_current_origin()
        self.load_origin_children()

    def update_current_origin(self):
        if self.originPinCmbBx.count() > 0:
            self.curorigin = self.originPinCmbBx.itemData(
                self.originPinCmbBx.currentIndex())
            self.curorigintxt = " ({0})".format(
                self.originPinCmbBx.currentText())
        else:
            self.curorigin = "{0}{1}{0}".format("-1", self.datadelim)
            self.curorigintxt = ''

        self.settings.setValue("currentOrigin", self.current_origin())
        self.gridsGrpBx.setTitle(
            "{0}{1}".format(self.tr('Grids'), self.curorigintxt))

    def current_origin(self):  # pkuid
        return self.split_data(self.curorigin)[1]

    def current_origin_fid(self):
        return int(self.split_data(self.curorigin)[0])

    def current_origin_feat(self):
        #self.pydev()
        return self.get_feature(self.pin_layer_id(), self.current_origin_fid())

    def current_origin_point(self):
        feat = self.current_origin_feat()
        return feat.geometry().asPoint()

    def delete_current_origin(self):
        self.delete_feature(self.pin_layer_id(), self.current_origin_fid())

    def origin_pins(self):
        expstr = " \"kind\"='origin' "
        return self.get_features(self.pin_layer_id(), expstr)

    def load_origin_pins(self):
        self.originPinCmbBx.clear()
        pins = self.origin_pins()
        haspins = len(pins) > 0
        if haspins:
            self.originEditFrame.setEnabled(True)
            self.originPinCmbBx.blockSignals(True)
            # sort by pin name
            plist = []
            for p in pins:
                plist.append((p.id(), p['pkuid'], p['name']))
            plist = sorted(plist, key=itemgetter(2))

            curorig = self.settings.value("currentOrigin", "-1", type=str)
            curindx = -1
            for (i, p) in enumerate(plist):
                self.originPinCmbBx.addItem(p[2], self.join_data(p[0], p[1]))
                if curorig != "-1" and curorig == str(p[1]):
                    curindx = i
            if (curindx > -1 and
                    not curindx > (self.originPinCmbBx.count() - 1)):
                self.originPinCmbBx.setCurrentIndex(curindx)

            self.originPinCmbBx.blockSignals(False)

        self.directPinFrame.setEnabled(haspins)

    def load_origin_children(self):
        # load directional pins associated with the current origin
        self.load_directional_pins()
        # load grids associated with the current origin
        self.load_origin_major_grids()

    def current_directional_item(self):
        return self.directPinList.currentItem()

    def current_directional(self):  # pkuid
        return self.split_data(
            self.current_directional_item().data(Qt.UserRole))[1]

    def current_directional_fid(self):
        return int(self.split_data(
            self.current_directional_item().data(Qt.UserRole))[0])

    def current_directional_feat(self):
        #self.pydev()
        return self.get_feature(self.pin_layer_id(),
                                self.current_directional_fid())

    def current_directional_point(self):
        feat = self.current_directional_feat()
        return feat.geometry().asPoint()

    def delete_current_directional(self):
        self.delete_feature(self.pin_layer_id(), self.current_directional_fid())

    def directional_pins(self, origin=-1):
        if origin == -1:
            origin = self.current_origin()
        if origin == -1:
            return []
        expstr = " \"kind\"='directional' AND \"origin\"={0} ".format(origin)
        return self.get_features(self.pin_layer_id(), expstr)

    def load_directional_pins(self):
        self.directPinList.clear()
        self.directPinList.blockSignals(True)
        for pin in self.directional_pins(self.current_origin()):
            lw = QListWidgetItem(pin['name'])
            lw.setData(Qt.UserRole, self.join_data(pin.id(), pin['pkuid']))
            self.directPinList.addItem(lw)
        self.directPinList.blockSignals(False)

    def update_current_grid(self):
        if self.gridsCmbBx.count() > 0:
            self.curgrid = self.gridsCmbBx.itemData(
                self.gridsCmbBx.currentIndex())
        else:
            self.curgrid = "{0}{1}{0}".format("-1", self.datadelim)

        data = self.join_data(self.current_origin(), self.current_grid())
        self.settings.setValue("currentGrid", data)

    def current_grid(self):
        return self.split_data(self.curgrid)[1]  # pkuid

    def current_grid_fid(self):
        return int(self.split_data(self.curgrid)[0])

    def current_grid_feat(self):
        #self.pydev()
        return self.get_feature(self.grid_layer_id(), self.current_grid_fid())

    def current_grid_polygon(self):
        feat = self.current_grid_feat()
        return feat.geometry().asPolygon()

    def current_grid_points(self):
        pts = []
        for i in self.current_grid_polygon():
            for k in i:
                pts.append(QgsPoint(k.x(), k.y()))
        return pts

    def current_grid_rect(self):
        pts = self.current_grid_points()
        return QgsRectangle(pts[0], pts[2])

    def current_grid_center(self):
        return self.current_grid_rect().center()

    def current_grid_ll_point(self):
        rect = self.current_grid_rect()
        return QgsPoint(rect.xMinimum(), rect.yMinimum())

    def current_grid_ul_point(self):
        rect = self.current_grid_rect()
        return QgsPoint(rect.xMinimum(), rect.yMaximum())

    def current_grid_ur_point(self):
        rect = self.current_grid_rect()
        return QgsPoint(rect.xMaximum(), rect.yMaximum())

    def current_grid_lr_point(self):
        rect = self.current_grid_rect()
        return QgsPoint(rect.xMaximum(), rect.yMinimum())

    def zoom_to_corner_pt(self, pt):
        rect = self.rect_buf_point(pt, self.minor_grid_m())
        self.zoom_canvas(rect)

    def delete_current_grid(self):
        # find/delete both major and minor grids for same location
        xyloc = self.grid_xyloc_from_origin(self.current_grid_center())
        expstr = ' "x"={0} and "y"={1} and "origin"={2} '. \
            format(xyloc[0], xyloc[1], self.current_origin())
        self.delete_features_by_expr(self.grid_layer_id(), expstr)
        self.load_origin_major_grids()

    def origin_has_grids(self):
        # find both major and minor grids for current origin
        expstr = ' "origin"={0} '.format(self.current_origin())
        feats = self.get_features(self.grid_layer_id(), expstr)
        return len(feats) > 0

    def delete_all_origin_grids(self):
        # find/delete both major and minor grids for current origin
        expstr = ' "origin"={0} '.format(self.current_origin())
        self.delete_features_by_expr(self.grid_layer_id(), expstr)
        self.load_origin_major_grids()

    def offset_within_size(self, a, b, size):
        # offset of a from b within number of sizes
        d = 0
        if a > b:
            while a > b:
                d += 1
                b += size
        else:
            while a < b:
                d -= 1
                b -= size
        return d

    def grid_xyloc_from_origin(self, pt):  # p is center point of grid
        g = self.major_grid_m()
        o = self.current_origin_point()
        return [self.offset_within_size(pt.x(), o.x(), g),
                self.offset_within_size(pt.y(), o.y(), g)]

    def grid_xyloc_exists(self, xyloc):
        expstr = ' "kind"=\'major\' and "x"={0} and "y"={1} and "origin"={2} '.\
            format(xyloc[0], xyloc[1], self.current_origin())
        feats = self.get_features(self.grid_layer_id(), expstr)
        return len(feats) > 0

    def create_grid_geom(self, pt, kind):  # lower left point
        g = self.major_grid_m() if kind == 'major' else self.minor_grid_m()
        pts = [QgsPoint(pt.x(), pt.y()),
               QgsPoint(pt.x(), pt.y() + g),
               QgsPoint(pt.x() + g, pt.y() + g),
               QgsPoint(pt.x() + g, pt.y())]
        return QgsGeometry.fromPolygon([pts])

    def minor_grid_id(self):  # generator
        ab = list(map(chr, range(ord('a'), ord('z') + 1)))
        (i, l) = 0, 1
        while True:
            char = ab[i]
            yield char * l
            i += 1
            if i == 26:
                (i, l) = 0, l + 1

    def create_grid(self, layer, pt, ptloc='ll'):
        if not self.check_grid_squares():
            return
        if not layer:
            return

        x = pt.x()
        y = pt.y()
        g = self.major_grid_m()
        # normalize to lower left coord
        if ptloc == 'ul':  # upper left
            y -= g
        elif ptloc == 'ur':  # upper right
            x -= g
            y -= g
        elif ptloc == 'lr':  # lower right
            x -= g
        xyloc = self.grid_xyloc_from_origin(QgsPoint(x + g / 2, y + g / 2))

        # don't duplicate grids
        # TODO: maybe move to comparison of set of origin_major_grids_xylocs()
        if self.grid_xyloc_exists(xyloc):
            return

        # major grid feature
        feat1 = QgsFeature()
        feat1.setGeometry(self.create_grid_geom(QgsPoint(x, y), 'major'))
        fields = layer.pendingFields()
        feat1.setFields(fields)
        feat1["kind"] = 'major'
        feat1['x'] = xyloc[0]
        feat1['y'] = xyloc[1]
        feat1['minor'] = "n/a"
        feat1['origin'] = self.current_origin()
        layer.addFeature(feat1, True)

        # self.pydev()

        # minor grid features (from top-left to bottom-right)
        n = self.major_grid() // self.minor_grid()
        mg = self.minor_grid_m()
        # whether to buffer exterior of major with minor
        mbuf = self.buffer_major_grid()
        if mbuf:
            n += 2
            x -= mg
            y -= mg
        gid = self.minor_grid_id()  # generator
        for j in range(n)[::-1]:
            my = y + j * mg
            for k in range(n):
                mx = x + k * mg
                feat2 = QgsFeature()
                feat2.setGeometry(
                    self.create_grid_geom(QgsPoint(mx, my), 'minor'))
                fields = layer.pendingFields()
                feat2.setFields(fields)
                feat2["kind"] = 'minor'
                feat2['x'] = xyloc[0]
                feat2['y'] = xyloc[1]
                mid = ' '  # column should not contain NULL
                if mbuf:
                    if j != 0 and j != n - 1 and k != 0 and k != n - 1:
                        mid = gid.next()
                else:
                    mid = gid.next()
                feat2['minor'] = mid
                feat2['origin'] = self.current_origin()
                layer.addFeature(feat2, True)

    def origin_major_grids(self, origin=-1):
        if origin == -1:
            origin = self.current_origin()
        if origin == -1:
            return []
        expstr = " \"kind\"='major' AND \"origin\"={0} ".format(origin)
        return self.get_features(self.grid_layer_id(), expstr)

    def origin_major_grids_xylocs(self):
        xylocs = []
        for grid in self.origin_major_grids():
            xylocs.append((grid['x'], grid['y']))
        return xylocs  # list of tuples

    def reload_origin_major_grids(self):
        QTimer.singleShot(1000, self.load_origin_major_grids)

    def load_origin_major_grids(self):
        self.gridsCmbBx.blockSignals(True)
        self.gridsCmbBx.clear()
        self.gridsCmbBx.blockSignals(False)

        if self.current_origin() == -1:
            self.gridFrame.setEnabled(False)
            return
        self.gridFrame.setEnabled(True)

        grids = self.origin_major_grids()
        hasgrids = len(grids) > 0

        self.addGridGridRadio.setEnabled(hasgrids)
        self.addGridGridRadio.setChecked(hasgrids)
        self.addGridOriginRadio.setChecked(not hasgrids)
        self.gridsGoToCornerFrame.setEnabled(hasgrids)
        self.gridsEditFrame.setEnabled(hasgrids)
        self.gridsAllFrame.setEnabled(hasgrids)
        if hasgrids:
            # sort grids by x then y
            glist = []
            for grid in grids:
                glist.append((grid.id(), grid['pkuid'],
                              int(grid['x']), int(grid['y']), grid['name']))
            glist = sorted(glist, key=itemgetter(2, 3))

            self.gridsCmbBx.blockSignals(True)

            defaultdata = "{0}{1}{0}".format("-1", self.datadelim)
            datalist = self.split_data(
                self.settings.value("currentGrid", defaultdata, type=str))
            (curorig, curgrid) = datalist[0], datalist[1]
            curindx = -1
            # populate grids combobox
            for (i, g) in enumerate(glist):
                name = "{0}, {1}{2}".format(
                    str(g[2]),
                    str(g[3]),
                    "   ({0})".format(g[4]) if g[4] else '')
                self.gridsCmbBx.addItem(name, self.join_data(g[0], g[1]))

                if (curgrid != "-1" and
                        curorig == self.current_origin() and
                        curgrid == str(g[1])):
                    curindx = i

            if curindx > -1 and not curindx > (self.gridsCmbBx.count() - 1):
                    self.gridsCmbBx.setCurrentIndex(curindx)

            self.gridsCmbBx.blockSignals(False)

        # trigger gui updates
        self.update_current_grid()
        self.on_addGridRadioGrp_buttonClicked(
            self.addGridGridRadio if hasgrids
            else self.addGridOriginRadio)

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
        if avl.id() != self.feature_layer_id():
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
        self.msgbar.pushMessage(self.tr("Fossil Dig Tools"),
                                msg,
                                kind,
                                self.iface.messageTimeout())

    def notice(self, notice):
        self.noticeLabel.show()
        self.noticeLabel.setText(notice)

    def clear_notice(self):
        self.noticeLabel.setText("")
        self.noticeLabel.hide()

    def add_grids_ref_is_origin(self):
        return self.addGridRadioGrp.checkedButton() == \
            self.addGridOriginRadio

    def add_grids_has_checked(self):
        haschecked = False
        for btn in self.addGridBtnGrp.buttons():
            if btn.isCheckable() and btn.isChecked():
                haschecked = True
                break
        return haschecked

    def reset_add_grid_btns(self):
        for btn in self.addGridBtnGrp.buttons():
            btn.setEnabled(True)
            if btn.isCheckable():
                btn.setChecked(False)

    def set_grid_btns(self, origin=False):
        if origin:
            self.addGridNBtn.setEnabled(False)
            self.addGridSBtn.setEnabled(False)
            self.addGridWBtn.setEnabled(False)
            self.addGridEBtn.setEnabled(False)

    def update_grid_buttons(self):
        origin = self.add_grids_ref_is_origin()
        c = [0, 0]  # center reference x/y location
        if not origin:
            c = self.grid_xyloc_from_origin(self.current_grid_center())
        (x, y) = c[0], c[1]

        # handle when x or y is 1 or -1 and relative grid to test crosses axis
        # i.e., there are never any tested x or y that are 0
        mx = 2 if x == 1 else 1
        px = 2 if x == -1 else 1
        my = 2 if y == 1 else 1
        py = 2 if y == -1 else 1

        xylocs = set(self.origin_major_grids_xylocs())  # set(list of tuples)

        self.addGridNWBtn.setEnabled((x - mx, y + py) not in xylocs)
        self.addGridNEBtn.setEnabled((x + px, y + py) not in xylocs)
        self.addGridSWBtn.setEnabled((x - mx, y - my) not in xylocs)
        self.addGridSEBtn.setEnabled((x + px, y - my) not in xylocs)

        if not origin:
            self.addGridNBtn.setEnabled((x, y + py) not in xylocs)
            self.addGridEBtn.setEnabled((x + px, y) not in xylocs)
            self.addGridWBtn.setEnabled((x - mx, y) not in xylocs)
            self.addGridSBtn.setEnabled((x, y - my) not in xylocs)

    def open_settings_dlg(self):
        settingsDlg = FdtSettingsDialog(self, self.iface, self.settings)
        settingsDlg.exec_()
        self.check_plugin_ready()

    @pyqtSlot(int)
    def on_originPinCmbBx_currentIndexChanged(self, indx):
        self.update_current_origin()
        self.load_origin_children()

    @pyqtSlot()
    def on_originPinAddBtn_clicked(self):
        pinDlg = FdtPinDialog(self, self.iface, 'origin')
        # pinDlg.accepted.connect(self.load_pins)
        pinDlg.show()

    @pyqtSlot()
    def on_originPinEditBtn_clicked(self):
        feat = self.current_origin_feat()
        if feat.isValid():
            pinDlg = FdtPinDialog(self, self.iface, 'origin', feat)
            # pinDlg.accepted.connect(self.load_pins)
            pinDlg.show()

    @pyqtSlot()
    def on_originPinRemoveBtn_clicked(self):
        hasgrids = self.origin_has_grids()
        msgbx = QMessageBox(self.parent())
        msgbx.setIcon(QMessageBox.Warning)
        msgbx.setWindowTitle(self.tr("Caution!"))
        msgbx.setText(
            self.tr("Really delete current origin pin?\n"))
        msgbx.setInformativeText(
            self.tr("(operation can not be undone)"))
        if hasgrids:
            msgbx.setDetailedText(self.tr(
                "Deleting just pin will orphan any associated grids, "
                "which will have to be manually deleted."))
        msgbx.setStandardButtons(QMessageBox.Cancel)
        delpin = msgbx.addButton(self.tr("Delete pin"),
                                 QMessageBox.ActionRole)
        delgrids = None
        if hasgrids:
            delgrids = msgbx.addButton(self.tr("Delete pin and grids"),
                                       QMessageBox.ActionRole)
        msgbx.setDefaultButton(QMessageBox.Cancel)
        msgbx.exec_()
        btn = msgbx.clickedButton()
        if btn == QMessageBox.Cancel:
            return
        elif btn == delpin:
            self.delete_current_origin()
        elif btn == delgrids:
            self.delete_all_origin_grids()
            self.delete_current_origin()

    @pyqtSlot()
    def on_originPinGoToBtn_clicked(self):
        pt = self.current_origin_point()
        rect = self.rect_buf_point(pt, self.major_grid_buf())
        self.zoom_canvas(rect)

        # highlight origin pt
        geom = self.circle_geometry(pt)
        self.add_highlight(self.pin_layer_id(), geom, self.redhlcolor)
        # self.remove_highlights()

    @pyqtSlot("QListWidgetItem *", "QListWidgetItem *")
    def on_directPinList_currentItemChanged(self, cur, prev):
        self.directPinEditFrame.setEnabled(cur is not None)

    @pyqtSlot("QListWidgetItem *")
    def on_directPinList_itemDoubleClicked(self, itm):
        feat = self.current_directional_feat()
        if feat.isValid():
            pinDlg = FdtPinDialog(self, self.iface, 'directional', feat)
            # pinDlg.accepted.connect(self.load_pins)
            pinDlg.show()

    @pyqtSlot()
    def on_directPinAddBtn_clicked(self):
        pinDlg = FdtPinDialog(self, self.iface, 'directional')
        # pinDlg.accepted.connect(self.load_pins)
        pinDlg.show()

    @pyqtSlot()
    def on_directPinRemoveBtn_clicked(self):
        res = QMessageBox.warning(
            self.parent(),
            self.tr("Caution!"),
            self.tr("Really delete selected directional pin?\n\n"
                    "(operation can not be undone)"),
            QMessageBox.Ok | QMessageBox.Cancel,
            QMessageBox.Cancel)
        if res != QMessageBox.Ok:
            return
        self.delete_current_directional()

    @pyqtSlot()
    def on_directPinGoToBtn_clicked(self):
        o = QgsPoint(self.current_origin_point())
        d = QgsPoint(self.current_directional_point())
        # handle instance where extent of pins has no width or height,
        # e.g. they are offest directly north south, east or west
        pad = self.minor_grid_m() / 2
        if o.x() == d.x():
            o.setX(o.x() + pad)
            d.setX(d.x() - pad)
        if o.y() == d.y():
            o.setY(o.y() + pad)
            d.setY(d.y() - pad)

        rect = QgsRectangle(o, d) if o < d else QgsRectangle(d, o)
        self.zoom_canvas(rect)
        self.canvas.zoomByFactor(1.10)  # add a little buffer to extent

        # highlight origin pt
        geom1 = self.circle_geometry(self.current_origin_point())
        self.add_highlight(self.pin_layer_id(), geom1, self.redhlcolor)
        # highlight directional pt
        geom2 = self.circle_geometry(self.current_directional_point())
        self.add_highlight(self.pin_layer_id(), geom2, self.bluehlcolor)
        # self.remove_highlights()

    @pyqtSlot()
    def on_attributesOpenFormBtn_clicked(self):
        for f in self.selected_features():
            self.iface.openFeatureForm(self.iface.activeLayer(), f)

    @pyqtSlot(int)
    def on_gridsCmbBx_currentIndexChanged(self, indx):
        self.update_current_grid()
        self.update_grid_buttons()

    @pyqtSlot()
    def on_gridsGoToUlBtn_clicked(self):
        self.zoom_to_corner_pt(self.current_grid_ul_point())

    @pyqtSlot()
    def on_gridsGoToUrBtn_clicked(self):
        self.zoom_to_corner_pt(self.current_grid_ur_point())

    @pyqtSlot()
    def on_gridsGoToLlBtn_clicked(self):
        self.zoom_to_corner_pt(self.current_grid_ll_point())

    @pyqtSlot()
    def on_gridsGoToLrBtn_clicked(self):
        self.zoom_to_corner_pt(self.current_grid_lr_point())

    @pyqtSlot()
    def on_gridsEditBtn_clicked(self):
        feat = self.current_grid_feat()
        ok = False
        (name, ok) = QInputDialog.getText(
            self.parent(),
            "Grid name",
            "Grid identification name",
            QLineEdit.Normal,
            feat['name'])
        if not ok:
            return

        layer = self.get_layer(self.grid_layer_id())
        if not layer:
            return
        layer.startEditing()
        feat["name"] = name
        layer.updateFeature(feat)
        layer.commitChanges()
        layer.setCacheImage(None)
        layer.triggerRepaint()

    @pyqtSlot()
    def on_gridsRemoveBtn_clicked(self):
        res = QMessageBox.warning(
            self.parent(),
            self.tr("Caution!"),
            self.tr("Really delete current grid?\n\n"
                    "(operation can not be undone)"),
            QMessageBox.Ok | QMessageBox.Cancel,
            QMessageBox.Cancel)
        if res != QMessageBox.Ok:
            return
        self.delete_current_grid()

    @pyqtSlot()
    def on_gridsGoToBtn_clicked(self):
        pt = self.current_grid_center()
        rect = self.rect_buf_point(pt, self.major_grid_buf())
        self.zoom_canvas(rect)

    @pyqtSlot(QAbstractButton)
    def on_addGridRadioGrp_buttonClicked(self, btn):
        self.reset_add_grid_btns()
        origin = False
        if btn is self.addGridGridRadio:
            self.addGridIconLabel.setPixmap(
                QPixmap(":/plugins/fossildigtools/icons/grid.svg"))
        elif btn is self.addGridOriginRadio:
            self.addGridIconLabel.setPixmap(
                QPixmap(":/plugins/fossildigtools/icons/origin.svg"))
            origin = True
        self.set_grid_btns(origin)

        # disable buttons where grids already exist
        self.update_grid_buttons()

    @pyqtSlot()
    def on_gridsAddBtn_clicked(self):
        if not self.add_grids_has_checked():
            return
        layer = self.get_layer(self.grid_layer_id())
        if not layer:
            return

        layer.blockSignals(True)
        layer.startEditing()
        layer.beginEditCommand("Add grids")

        if self.add_grids_ref_is_origin():
            p = self.current_origin_point()
            if self.addGridNWBtn.isChecked():
                self.create_grid(layer, p, 'lr')
            if self.addGridNEBtn.isChecked():
                self.create_grid(layer, p, 'll')
            if self.addGridSWBtn.isChecked():
                self.create_grid(layer, p, 'ur')
            if self.addGridSEBtn.isChecked():
                self.create_grid(layer, p, 'ul')
        else:
            rect = self.current_grid_rect()
            ll = QgsPoint(rect.xMinimum(), rect.yMinimum())
            ul = QgsPoint(rect.xMinimum(), rect.yMaximum())
            ur = QgsPoint(rect.xMaximum(), rect.yMaximum())
            lr = QgsPoint(rect.xMaximum(), rect.yMinimum())

            if self.addGridWBtn.isChecked():
                self.create_grid(layer, ul, 'ur')
            if self.addGridNWBtn.isChecked():
                self.create_grid(layer, ul, 'lr')

            if self.addGridNBtn.isChecked():
                self.create_grid(layer, ur, 'lr')
            if self.addGridNEBtn.isChecked():
                self.create_grid(layer, ur, 'll')

            if self.addGridEBtn.isChecked():
                self.create_grid(layer, lr, 'll')
            if self.addGridSEBtn.isChecked():
                self.create_grid(layer, lr, 'ul')

            if self.addGridSBtn.isChecked():
                self.create_grid(layer, ll, 'ul')
            if self.addGridSWBtn.isChecked():
                self.create_grid(layer, ll, 'ur')

        self.reset_add_grid_btns()

        layer.commitChanges()
        layer.endEditCommand()
        layer.blockSignals(False)

        layer.setCacheImage(None)
        layer.triggerRepaint()
        # trigger gui update manually instead of on layer.editingStopped
        # otherwise, on Mac, cpu maxes out updating the gui many times
        self.load_origin_major_grids()

    @pyqtSlot()
    def on_gridsZoomToAllBtn_clicked(self):
        feats = self.origin_major_grids()
        if not feats:
            return
        rect = QgsRectangle()
        rect.setMinimal()
        for feat in feats:
            r = feat.geometry().boundingBox()
            rect.combineExtentWith(r)

        # buffer it with minor grid
        if self.buffer_major_grid():
            g = self.minor_grid_m()
            ll = QgsPoint(rect.xMinimum() - g, rect.yMinimum() - g)
            ur = QgsPoint(rect.xMaximum() + g, rect.yMaximum() + g)
            rect = QgsRectangle(ll, ur)

        self.zoom_canvas(rect)

    @pyqtSlot()
    def on_gridsRemoveAllBtn_clicked(self):
        res = QMessageBox.warning(
            self.parent(),
            self.tr("Caution!"),
            self.tr("Really delete ALL grids for current origin?\n\n"
                    "(operation can not be undone)"),
            QMessageBox.Ok | QMessageBox.Cancel,
            QMessageBox.Cancel)
        if res != QMessageBox.Ok:
            return

        self.delete_all_origin_grids()


if __name__ == "__main__":
    pass
