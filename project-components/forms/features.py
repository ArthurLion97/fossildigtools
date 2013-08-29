
import os
import sys
import csv
from datetime import datetime

from PyQt4.QtCore import *
from PyQt4.QtGui import *
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

        self.fdtwidget = None
        self.settings = None
        try:
            self.fdtwidget = utils.plugins['fossildigtools'].toolsWidget()
            """:type : fdt_mainwidget.FdtMainWidget"""
            self.settings = utils.plugins['fossildigtools'].pluginSettings()
            """:type : PyQt4.QtCore.QSettings"""
        except:
            raise Exception('Fossil Dig Tools plugin not active')

        # Identification tab
        self.numLEdit = self._getControl("number")
        """:type : PyQt4.QtGui.QLineEdit"""
        self.numLockBtn = self._getControl("numLockBtn")
        """:type : PyQt4.QtGui.QToolButton"""
        # self.pkLEdit = self._getControl("pkuid")
        # """:type : PyQt4.QtGui.QLineEdit"""
        self.blockIdCmbBx = self._getControl("block_id")
        """:type : PyQt4.QtGui.QComboBox"""
        self.genusCmbBx = self._getControl("genus")
        """:type : PyQt4.QtGui.QComboBox"""
        self.identCmbBx = self._getControl("identify")
        """:type : PyQt4.QtGui.QComboBox"""
        self.identBtn = self._getControl("identBtn")
        """:type : PyQt4.QtGui.QToolButton"""
        self.lrCmbBx = self._getControl("left_right")
        """:type : PyQt4.QtGui.QComboBox"""
        self.fragChkBx = self._getControl("fragment")
        """:type : PyQt4.QtGui.QCheckBox"""
        self.wBoneSpnBx = self._getControl("with_bone")
        """:type : PyQt4.QtGui.QSpinBox"""
        self.wBoneBtn = self._getControl("withBoneBtn")
        """:type : PyQt4.QtGui.QToolButton"""
        self.ontgyCmbBx = self._getControl("ontogeny")
        """:type : PyQt4.QtGui.QComboBox"""

        # Attributes tab
        self.origNameLEdit = self._getControl("originName")
        """:type : PyQt4.QtGui.QLineEdit"""
        self.origLEdit = self._getControl("origin")
        """:type : PyQt4.QtGui.QLineEdit"""
        self.gridCmbBx = self._getControl("grid")
        """:type : PyQt4.QtGui.QComboBox"""
        self.zOrderSpnBx = self._getControl("z_order")
        """:type : PyQt4.QtGui.QSpinBox"""
        self.assocChkBx = self._getControl("associated")
        """:type : PyQt4.QtGui.QCheckBox"""
        self.complSpnBx = self._getControl("percent")
        """:type : PyQt4.QtGui.QSpinBox"""
        self.countsChkBx = self._getControl("counts")
        """:type : PyQt4.QtGui.QCheckBox"""
        self.prsrvCmbBx = self._getControl("preservation")
        """:type : PyQt4.QtGui.QComboBox"""
        self.lenDSpnBx = self._getControl("length")
        """:type : PyQt4.QtGui.QDoubleSpinBox"""
        self.wdthDSpnBx = self._getControl("width")
        """:type : PyQt4.QtGui.QDoubleSpinBox"""
        self.dpthDSpnBx = self._getControl("depth")
        """:type : PyQt4.QtGui.QDoubleSpinBox"""
        self.unitsCmbBx = self._getControl("units")
        """:type : PyQt4.QtGui.QComboBox"""

        # Notes tab
        self.notesPTEdit = self._getControl("notes")
        """:type : PyQt4.QtGui.QPlainTextEdit"""
        self.pkgCmbBx = self._getControl("packaging")
        """:type : PyQt4.QtGui.QComboBox"""
        self.addLEdit = self._getControl("added")
        """:type : PyQt4.QtGui.QLineEdit"""
        self.modLEdit = self._getControl("modified")
        """:type : PyQt4.QtGui.QLineEdit"""

        # bogart button box connections for custom slots
        self.buttonBox = self._getControl("buttonBox")
        """:type : PyQt4.QtGui.QDialogButtonBox"""

        self.setupGui()

        # post-populate connections
        self.numLockBtn.toggled.connect(self._toggleNumLEdit)

        self.genusCmbBx.currentIndexChanged[int].connect(
            self.updateIdentifyListButton)

        self.identBtn.clicked.connect(self.showIdentSelector)

        # # disconnect signal QGIS has wired up for the dialog to the button box
        # self.buttonBox.accepted.disconnect(self.dlg.accept)
        #
        # # wire up our own signals
        # self.buttonBox.accepted.connect(self.dialogAccept)
        # self.buttonBox.rejected.connect(self.dialogReject)

        self.dlg.accepted.connect(self._saveGeometry)
        self.dlg.rejected.connect(self._saveGeometry)
        self.dlg.restoreGeometry(self.settings.value(
            "/featForm/geometry",
            QByteArray(),
            type=QByteArray))

    def setupGui(self):
        # self.nextPrimaryKey()
        self.nextFeatureNumber()
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
        # self.pkLEdit.setVisible(False)
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

        # set focus
        self.genusCmbBx.setFocus()

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
            self.populateUniqueComboBox(*c)

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
        if not self._isEmptyOrNull(curtxt):
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

    def nextFeatureNumber(self):
        # don't increment existing number
        if not self._isEmptyOrNull(self.numLEdit.text()):
            return

        maxnum = 0

        # get maximum of committed features
        indx = self.layer.fieldNameIndex('number')
        mx = self.layer.maximumValue(indx)
        if mx is not None:
            maxnum = mx

        # dp = self.layer.dataProvider()
        # ds = QgsDataSourceURI(dp.dataSourceUri())
        #
        # # connect to layer's parent database
        # conn = db.connect(ds.database())
        # cur = conn.cursor()
        #
        # sql = 'SELECT MAX(number) FROM "{0}"'.format(ds.table())
        # rs = cur.execute(sql)
        # rslist = list(rs)
        #
        # if rslist:
        #     mx = rslist[0][0]
        #     print "mx: {0}".format(mx)
        #     if isinstance(mx, int):
        #         maxnum = mx

        fadd = self.layer.pendingFeatureCount() - self.layer.featureCount()
        # req = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)
        # fit = self.layer.getFeatures(req)
        # fcnt = len(list(fit))

        nextId = (maxnum + fadd + 1)
        self.numLEdit.setText(str(nextId))
        print "nextId = (maxnum + fadd)=({0} + {1}) + 1 = {2}".format(
            maxnum, fadd, nextId)

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

        if self._isEmptyOrNull(self.addLEdit.text()):
            self.addLEdit.setText(stamp)
        self.modLEdit.setText(stamp)

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

    @pyqtSlot(bool)
    def _toggleNumLEdit(self, chkd):
        icon = QIcon(':/fdt/icons/{0}locked.svg'.format('un' if chkd else ''))
        self.numLockBtn.setIcon(icon)
        self.numLEdit.setEnabled(chkd)

    def _isEmptyOrNull(self, txt):
        return not txt or txt.lower().strip() == 'null'

    def _getControl(self, name, control_type=QWidget):
        """
        Return a control from the dialog using its name
        """
        return self.dlg.findChild(control_type, name)

    @pyqtSlot()
    def _saveGeometry(self):
        self.settings.setValue("/featForm/geometry", self.dlg.saveGeometry())


def formOpen(dialog, layer, featureid):
    # global cf  # have to raise the scope so dialog's widget signals can connect
    return CustomForm(dialog, layer, featureid)
    # dialog.destroyed.connect(cf.deleteLater)


