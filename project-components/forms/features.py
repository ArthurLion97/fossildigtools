
import os
import sys
import csv
# import inspect

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

    def __init__(self, dialog, layer, featureid):
        """
        :type dialog: PyQt4.QtGui.QDialog
        :type layer: qgis.core.QgsVectorLayer
        :type featureid: int
        """
        QObject.__init__(self)

        self.dlg = dialog
        self.layer = layer
        self.featid = featureid
        self.projdir = PROJDIR

        self.pkuidLEdit = self.dlg.findChild(QLineEdit, "pkuid")
        """:type : PyQt4.QtGui.QLineEdit"""
        self.pkuidLEdit.setVisible(False)

        self.numLEdit = self.dlg.findChild(QLineEdit, "number")
        """:type : PyQt4.QtGui.QLineEdit"""
        self.genusCmbBx = self.dlg.findChild(QComboBox, "genus")
        """:type : PyQt4.QtGui.QComboBox"""
        self.identCmbBx = self.dlg.findChild(QComboBox, "identify")
        """:type : PyQt4.QtGui.QComboBox"""
        self.identBtn = self.dlg.findChild(QToolButton, "identBtn")
        """:type : PyQt4.QtGui.QToolButton"""
        # self.identBtnMenu = QMenu(self.dlg)
        # self.identBtn.setMenu(self.identBtnMenu)
        self.origin = self.dlg.findChild(QLineEdit, "origin")
        """:type : PyQt4.QtGui.QLineEdit"""

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

        # bogart button box connections with custom slots
        self.buttonBox = self.dlg.findChild(QDialogButtonBox, "buttonBox")
        """:type : PyQt4.QtGui.QDialogButtonBox"""

        # disconnect signal QGIS has wired up for the dialog to the button box
        # buttonBox.accepted.disconnect(self.dlg.accept)
        #
        # wire up our own signals
        # buttonBox.accepted.connect(validate)
        # buttonBox.rejected.connect(self.dlg.reject)

        self.setupGui()
        self.nextPrimaryKey()
        self.populateGenusComboBox()
        # must come after genus cmbbx populate
        self.updateIdentifyListButton()
        self.populateIdentifyComboBox()

        self.setCurrentOrigin()

        # post-populate connections
        self.genusCmbBx.currentIndexChanged[int].connect(
            self.updateIdentifyListButton)

        self.identBtn.clicked.connect(self.showIdentSelector)

    def setupGui(self):
        if not self.layer.isEditable():
            self.identBtn.setVisible(False)
            return
        self.identBtn.setIcon(QIcon(':/fdt/icons/bone.svg'))

    def nextPrimaryKey(self):
        # don't increment existing number
        if self.pkuidLEdit.text():
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
        if not rs:
            return
        pkuid = list(rs)[0][0]
        # print "pkuid: {0}".format(pkuid)

        eb = self.layer.editBuffer()
        addedf = len(eb.addedFeatures()) if self.layer.isEditable() else 0
        # print "addedf: {0}".format(addedf)

        nextId = (pkuid + addedf + 1)
        self.pkuidLEdit.setText(str(nextId))
        # print "pkuid + addedf + 1: {0}".format(nextId)

        self.numLEdit.setText(str(nextId))

    def populateGenusComboBox(self):
        curtxt = self.genusCmbBx.currentText()
        self.genusCmbBx.clear()

        model = self.genusCmbBx.model()
        self._addModelItem(model, 'N/A')
        self._addModelItem(model, 'Unknown')
        self._addModelSeparator(model)
        for genus, ident in GENUSINDENTS.iteritems():
            self._addModelItem(model, genus, data=ident)
        assert model.rowCount() > 0, 'No rows in genus-ident model'

        indx = self.genusCmbBx.findText(GENUSPREF)
        if curtxt:
            indx = self.genusCmbBx.findText(curtxt)
        if indx != -1:
            self.genusCmbBx.setCurrentIndex(indx)

    def currentGenusIdent(self):
        return self.genusCmbBx.itemData(self.genusCmbBx.currentIndex())

    @pyqtSlot()
    def updateIdentifyListButton(self):
        self.identBtn.setEnabled(self.currentGenusIdent() is not None)

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

    @pyqtSlot(int)
    def populateIdentifyComboBox(self, indx=-1):
        curtxt = self.identCmbBx.currentText()

        # add general idents
        if not os.path.exists(GENERALIDENT):
            raise IOError('Missing general identify file: ' + GENERALIDENT)

        model = self.identCmbBx.model()
        """:type: QStandardItemModel"""

        with open(GENERALIDENT, 'r') as f:
            for line in f:
                self._addModelItem(model, line.strip())
        if model.rowCount() > 0:
            self._addModelSeparator(model)

        identvals = set()
        indx = self.layer.fieldNameIndex('identify')
        # get unique values from uncomitted edits
        eb = self.layer.editBuffer()
        addedf = eb.addedFeatures() if self.layer.isEditable() else {}
        # print addedf
        for f in addedf.itervalues():
            val = str(f[indx])
            if val:
                identvals.add(val)

        # get unique values for existing ident vals

        vals = set(self.layer.dataProvider().uniqueValues(indx))
        identvals.update(vals)
        # print sorted(list(identvals)).__repr__()

        for val in sorted(list(identvals), key=lambda s: s.lower()):
            val = val.strip()
            if val and val != 'None':
                self._addModelItem(model, val.strip())

        if curtxt:  # reset any existing attr value
            self.identCmbBx.lineEdit().setText(curtxt)

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
            # # update font
            # f = item.font()
            # f.setBold(header)
            # # f.setItalic(header)
            # f.setUnderline(header)
            # item.setFont(f)
        if title:
            item.setForeground(QColor(Qt.red))

        model.appendRow(item)

    def _addModelSeparator(self, model):
        item = QStandardItem()
        item.setData('separator', role=Qt.AccessibleDescriptionRole)
        model.appendRow(item)

    def setCurrentOrigin(self):
        if self.fdtwidget is None:
            return
        # print 'setCurrentOrigin entered'
        orgf = self.fdtwidget.current_origin_feat()
        orgname = orgf['name']
        self.origin.setText(orgname)

    def validate(self):
        self.dlg.accept()
        # # Make sure that the name field isn't empty.
        # if not self.pkuidLEdit.text().length() > 0:
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


