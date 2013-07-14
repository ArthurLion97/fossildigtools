# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/larrys/QGIS/PluginProjects/fossildigtools/fdt_pinwidget.ui'
#
# Created: Sun Jul 14 14:26:55 2013
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_AddPinDialog(object):
    def setupUi(self, AddPinDialog):
        AddPinDialog.setObjectName(_fromUtf8("AddPinDialog"))
        AddPinDialog.resize(486, 246)
        self.verticalLayout = QtGui.QVBoxLayout(AddPinDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(AddPinDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtGui.QDialogButtonBox(AddPinDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AddPinDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AddPinDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AddPinDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AddPinDialog)

    def retranslateUi(self, AddPinDialog):
        AddPinDialog.setWindowTitle(_translate("AddPinDialog", "Add Pin", None))
        self.label.setText(_translate("AddPinDialog", "Add a location pin", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    AddPinDialog = QtGui.QDialog()
    ui = Ui_AddPinDialog()
    ui.setupUi(AddPinDialog)
    AddPinDialog.show()
    sys.exit(app.exec_())

