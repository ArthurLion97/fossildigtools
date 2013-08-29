from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from pyspatialite import dbapi2 as db

# during dev of script leave attribute active: will reload module of form open
# DEBUGMODE = True

# pkuidLineEdit = None
# myDialog = None


def formOpen(dialog, layer, featureid):
    QTimer.singleShot(0, dialog.accept)
    # global myDialog
    # myDialog = dialog
    # myDialog.setVisible(False)
    # global pkuidLineEdit
    # pkuidLineEdit = dialog.findChild(QLineEdit, "pkuid")
    # buttonBox = dialog.findChild(QDialogButtonBox, "buttonBox")
    #
    # # pre-populate pkuid with next incremented primary key
    # l = layer
    # dp = l.dataProvider()
    # ds = QgsDataSourceURI(dp.dataSourceUri())
    #
    # # connect to layer's parent database
    # conn = db.connect(ds.database())
    # cur = conn.cursor()
    #
    # sql = 'SELECT "seq" FROM "sqlite_sequence"' \
    #       'WHERE name = "{0}"'.format(ds.table())
    # rs = cur.execute(sql)
    # pkuid = list(rs)[0][0]
    # # print "pkuid: {0}".format(pkuid)
    #
    # eb = l.editBuffer()
    # addedf = len(eb.addedFeatures()) if l.isEditable() else 0
    # # print "addedf: {0}".format(addedf)
    #
    # nextId = (pkuid + addedf + 1)
    # pkuidLineEdit.setText(str(nextId))
    # # print "pkuid + addedf + 1: {0}".format(nextId)
    #
    # # myDialog.setHidden(True)
    #
    # QTimer.singleShot(0, myDialog.accept)

    # # Disconnect signal that QGIS has wired up for the dialog to the button box.
    # buttonBox.accepted.disconnect(myDialog.accept)
    #
    # # Wire up our own signals.
    # buttonBox.accepted.connect(validate)
    # buttonBox.rejected.connect(myDialog.reject)
    #
    # # auto-close this dialog
    # btn = buttonBox.button(QDialogButtonBox.Ok)
    # btn.click()


# def validate():
#     myDialog.accept()
    # # Make sure that the name field isn't empty.
    # if not pkuidLineEdit.text().length() > 0:
    #     msgBox = QMessageBox()
    #     msgBox.setText("Name field can not be null.")
    #     msgBox.exec_()
    # else:
    #     # Return the form as accpeted to QGIS.
    #     myDialog.accept()
