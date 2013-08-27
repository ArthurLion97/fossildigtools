
import os
import sys
import csv
# import inspect
from datetime import datetime

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sip import *
from qgis.core import *
import qgis.utils as utils
from pyspatialite import dbapi2 as db

try:
    # just for code completion in PyCharm
    from fdt_mainwidget import FdtMainWidget
except ImportError:
    pass

import resources_rc
from Ui_identify_dlg import Ui_IdentDialog

# during dev of script leave attribute active: will reload module of form open
DEBUGMODE = True

# current module directory, then move up to to project directory
# MODDIR = os.path.dirname(
#     os.path.dirname(inspect.getfile(inspect.currentframe())))
PROJDIR = QgsProject.instance().homePath()

# project-relative configs
IDENTSDIR = os.path.join(PROJDIR, 'ident-files')
GENUSPREF = 'Tyrannosaurus'
GENUSINDENTS = {}
with open(os.path.join(IDENTSDIR, 'genus-idents.txt'), 'rb') as f:
    reader = csv.reader(f, delimiter=':', quoting=csv.QUOTE_NONE)
    for row in reader:
        GENUSINDENTS[row[0].strip()] = row[1].strip()
GENERALIDENT = os.path.join(IDENTSDIR, 'general-ident-vals.txt')


class CustomForm(QObject):

    def __init__(self, dialog, layer, feature):
        """
        :type dialog: PyQt4.QtGui.QDialog
        :type layer: qgis.core.QgsVectorLayer
        :type feature: qgis.core.QgsFeature
        """
        QObject.__init__(self)

        self.dlg = dialog
        self.layer = layer
        self.feat = feature
        self.projdir = PROJDIR

        self.iface = utils.iface
        """:type : qgis.gui.QgisInterface"""

        # self.fdtwidget = \
        #     self.iface.mainWindow().findChild(QWidget, "FDT_MainWidget")
        self.fdtwidget = None
        try:
            self.fdtwidget = utils.plugins['fossildigtools'].toolsWidget()
            """:type : fdt_mainwidget.FdtMainWidget"""
        except:
            pass

        # Identification tab
        self.numLEdit = self.dlg.findChild(QLineEdit, "number")
        """:type : PyQt4.QtGui.QLineEdit"""
        self.numLockBtn = self.dlg.findChild(QPushButton, "numLockBtn")
        """:type : PyQt4.QtGui.QPushButton"""
        self.pkLEdit = self.dlg.findChild(QLineEdit, "pkuid")
        """:type : PyQt4.QtGui.QLineEdit"""
        self.blockIdCmbBx = self.dlg.findChild(QComboBox, "block_id")
        """:type : PyQt4.QtGui.QComboBox"""
        self.genusCmbBx = self.dlg.findChild(QComboBox, "genus")
        """:type : PyQt4.QtGui.QComboBox"""
        self.identCmbBx = self.dlg.findChild(QComboBox, "identify")
        """:type : PyQt4.QtGui.QComboBox"""
        self.identBtn = self.dlg.findChild(QToolButton, "identBtn")
        """:type : PyQt4.QtGui.QToolButton"""
        self.lrCmbBx = self.dlg.findChild(QComboBox, "left_right")
        """:type : PyQt4.QtGui.QComboBox"""
        self.fragChkBx = self.dlg.findChild(QCheckBox, "fragment")
        """:type : PyQt4.QtGui.QCheckBox"""
        self.wBoneSpnBx = self.dlg.findChild(QSpinBox, "with_bone")
        """:type : PyQt4.QtGui.QSpinBox"""
        self.wBoneBtn = self.dlg.findChild(QToolButton, "withBoneBtn")
        """:type : PyQt4.QtGui.QToolButton"""
        self.ontgyCmbBx = self.dlg.findChild(QComboBox, "ontogeny")
        """:type : PyQt4.QtGui.QComboBox"""

        # Attributes tab
        self.origNameLEdit = self.dlg.findChild(QLineEdit, "originName")
        """:type : PyQt4.QtGui.QLineEdit"""
        self.origLEdit = self.dlg.findChild(QLineEdit, "origin")
        """:type : PyQt4.QtGui.QLineEdit"""
        self.gridCmbBx = self.dlg.findChild(QComboBox, "grid")
        """:type : PyQt4.QtGui.QComboBox"""
        self.zOrderSpnBx = self.dlg.findChild(QSpinBox, "z_order")
        """:type : PyQt4.QtGui.QSpinBox"""
        self.assocChkBx = self.dlg.findChild(QCheckBox, "associated")
        """:type : PyQt4.QtGui.QCheckBox"""
        self.complSpnBx = self.dlg.findChild(QSpinBox, "percent")
        """:type : PyQt4.QtGui.QSpinBox"""
        self.countsChkBx = self.dlg.findChild(QCheckBox, "counts")
        """:type : PyQt4.QtGui.QCheckBox"""
        self.prsrvCmbBx = self.dlg.findChild(QComboBox, "preservation")
        """:type : PyQt4.QtGui.QComboBox"""
        self.lenDSpnBx = self.dlg.findChild(QDoubleSpinBox, "length")
        """:type : PyQt4.QtGui.QDoubleSpinBox"""
        self.wdthDSpnBx = self.dlg.findChild(QDoubleSpinBox, "width")
        """:type : PyQt4.QtGui.QDoubleSpinBox"""
        self.dpthDSpnBx = self.dlg.findChild(QDoubleSpinBox, "depth")
        """:type : PyQt4.QtGui.QDoubleSpinBox"""
        self.unitsCmbBx = self.dlg.findChild(QComboBox, "units")
        """:type : PyQt4.QtGui.QComboBox"""

        # Notes tab
        self.notesPTEdit = self.dlg.findChild(QPlainTextEdit, "notes")
        """:type : PyQt4.QtGui.QPlainTextEdit"""
        self.pkgCmbBx = self.dlg.findChild(QComboBox, "packaging")
        """:type : PyQt4.QtGui.QComboBox"""
        self.addLEdit = self.dlg.findChild(QLineEdit, "added")
        """:type : PyQt4.QtGui.QLineEdit"""
        self.modLEdit = self.dlg.findChild(QLineEdit, "modified")
        """:type : PyQt4.QtGui.QLineEdit"""

        # bogart button box connections for custom slots
        self.buttonBox = self.dlg.findChild(QDialogButtonBox, "buttonBox")
        """:type : PyQt4.QtGui.QDialogButtonBox"""

        self.setupGui()

        # post-populate connections
        self.genusCmbBx.currentIndexChanged[int].connect(
            self.updateIdentifyListButton)

        self.identBtn.clicked.connect(self.showIdentSelector)

        # disconnect signal QGIS has wired up for the dialog to the button box
        # self.buttonBox.accepted.disconnect(self.dlg.accept)
        #
        # wire up our own signals
        # self.buttonBox.accepted.connect(validate)
        # self.buttonBox.rejected.connect(self.dlg.reject)

    def setupGui(self):
        self.nextPrimaryKey()
        self.populateGeneralUniqueComboBoxes()
        self.populateGenusComboBox()
        # must come after populateGenusComboBox
        self.updateIdentifyListButton()
        self.populateIdentifyComboBox()

        self.setCurrentOrigin()
        self.populateGridComboBox()
        self.setZOrder()

        self.setDateTimes()

        self.numLEdit.setEnabled(False)
        self.origNameLEdit.setEnabled(False)
        self.pkLEdit.setVisible(False)
        self.origLEdit.setVisible(False)

        self.addLEdit.setEnabled(False)
        self.modLEdit.setEnabled(False)

        if not self.layer.isEditable():
            self.numLockBtn.setVisible(False)
            self.identBtn.setVisible(False)
            self.wBoneBtn.setVisible(False)
            return
        self.numLockBtn.setIcon(QIcon(':/fdt/icons/locked.svg'))
        self.identBtn.setIcon(QIcon(':/fdt/icons/bone.svg'))
        self.wBoneBtn.setIcon(QIcon(':/fdt/icons/bone.svg'))

    def uniqueAllValsSorted(self, field):
        """
        :type field: str
        :returns: list of sorted str values
        """
        return self.fdtwidget.uniqueAllValsSorted(self.layer, field)

    def populateUniqueComboBox(self, cmbx, field, topitems=None):
        """
        :type topitems: list
        :type cmbx: PyQt4.QtGui.QComboBox
        :type field: str
        """
        curtxt = cmbx.currentText()
        model = cmbx.model()
        """:type: QStandardItemModel"""

        if topitems is not None and len(topitems) > 0:
            for val in topitems:
                self._addModelItem(model, val)
            self._addModelSeparator(model)

        for val in self.uniqueAllValsSorted(field.strip()):
            self._addModelItem(model, val)

        if curtxt:  # reset any existing attr value
            cmbx.lineEdit().setText(curtxt)

    def populateGeneralUniqueComboBoxes(self):
        cmbxs = [
            (self.blockIdCmbBx, 'block_id', None),
            (self.ontgyCmbBx, 'ontogeny', None),
            (self.prsrvCmbBx, 'preservation', None),
            (self.pkgCmbBx, 'packaging', None)
        ]
        for c in cmbxs:
            self.populateUniqueComboBox(c[0], c[1], c[2])

    def populateGenusComboBox(self):
        curtxt = self.genusCmbBx.currentText()
        """:type: str"""
        self.genusCmbBx.clear()

        model = self.genusCmbBx.model()
        self._addModelItem(model, 'N/A')
        self._addModelItem(model, 'Unknown')
        self._addModelSeparator(model)
        for genus, ident in GENUSINDENTS.iteritems():
            self._addModelItem(model, genus, data=ident)
        assert model.rowCount() > 0, 'No rows in genus-ident model'

        indx = self.genusCmbBx.findText(GENUSPREF)
        if curtxt and not self._isNull(curtxt):
            indx = self.genusCmbBx.findText(curtxt)
        if indx != -1:
            self.genusCmbBx.setCurrentIndex(indx)

    def currentGenusIdent(self):
        return self.genusCmbBx.itemData(self.genusCmbBx.currentIndex())

    @pyqtSlot()
    def updateIdentifyListButton(self):
        self.identBtn.setEnabled(self.currentGenusIdent() is not None)

    @pyqtSlot(int)
    def populateIdentifyComboBox(self, indx=-1):
        # add general idents
        if GENERALIDENT and not os.path.exists(GENERALIDENT):
            raise IOError('Missing general identify file: ' + GENERALIDENT)

        lines = []
        with open(GENERALIDENT, 'r') as f:
            for line in f:
                lines.append(line.strip())

        self.populateUniqueComboBox(self.identCmbBx, 'identify', lines)

    @pyqtSlot()
    def showIdentSelector(self):
        curindent = self.currentGenusIdent()
        if curindent is None:  # reset any existing attr value
            print 'Missing identify file for current genus'
            return

        identfile = os.path.join(IDENTSDIR, curindent)
        if not os.path.exists(identfile):
            raise IOError('Missing identify file: ' + identfile)

        model = QStandardItemModel()
        title = ''

        with open(identfile, 'r') as f:
            for line in f:
                if line.count('###'):
                    title = line.replace('###', '').strip()
                    continue
                isheader = line.count('---')
                if isheader:
                    line = line.replace('---', '')
                self._addModelItem(model, line.strip(), header=isheader)
        assert model.rowCount() > 0, 'No rows in identify model'

        identdlg = QDialog(self.dlg)
        identdlg.ui = Ui_IdentDialog()
        identdlg.ui.setupUi(identdlg)
        identdlg.ui.genusLabel.setText(title)
        identview = identdlg.ui.identListView
        """:type: PyQt4.QtGui.QListView"""
        identview.setModel(model)
        identview.doubleClicked.connect(identdlg.accept)
        if identdlg.exec_():
            ident = model.itemFromIndex(identview.currentIndex())
            self.identCmbBx.setEditText(ident.text())

    def _addModelItem(self, model, name,
                      flags=None, data=None,
                      enabled=True, icon=None,
                      header=False, title=False):
        item = QStandardItem(name)
        if flags is not None:
            item.setFlags(flags)
        if data is not None:
            item.setData(data, role=Qt.UserRole)
        if not enabled:
            item.setEnabled(False)
        if icon is not None:
            item.setIcon(icon)
        if header:
            item.setForeground(QColor(Qt.blue))
            # setting font doesn't work ???
        if title:
            item.setForeground(QColor(Qt.red))

        model.appendRow(item)

    def _addModelSeparator(self, model):
        item = QStandardItem()
        item.setData('separator', role=Qt.AccessibleDescriptionRole)
        model.appendRow(item)

    def nextPrimaryKey(self):
        # don't increment existing number
        if self.pkLEdit.text():
            return
            # pre-populate pkuid with next incremented primary key
        dp = self.layer.dataProvider()
        ds = QgsDataSourceURI(dp.dataSourceUri())

        # connect to layer's parent database
        conn = db.connect(ds.database())
        cur = conn.cursor()

        sql = 'SELECT "seq" FROM "sqlite_sequence"' \
              'WHERE name = "{0}"'.format(ds.table())
        rs = cur.execute(sql)
        pkuid = 0
        if list(rs):
            pkuid = list(rs)[0][0]
        # print "pkuid: {0}".format(pkuid)

        eb = self.layer.editBuffer()
        addedf = len(eb.addedFeatures()) if self.layer.isEditable() else 0
        # print "addedf: {0}".format(addedf)

        nextId = (pkuid + addedf + 1)
        self.pkLEdit.setText(str(nextId))
        # print "pkuid + addedf + 1: {0}".format(nextId)

        self.numLEdit.setText(str(nextId))

    def setCurrentOrigin(self):
        if self.fdtwidget is None:
            return
        # print 'setCurrentOrigin entered'
        orgf = self.fdtwidget.current_origin_feat()
        orgname = orgf['name']
        self.origNameLEdit.setText(orgname)

    def populateGridComboBox(self):
        curtxt = self.gridCmbBx.currentText()
        if not self.feat:
            return
        frect = self.feat.geometry().boundingBox()

        req = QgsFeatureRequest()
        req.setFilterRect(frect)
        feats = list(self.fdtwidget.grid_layer().getFeatures(req))
        # """:type: qgis.core.QgsFeatureIterator"""
        if len(feats) < 0:
            return

        model = self.gridCmbBx.model()
        for f in feats:
            if f['kind'] == 'major':
                self._addModelItem(model, '{0},{1}'.format(f['x'], f['y']))

        if curtxt:
            self.gridCmbBx.lineEdit().setText(curtxt)

    def setZOrder(self):
        if self.zOrderSpnBx.value() != 0:
            return
        zlist = self.uniqueAllValsSorted('z_order')
        # print 'zlist: ' + zlist.__repr__()
        maxval = 0 if not zlist else max(map(int, zlist))
        self.zOrderSpnBx.setValue(maxval + 1)

    def setDateTimes(self):
        if not self.layer.isEditable():
            return

        now = datetime.now()
        now = now.replace(microsecond=0)
        stamp = now.isoformat(' ')

        if self._isNull(self.addLEdit.text()):
            self.addLEdit.setText(stamp)
        self.modLEdit.setText(stamp)

    def _isNull(self, txt):
        return txt.lower().strip() == 'null'

    def validate(self):
        self.dlg.accept()
        # # Make sure that the name field isn't empty.
        # if not self.pkLEdit.text().length() > 0:
        #     msgBox = QMessageBox()
        #     msgBox.setText("Name field can not be null.")
        #     msgBox.exec_()
        # else:
        #     # Return the form as accpeted to QGIS.
        #     self.dlg.accept()


def formOpen(dialog, layer, featureid):
    global cf  # have to raise the scope so dialog's widget signals can connect
    cf = CustomForm(dialog, layer, featureid)
    dialog.destroyed.connect(cf.deleteLater)


