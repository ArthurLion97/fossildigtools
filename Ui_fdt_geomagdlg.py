# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fdt_geomagdlg.ui'
#
# Created: Wed Jul 24 17:55:08 2013
#      by: PyQt4 UI code generator 4.10.2
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

class Ui_GeoMagDialog(object):
    def setupUi(self, GeoMagDialog):
        GeoMagDialog.setObjectName(_fromUtf8("GeoMagDialog"))
        GeoMagDialog.resize(340, 646)
        GeoMagDialog.setMinimumSize(QtCore.QSize(340, 0))
        self.verticalLayout = QtGui.QVBoxLayout(GeoMagDialog)
        self.verticalLayout.setMargin(3)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.scrollArea = QtGui.QScrollArea(GeoMagDialog)
        self.scrollArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 328, 553))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setMargin(3)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.decLocGrpBx = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.decLocGrpBx.setObjectName(_fromUtf8("decLocGrpBx"))
        self.gridLayout = QtGui.QGridLayout(self.decLocGrpBx)
        self.gridLayout.setMargin(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.frame = QtGui.QFrame(self.decLocGrpBx)
        self.frame.setFrameShape(QtGui.QFrame.Box)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_2.setMargin(6)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.decXDblSpinBx = QtGui.QDoubleSpinBox(self.frame)
        self.decXDblSpinBx.setDecimals(4)
        self.decXDblSpinBx.setMaximum(10000000.0)
        self.decXDblSpinBx.setObjectName(_fromUtf8("decXDblSpinBx"))
        self.horizontalLayout.addWidget(self.decXDblSpinBx)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_4 = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_2.addWidget(self.label_4)
        self.decYDblSpinBx = QtGui.QDoubleSpinBox(self.frame)
        self.decYDblSpinBx.setDecimals(4)
        self.decYDblSpinBx.setMaximum(10000000.0)
        self.decYDblSpinBx.setObjectName(_fromUtf8("decYDblSpinBx"))
        self.horizontalLayout_2.addWidget(self.decYDblSpinBx)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_9 = QtGui.QLabel(self.frame)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.horizontalLayout_3.addWidget(self.label_9)
        self.captureLocBtn = QtGui.QToolButton(self.frame)
        self.captureLocBtn.setMinimumSize(QtCore.QSize(26, 26))
        self.captureLocBtn.setMaximumSize(QtCore.QSize(26, 26))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/fossildigtools/icons/capturepin-origin.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.captureLocBtn.setIcon(icon)
        self.captureLocBtn.setIconSize(QtCore.QSize(20, 20))
        self.captureLocBtn.setCheckable(True)
        self.captureLocBtn.setObjectName(_fromUtf8("captureLocBtn"))
        self.horizontalLayout_3.addWidget(self.captureLocBtn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.gridLayout.addWidget(self.frame, 1, 1, 2, 1)
        self.pinOriginLabel = QtGui.QLabel(self.decLocGrpBx)
        self.pinOriginLabel.setObjectName(_fromUtf8("pinOriginLabel"))
        self.gridLayout.addWidget(self.pinOriginLabel, 0, 0, 1, 1)
        self.decOriginLineEdit = QtGui.QLineEdit(self.decLocGrpBx)
        self.decOriginLineEdit.setStyleSheet(_fromUtf8("QLineEdit {background-color: rgba(255, 255, 255, 128);}"))
        self.decOriginLineEdit.setReadOnly(True)
        self.decOriginLineEdit.setObjectName(_fromUtf8("decOriginLineEdit"))
        self.gridLayout.addWidget(self.decOriginLineEdit, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.decLocGrpBx)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_6 = QtGui.QLabel(self.decLocGrpBx)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.decElevDblSpnBx = QtGui.QDoubleSpinBox(self.decLocGrpBx)
        self.decElevDblSpnBx.setDecimals(3)
        self.decElevDblSpnBx.setMaximum(30000.0)
        self.decElevDblSpnBx.setObjectName(_fromUtf8("decElevDblSpnBx"))
        self.horizontalLayout_6.addWidget(self.decElevDblSpnBx)
        self.decElevUnitsCmbBx = QtGui.QComboBox(self.decLocGrpBx)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.decElevUnitsCmbBx.sizePolicy().hasHeightForWidth())
        self.decElevUnitsCmbBx.setSizePolicy(sizePolicy)
        self.decElevUnitsCmbBx.setObjectName(_fromUtf8("decElevUnitsCmbBx"))
        self.decElevUnitsCmbBx.addItem(_fromUtf8(""))
        self.decElevUnitsCmbBx.addItem(_fromUtf8(""))
        self.horizontalLayout_6.addWidget(self.decElevUnitsCmbBx)
        self.gridLayout.addLayout(self.horizontalLayout_6, 3, 1, 1, 1)
        self.verticalLayout_3.addWidget(self.decLocGrpBx)
        self.decDeclinationGrpBx = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.decDeclinationGrpBx.setObjectName(_fromUtf8("decDeclinationGrpBx"))
        self.gridLayout_4 = QtGui.QGridLayout(self.decDeclinationGrpBx)
        self.gridLayout_4.setMargin(6)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label_5 = QtGui.QLabel(self.decDeclinationGrpBx)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_4.addWidget(self.label_5, 1, 0, 1, 2)
        self.decCurrentDblSpinBox = QtGui.QDoubleSpinBox(self.decDeclinationGrpBx)
        self.decCurrentDblSpinBox.setReadOnly(True)
        self.decCurrentDblSpinBox.setDecimals(5)
        self.decCurrentDblSpinBox.setMinimum(-180.0)
        self.decCurrentDblSpinBox.setMaximum(180.0)
        self.decCurrentDblSpinBox.setObjectName(_fromUtf8("decCurrentDblSpinBox"))
        self.gridLayout_4.addWidget(self.decCurrentDblSpinBox, 0, 1, 1, 1)
        self.label_10 = QtGui.QLabel(self.decDeclinationGrpBx)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_4.addWidget(self.label_10, 0, 0, 1, 1)
        self.frame_2 = QtGui.QFrame(self.decDeclinationGrpBx)
        self.frame_2.setFrameShape(QtGui.QFrame.Box)
        self.frame_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setMargin(6)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setContentsMargins(-1, -1, -1, 3)
        self.gridLayout_2.setHorizontalSpacing(3)
        self.gridLayout_2.setVerticalSpacing(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout_5 = QtGui.QGridLayout()
        self.gridLayout_5.setSpacing(3)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.label_17 = QtGui.QLabel(self.frame_2)
        self.label_17.setText(_fromUtf8(""))
        self.label_17.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/fossildigtools/icons/directional.svg")))
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.gridLayout_5.addWidget(self.label_17, 1, 0, 1, 1)
        self.label_14 = QtGui.QLabel(self.frame_2)
        self.label_14.setText(_fromUtf8(""))
        self.label_14.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/fossildigtools/icons/directional.svg")))
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout_5.addWidget(self.label_14, 1, 2, 1, 1)
        self.label_12 = QtGui.QLabel(self.frame_2)
        self.label_12.setText(_fromUtf8(""))
        self.label_12.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/fossildigtools/icons/directional.svg")))
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_5.addWidget(self.label_12, 2, 1, 1, 1)
        self.fromOriginIconLabel = QtGui.QLabel(self.frame_2)
        self.fromOriginIconLabel.setText(_fromUtf8(""))
        self.fromOriginIconLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/fossildigtools/icons/origin.svg")))
        self.fromOriginIconLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fromOriginIconLabel.setObjectName(_fromUtf8("fromOriginIconLabel"))
        self.gridLayout_5.addWidget(self.fromOriginIconLabel, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.frame_2)
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/fossildigtools/icons/directional.svg")))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_5.addWidget(self.label_2, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout_5, 2, 2, 1, 1)
        self.decEBearingDblSpnBx = QtGui.QDoubleSpinBox(self.frame_2)
        self.decEBearingDblSpnBx.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.decEBearingDblSpnBx.setReadOnly(True)
        self.decEBearingDblSpnBx.setDecimals(1)
        self.decEBearingDblSpnBx.setMinimum(0.0)
        self.decEBearingDblSpnBx.setMaximum(360.0)
        self.decEBearingDblSpnBx.setObjectName(_fromUtf8("decEBearingDblSpnBx"))
        self.gridLayout_2.addWidget(self.decEBearingDblSpnBx, 2, 4, 1, 1)
        self.label_18 = QtGui.QLabel(self.frame_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.gridLayout_2.addWidget(self.label_18, 2, 3, 1, 1)
        self.decSBearingDblSpnBx = QtGui.QDoubleSpinBox(self.frame_2)
        self.decSBearingDblSpnBx.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.decSBearingDblSpnBx.setReadOnly(True)
        self.decSBearingDblSpnBx.setDecimals(1)
        self.decSBearingDblSpnBx.setMinimum(0.0)
        self.decSBearingDblSpnBx.setMaximum(360.0)
        self.decSBearingDblSpnBx.setObjectName(_fromUtf8("decSBearingDblSpnBx"))
        self.gridLayout_2.addWidget(self.decSBearingDblSpnBx, 4, 2, 1, 1)
        self.label_19 = QtGui.QLabel(self.frame_2)
        self.label_19.setAlignment(QtCore.Qt.AlignCenter)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.gridLayout_2.addWidget(self.label_19, 3, 2, 1, 1)
        self.decNBearingDblSpnBx = QtGui.QDoubleSpinBox(self.frame_2)
        self.decNBearingDblSpnBx.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.decNBearingDblSpnBx.setReadOnly(True)
        self.decNBearingDblSpnBx.setDecimals(1)
        self.decNBearingDblSpnBx.setMinimum(0.0)
        self.decNBearingDblSpnBx.setMaximum(360.0)
        self.decNBearingDblSpnBx.setObjectName(_fromUtf8("decNBearingDblSpnBx"))
        self.gridLayout_2.addWidget(self.decNBearingDblSpnBx, 0, 2, 1, 1)
        self.decWBearingDblSpnBx = QtGui.QDoubleSpinBox(self.frame_2)
        self.decWBearingDblSpnBx.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.decWBearingDblSpnBx.setReadOnly(True)
        self.decWBearingDblSpnBx.setDecimals(1)
        self.decWBearingDblSpnBx.setMinimum(0.0)
        self.decWBearingDblSpnBx.setMaximum(360.0)
        self.decWBearingDblSpnBx.setObjectName(_fromUtf8("decWBearingDblSpnBx"))
        self.gridLayout_2.addWidget(self.decWBearingDblSpnBx, 2, 0, 1, 1)
        self.label_20 = QtGui.QLabel(self.frame_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy)
        self.label_20.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.gridLayout_2.addWidget(self.label_20, 2, 1, 1, 1)
        self.label_8 = QtGui.QLabel(self.frame_2)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_2.addWidget(self.label_8, 1, 2, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_2)
        self.gridLayout_4.addWidget(self.frame_2, 2, 0, 1, 2)
        self.verticalLayout_3.addWidget(self.decDeclinationGrpBx)
        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.label_21 = QtGui.QLabel(GeoMagDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy)
        self.label_21.setStyleSheet(_fromUtf8("QLabel {font-size: 0.75em;}"))
        self.label_21.setWordWrap(True)
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.verticalLayout.addWidget(self.label_21)
        self.buttonBox = QtGui.QDialogButtonBox(GeoMagDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(GeoMagDialog)
        QtCore.QMetaObject.connectSlotsByName(GeoMagDialog)
        GeoMagDialog.setTabOrder(self.decXDblSpinBx, self.decYDblSpinBx)
        GeoMagDialog.setTabOrder(self.decYDblSpinBx, self.buttonBox)

    def retranslateUi(self, GeoMagDialog):
        GeoMagDialog.setWindowTitle(_translate("GeoMagDialog", "Geomagnetic Declination", None))
        self.decLocGrpBx.setTitle(_translate("GeoMagDialog", "Location", None))
        self.label.setText(_translate("GeoMagDialog", "X", None))
        self.label_4.setText(_translate("GeoMagDialog", "Y", None))
        self.label_9.setText(_translate("GeoMagDialog", "Capture from map", None))
        self.captureLocBtn.setText(_translate("GeoMagDialog", "...", None))
        self.pinOriginLabel.setText(_translate("GeoMagDialog", "Origin", None))
        self.label_3.setText(_translate("GeoMagDialog", "Coords", None))
        self.label_6.setText(_translate("GeoMagDialog", "Elevation", None))
        self.decElevUnitsCmbBx.setItemText(0, _translate("GeoMagDialog", "ft", None))
        self.decElevUnitsCmbBx.setItemText(1, _translate("GeoMagDialog", "m", None))
        self.decDeclinationGrpBx.setTitle(_translate("GeoMagDialog", "Declination", None))
        self.label_5.setText(_translate("GeoMagDialog", "<html><head/><body><p>Magnetic bearings to <span style=\" font-weight:600; color:#4243fd;\">true</span> directions</p></body></html>", None))
        self.label_10.setText(_translate("GeoMagDialog", "Current (off true North)", None))
        self.decEBearingDblSpnBx.setSuffix(_translate("GeoMagDialog", "˚", None))
        self.label_18.setText(_translate("GeoMagDialog", "E", None))
        self.decSBearingDblSpnBx.setSuffix(_translate("GeoMagDialog", "˚", None))
        self.label_19.setText(_translate("GeoMagDialog", "S", None))
        self.decNBearingDblSpnBx.setSuffix(_translate("GeoMagDialog", "˚", None))
        self.decWBearingDblSpnBx.setSuffix(_translate("GeoMagDialog", "˚", None))
        self.label_20.setText(_translate("GeoMagDialog", "W", None))
        self.label_8.setText(_translate("GeoMagDialog", "N", None))
        self.label_21.setText(_translate("GeoMagDialog", "Note: map projection and coordinates must be in UTM (meters)", None))

import resources_rc
