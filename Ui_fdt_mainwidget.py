# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fdt_mainwidget.ui'
#
# Created: Mon Jul 22 18:21:55 2013
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

class Ui_MainWidget(object):
    def setupUi(self, MainWidget):
        MainWidget.setObjectName(_fromUtf8("MainWidget"))
        MainWidget.resize(473, 628)
        self.verticalLayout = QtGui.QVBoxLayout(MainWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.toolBarFrame = QtGui.QFrame(MainWidget)
        self.toolBarFrame.setFrameShape(QtGui.QFrame.NoFrame)
        self.toolBarFrame.setLineWidth(0)
        self.toolBarFrame.setObjectName(_fromUtf8("toolBarFrame"))
        self.toolBarFrameLayout = QtGui.QGridLayout(self.toolBarFrame)
        self.toolBarFrameLayout.setMargin(0)
        self.toolBarFrameLayout.setSpacing(0)
        self.toolBarFrameLayout.setObjectName(_fromUtf8("toolBarFrameLayout"))
        self.verticalLayout.addWidget(self.toolBarFrame)
        self.noticeLabel = QtGui.QLabel(MainWidget)
        self.noticeLabel.setStyleSheet(_fromUtf8("QLabel {color: rgb(199, 0, 0);}\n"
""))
        self.noticeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.noticeLabel.setObjectName(_fromUtf8("noticeLabel"))
        self.verticalLayout.addWidget(self.noticeLabel)
        self.tabWidget = QtGui.QTabWidget(MainWidget)
        self.tabWidget.setStyleSheet(_fromUtf8("QTabWidget::pane {\n"
"  border-top: 1px inset #C2C7CB;\n"
"  position: absolute;\n"
"  top: -0.5em;\n"
"  padding-top: 6px;}"))
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.gridsTab = QtGui.QWidget()
        self.gridsTab.setObjectName(_fromUtf8("gridsTab"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.gridsTab)
        self.verticalLayout_4.setContentsMargins(0, 3, 0, 0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.scrollArea = QtGui.QScrollArea(self.gridsTab)
        self.scrollArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 473, 563))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setMargin(6)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.originsGrpBx = QgsCollapsibleGroupBox(self.scrollAreaWidgetContents)
        self.originsGrpBx.setObjectName(_fromUtf8("originsGrpBx"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.originsGrpBx)
        self.verticalLayout_6.setMargin(6)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.gridLayout_9 = QtGui.QGridLayout()
        self.gridLayout_9.setVerticalSpacing(6)
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.originPinIconLabel = QtGui.QLabel(self.originsGrpBx)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.originPinIconLabel.sizePolicy().hasHeightForWidth())
        self.originPinIconLabel.setSizePolicy(sizePolicy)
        self.originPinIconLabel.setText(_fromUtf8(""))
        self.originPinIconLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/fossildigtools/icons/origin.svg")))
        self.originPinIconLabel.setObjectName(_fromUtf8("originPinIconLabel"))
        self.gridLayout_9.addWidget(self.originPinIconLabel, 0, 0, 1, 1)
        self.originPinLabel = QtGui.QLabel(self.originsGrpBx)
        self.originPinLabel.setObjectName(_fromUtf8("originPinLabel"))
        self.gridLayout_9.addWidget(self.originPinLabel, 0, 1, 1, 2)
        self.originPinCmbBx = QtGui.QComboBox(self.originsGrpBx)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.originPinCmbBx.sizePolicy().hasHeightForWidth())
        self.originPinCmbBx.setSizePolicy(sizePolicy)
        self.originPinCmbBx.setObjectName(_fromUtf8("originPinCmbBx"))
        self.gridLayout_9.addWidget(self.originPinCmbBx, 1, 0, 1, 2)
        self.originEditFrame = QtGui.QFrame(self.originsGrpBx)
        self.originEditFrame.setObjectName(_fromUtf8("originEditFrame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.originEditFrame)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.originPinEditBtn = QtGui.QToolButton(self.originEditFrame)
        self.originPinEditBtn.setMaximumSize(QtCore.QSize(16777215, 24))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/fossildigtools/icons/edit.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.originPinEditBtn.setIcon(icon)
        self.originPinEditBtn.setIconSize(QtCore.QSize(20, 20))
        self.originPinEditBtn.setObjectName(_fromUtf8("originPinEditBtn"))
        self.horizontalLayout.addWidget(self.originPinEditBtn)
        self.originPinRemoveBtn = QtGui.QToolButton(self.originEditFrame)
        self.originPinRemoveBtn.setMaximumSize(QtCore.QSize(16777215, 24))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/fossildigtools/icons/remove.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.originPinRemoveBtn.setIcon(icon1)
        self.originPinRemoveBtn.setIconSize(QtCore.QSize(20, 20))
        self.originPinRemoveBtn.setObjectName(_fromUtf8("originPinRemoveBtn"))
        self.horizontalLayout.addWidget(self.originPinRemoveBtn)
        self.originPinGoToBtn = QtGui.QToolButton(self.originEditFrame)
        self.originPinGoToBtn.setMaximumSize(QtCore.QSize(16777215, 24))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/fossildigtools/icons/goto.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.originPinGoToBtn.setIcon(icon2)
        self.originPinGoToBtn.setIconSize(QtCore.QSize(20, 20))
        self.originPinGoToBtn.setObjectName(_fromUtf8("originPinGoToBtn"))
        self.horizontalLayout.addWidget(self.originPinGoToBtn)
        self.gridLayout_9.addWidget(self.originEditFrame, 2, 1, 1, 1)
        self.originPinAddBtn = QtGui.QToolButton(self.originsGrpBx)
        self.originPinAddBtn.setMaximumSize(QtCore.QSize(16777215, 24))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/fossildigtools/icons/add.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.originPinAddBtn.setIcon(icon3)
        self.originPinAddBtn.setIconSize(QtCore.QSize(20, 20))
        self.originPinAddBtn.setObjectName(_fromUtf8("originPinAddBtn"))
        self.gridLayout_9.addWidget(self.originPinAddBtn, 1, 2, 1, 1)
        self.directPinFrame = QtGui.QFrame(self.originsGrpBx)
        self.directPinFrame.setObjectName(_fromUtf8("directPinFrame"))
        self.gridLayout_6 = QtGui.QGridLayout(self.directPinFrame)
        self.gridLayout_6.setMargin(0)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.directPinList = QtGui.QListWidget(self.directPinFrame)
        self.directPinList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.directPinList.setObjectName(_fromUtf8("directPinList"))
        self.gridLayout_6.addWidget(self.directPinList, 1, 2, 2, 1)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.directPinAddBtn = QtGui.QToolButton(self.directPinFrame)
        self.directPinAddBtn.setMaximumSize(QtCore.QSize(16777215, 24))
        self.directPinAddBtn.setIcon(icon3)
        self.directPinAddBtn.setIconSize(QtCore.QSize(20, 20))
        self.directPinAddBtn.setObjectName(_fromUtf8("directPinAddBtn"))
        self.verticalLayout_8.addWidget(self.directPinAddBtn)
        self.directPinEditFrame = QtGui.QFrame(self.directPinFrame)
        self.directPinEditFrame.setObjectName(_fromUtf8("directPinEditFrame"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.directPinEditFrame)
        self.verticalLayout_7.setMargin(0)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.directPinEditBtn = QtGui.QToolButton(self.directPinEditFrame)
        self.directPinEditBtn.setMaximumSize(QtCore.QSize(16777215, 24))
        self.directPinEditBtn.setIcon(icon)
        self.directPinEditBtn.setIconSize(QtCore.QSize(20, 20))
        self.directPinEditBtn.setObjectName(_fromUtf8("directPinEditBtn"))
        self.verticalLayout_7.addWidget(self.directPinEditBtn)
        self.directPinRemoveBtn = QtGui.QToolButton(self.directPinEditFrame)
        self.directPinRemoveBtn.setMaximumSize(QtCore.QSize(16777215, 24))
        self.directPinRemoveBtn.setIcon(icon1)
        self.directPinRemoveBtn.setIconSize(QtCore.QSize(20, 20))
        self.directPinRemoveBtn.setObjectName(_fromUtf8("directPinRemoveBtn"))
        self.verticalLayout_7.addWidget(self.directPinRemoveBtn)
        self.directPinGoToBtn = QtGui.QToolButton(self.directPinEditFrame)
        self.directPinGoToBtn.setMaximumSize(QtCore.QSize(16777215, 24))
        self.directPinGoToBtn.setIcon(icon2)
        self.directPinGoToBtn.setIconSize(QtCore.QSize(20, 20))
        self.directPinGoToBtn.setObjectName(_fromUtf8("directPinGoToBtn"))
        self.verticalLayout_7.addWidget(self.directPinGoToBtn)
        self.verticalLayout_8.addWidget(self.directPinEditFrame)
        self.gridLayout_6.addLayout(self.verticalLayout_8, 1, 3, 1, 1)
        self.directPinIconLabel = QtGui.QLabel(self.directPinFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.directPinIconLabel.sizePolicy().hasHeightForWidth())
        self.directPinIconLabel.setSizePolicy(sizePolicy)
        self.directPinIconLabel.setText(_fromUtf8(""))
        self.directPinIconLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/fossildigtools/icons/directional.svg")))
        self.directPinIconLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.directPinIconLabel.setObjectName(_fromUtf8("directPinIconLabel"))
        self.gridLayout_6.addWidget(self.directPinIconLabel, 0, 0, 1, 1)
        self.directPinLabel = QtGui.QLabel(self.directPinFrame)
        self.directPinLabel.setObjectName(_fromUtf8("directPinLabel"))
        self.gridLayout_6.addWidget(self.directPinLabel, 0, 2, 1, 2)
        self.gridLayout_9.addWidget(self.directPinFrame, 3, 0, 1, 3)
        self.verticalLayout_6.addLayout(self.gridLayout_9)
        self.verticalLayout_3.addWidget(self.originsGrpBx)
        self.gridsGrpBx = QgsCollapsibleGroupBox(self.scrollAreaWidgetContents)
        self.gridsGrpBx.setObjectName(_fromUtf8("gridsGrpBx"))
        self.gridLayout_4 = QtGui.QGridLayout(self.gridsGrpBx)
        self.gridLayout_4.setMargin(6)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.gridFrame = QtGui.QFrame(self.gridsGrpBx)
        self.gridFrame.setObjectName(_fromUtf8("gridFrame"))
        self.gridLayout_3 = QtGui.QGridLayout(self.gridFrame)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setSpacing(3)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.addGridSEBtn = QtGui.QToolButton(self.gridFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addGridSEBtn.sizePolicy().hasHeightForWidth())
        self.addGridSEBtn.setSizePolicy(sizePolicy)
        self.addGridSEBtn.setMinimumSize(QtCore.QSize(40, 0))
        self.addGridSEBtn.setCheckable(True)
        self.addGridSEBtn.setObjectName(_fromUtf8("addGridSEBtn"))
        self.addGridBtnGrp = QtGui.QButtonGroup(MainWidget)
        self.addGridBtnGrp.setObjectName(_fromUtf8("addGridBtnGrp"))
        self.addGridBtnGrp.addButton(self.addGridSEBtn)
        self.gridLayout_3.addWidget(self.addGridSEBtn, 3, 3, 1, 1)
        self.addGridSBtn = QtGui.QToolButton(self.gridFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addGridSBtn.sizePolicy().hasHeightForWidth())
        self.addGridSBtn.setSizePolicy(sizePolicy)
        self.addGridSBtn.setMinimumSize(QtCore.QSize(40, 0))
        self.addGridSBtn.setCheckable(True)
        self.addGridSBtn.setObjectName(_fromUtf8("addGridSBtn"))
        self.addGridBtnGrp.addButton(self.addGridSBtn)
        self.gridLayout_3.addWidget(self.addGridSBtn, 3, 2, 1, 1)
        self.addGridSWBtn = QtGui.QToolButton(self.gridFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addGridSWBtn.sizePolicy().hasHeightForWidth())
        self.addGridSWBtn.setSizePolicy(sizePolicy)
        self.addGridSWBtn.setMinimumSize(QtCore.QSize(40, 0))
        self.addGridSWBtn.setCheckable(True)
        self.addGridSWBtn.setObjectName(_fromUtf8("addGridSWBtn"))
        self.addGridBtnGrp.addButton(self.addGridSWBtn)
        self.gridLayout_3.addWidget(self.addGridSWBtn, 3, 1, 1, 1)
        self.addGridNEBtn = QtGui.QToolButton(self.gridFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addGridNEBtn.sizePolicy().hasHeightForWidth())
        self.addGridNEBtn.setSizePolicy(sizePolicy)
        self.addGridNEBtn.setMinimumSize(QtCore.QSize(40, 0))
        self.addGridNEBtn.setCheckable(True)
        self.addGridNEBtn.setObjectName(_fromUtf8("addGridNEBtn"))
        self.addGridBtnGrp.addButton(self.addGridNEBtn)
        self.gridLayout_3.addWidget(self.addGridNEBtn, 1, 3, 1, 1)
        self.addGridNBtn = QtGui.QToolButton(self.gridFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addGridNBtn.sizePolicy().hasHeightForWidth())
        self.addGridNBtn.setSizePolicy(sizePolicy)
        self.addGridNBtn.setMinimumSize(QtCore.QSize(40, 0))
        self.addGridNBtn.setCheckable(True)
        self.addGridNBtn.setObjectName(_fromUtf8("addGridNBtn"))
        self.addGridBtnGrp.addButton(self.addGridNBtn)
        self.gridLayout_3.addWidget(self.addGridNBtn, 1, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(6, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 2, 4, 1, 1)
        self.gridsAddBtn = QtGui.QToolButton(self.gridFrame)
        self.gridsAddBtn.setMaximumSize(QtCore.QSize(16777215, 24))
        self.gridsAddBtn.setText(_fromUtf8("+"))
        self.gridsAddBtn.setIcon(icon3)
        self.gridsAddBtn.setIconSize(QtCore.QSize(20, 20))
        self.gridsAddBtn.setObjectName(_fromUtf8("gridsAddBtn"))
        self.gridLayout_3.addWidget(self.gridsAddBtn, 2, 5, 1, 1)
        self.addGridIconLabel = QtGui.QLabel(self.gridFrame)
        self.addGridIconLabel.setText(_fromUtf8(""))
        self.addGridIconLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/fossildigtools/icons/origin.svg")))
        self.addGridIconLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.addGridIconLabel.setObjectName(_fromUtf8("addGridIconLabel"))
        self.gridLayout_3.addWidget(self.addGridIconLabel, 2, 2, 1, 1)
        self.addGridEBtn = QtGui.QToolButton(self.gridFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addGridEBtn.sizePolicy().hasHeightForWidth())
        self.addGridEBtn.setSizePolicy(sizePolicy)
        self.addGridEBtn.setMinimumSize(QtCore.QSize(40, 0))
        self.addGridEBtn.setCheckable(True)
        self.addGridEBtn.setObjectName(_fromUtf8("addGridEBtn"))
        self.addGridBtnGrp.addButton(self.addGridEBtn)
        self.gridLayout_3.addWidget(self.addGridEBtn, 2, 3, 1, 1)
        self.addGridWBtn = QtGui.QToolButton(self.gridFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addGridWBtn.sizePolicy().hasHeightForWidth())
        self.addGridWBtn.setSizePolicy(sizePolicy)
        self.addGridWBtn.setMinimumSize(QtCore.QSize(40, 0))
        self.addGridWBtn.setCheckable(True)
        self.addGridWBtn.setObjectName(_fromUtf8("addGridWBtn"))
        self.addGridBtnGrp.addButton(self.addGridWBtn)
        self.gridLayout_3.addWidget(self.addGridWBtn, 2, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(6, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 2, 0, 1, 1)
        self.addGridNWBtn = QtGui.QToolButton(self.gridFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addGridNWBtn.sizePolicy().hasHeightForWidth())
        self.addGridNWBtn.setSizePolicy(sizePolicy)
        self.addGridNWBtn.setMinimumSize(QtCore.QSize(40, 0))
        self.addGridNWBtn.setCheckable(True)
        self.addGridNWBtn.setObjectName(_fromUtf8("addGridNWBtn"))
        self.addGridBtnGrp.addButton(self.addGridNWBtn)
        self.gridLayout_3.addWidget(self.addGridNWBtn, 1, 1, 1, 1)
        self.addGridFrame = QtGui.QFrame(self.gridFrame)
        self.addGridFrame.setObjectName(_fromUtf8("addGridFrame"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.addGridFrame)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.addGridLabel = QtGui.QLabel(self.addGridFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addGridLabel.sizePolicy().hasHeightForWidth())
        self.addGridLabel.setSizePolicy(sizePolicy)
        self.addGridLabel.setObjectName(_fromUtf8("addGridLabel"))
        self.horizontalLayout_2.addWidget(self.addGridLabel)
        self.addGridGridRadio = QtGui.QRadioButton(self.addGridFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addGridGridRadio.sizePolicy().hasHeightForWidth())
        self.addGridGridRadio.setSizePolicy(sizePolicy)
        self.addGridGridRadio.setObjectName(_fromUtf8("addGridGridRadio"))
        self.addGridRadioGrp = QtGui.QButtonGroup(MainWidget)
        self.addGridRadioGrp.setObjectName(_fromUtf8("addGridRadioGrp"))
        self.addGridRadioGrp.addButton(self.addGridGridRadio)
        self.horizontalLayout_2.addWidget(self.addGridGridRadio)
        self.addGridOriginRadio = QtGui.QRadioButton(self.addGridFrame)
        self.addGridOriginRadio.setChecked(True)
        self.addGridOriginRadio.setObjectName(_fromUtf8("addGridOriginRadio"))
        self.addGridRadioGrp.addButton(self.addGridOriginRadio)
        self.horizontalLayout_2.addWidget(self.addGridOriginRadio)
        self.gridLayout_3.addWidget(self.addGridFrame, 0, 0, 1, 6)
        self.gridLayout_4.addWidget(self.gridFrame, 3, 0, 1, 1)
        self.gridLayout_5 = QtGui.QGridLayout()
        self.gridLayout_5.setVerticalSpacing(0)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.gridsCmbBx = QtGui.QComboBox(self.gridsGrpBx)
        self.gridsCmbBx.setObjectName(_fromUtf8("gridsCmbBx"))
        self.gridLayout_5.addWidget(self.gridsCmbBx, 0, 1, 1, 1)
        self.gridsEditFrame = QtGui.QFrame(self.gridsGrpBx)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gridsEditFrame.sizePolicy().hasHeightForWidth())
        self.gridsEditFrame.setSizePolicy(sizePolicy)
        self.gridsEditFrame.setFrameShape(QtGui.QFrame.NoFrame)
        self.gridsEditFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.gridsEditFrame.setObjectName(_fromUtf8("gridsEditFrame"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.gridsEditFrame)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.gridsEditBtn = QtGui.QToolButton(self.gridsEditFrame)
        self.gridsEditBtn.setMaximumSize(QtCore.QSize(16777215, 24))
        self.gridsEditBtn.setIcon(icon)
        self.gridsEditBtn.setIconSize(QtCore.QSize(20, 20))
        self.gridsEditBtn.setObjectName(_fromUtf8("gridsEditBtn"))
        self.horizontalLayout_4.addWidget(self.gridsEditBtn)
        self.gridsRemoveBtn = QtGui.QToolButton(self.gridsEditFrame)
        self.gridsRemoveBtn.setMaximumSize(QtCore.QSize(16777215, 24))
        self.gridsRemoveBtn.setIcon(icon1)
        self.gridsRemoveBtn.setIconSize(QtCore.QSize(20, 20))
        self.gridsRemoveBtn.setObjectName(_fromUtf8("gridsRemoveBtn"))
        self.horizontalLayout_4.addWidget(self.gridsRemoveBtn)
        self.gridsGoToBtn = QtGui.QToolButton(self.gridsEditFrame)
        self.gridsGoToBtn.setMaximumSize(QtCore.QSize(16777215, 24))
        self.gridsGoToBtn.setIcon(icon2)
        self.gridsGoToBtn.setIconSize(QtCore.QSize(20, 20))
        self.gridsGoToBtn.setObjectName(_fromUtf8("gridsGoToBtn"))
        self.horizontalLayout_4.addWidget(self.gridsGoToBtn)
        self.gridLayout_5.addWidget(self.gridsEditFrame, 0, 2, 1, 1)
        self.gridsIconLabel = QtGui.QLabel(self.gridsGrpBx)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gridsIconLabel.sizePolicy().hasHeightForWidth())
        self.gridsIconLabel.setSizePolicy(sizePolicy)
        self.gridsIconLabel.setText(_fromUtf8(""))
        self.gridsIconLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/fossildigtools/icons/grid.svg")))
        self.gridsIconLabel.setObjectName(_fromUtf8("gridsIconLabel"))
        self.gridLayout_5.addWidget(self.gridsIconLabel, 0, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_5, 0, 0, 1, 1)
        self.gridsAllFrame = QtGui.QFrame(self.gridsGrpBx)
        self.gridsAllFrame.setObjectName(_fromUtf8("gridsAllFrame"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.gridsAllFrame)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.gridsZoomToAllBtn = QtGui.QToolButton(self.gridsAllFrame)
        self.gridsZoomToAllBtn.setMaximumSize(QtCore.QSize(16777215, 24))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/fossildigtools/icons/zoom-grids.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.gridsZoomToAllBtn.setIcon(icon4)
        self.gridsZoomToAllBtn.setIconSize(QtCore.QSize(20, 20))
        self.gridsZoomToAllBtn.setObjectName(_fromUtf8("gridsZoomToAllBtn"))
        self.horizontalLayout_3.addWidget(self.gridsZoomToAllBtn)
        self.label_2 = QtGui.QLabel(self.gridsAllFrame)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.label = QtGui.QLabel(self.gridsAllFrame)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        self.gridsRemoveAllBtn = QtGui.QToolButton(self.gridsAllFrame)
        self.gridsRemoveAllBtn.setMaximumSize(QtCore.QSize(16777215, 24))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/fossildigtools/icons/remove-all.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.gridsRemoveAllBtn.setIcon(icon5)
        self.gridsRemoveAllBtn.setIconSize(QtCore.QSize(20, 20))
        self.gridsRemoveAllBtn.setObjectName(_fromUtf8("gridsRemoveAllBtn"))
        self.horizontalLayout_3.addWidget(self.gridsRemoveAllBtn)
        self.gridLayout_4.addWidget(self.gridsAllFrame, 4, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.gridsGrpBx)
        spacerItem2 = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_4.addWidget(self.scrollArea)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/fossildigtools/icons/grid.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.gridsTab, icon6, _fromUtf8(""))
        self.featuresTab = QtGui.QWidget()
        self.featuresTab.setObjectName(_fromUtf8("featuresTab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.featuresTab)
        self.verticalLayout_2.setContentsMargins(0, 3, 0, 0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.scrollArea_2 = QtGui.QScrollArea(self.featuresTab)
        self.scrollArea_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName(_fromUtf8("scrollArea_2"))
        self.scrollAreaWidgetContents_2 = QtGui.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 473, 563))
        self.scrollAreaWidgetContents_2.setObjectName(_fromUtf8("scrollAreaWidgetContents_2"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_5.setMargin(6)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.arrangeGrpBox = QgsCollapsibleGroupBox(self.scrollAreaWidgetContents_2)
        self.arrangeGrpBox.setObjectName(_fromUtf8("arrangeGrpBox"))
        self.gridLayout = QtGui.QGridLayout(self.arrangeGrpBox)
        self.gridLayout.setMargin(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.arrangeRaiseBtn = QtGui.QToolButton(self.arrangeGrpBox)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/fossildigtools/icons/arrange-raise.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.arrangeRaiseBtn.setIcon(icon7)
        self.arrangeRaiseBtn.setIconSize(QtCore.QSize(20, 20))
        self.arrangeRaiseBtn.setObjectName(_fromUtf8("arrangeRaiseBtn"))
        self.gridLayout.addWidget(self.arrangeRaiseBtn, 0, 0, 1, 1)
        self.arrangeLowerBtn = QtGui.QToolButton(self.arrangeGrpBox)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/fossildigtools/icons/arrange-lower.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.arrangeLowerBtn.setIcon(icon8)
        self.arrangeLowerBtn.setIconSize(QtCore.QSize(20, 20))
        self.arrangeLowerBtn.setObjectName(_fromUtf8("arrangeLowerBtn"))
        self.gridLayout.addWidget(self.arrangeLowerBtn, 0, 1, 1, 1)
        self.arrangeToTopBtn = QtGui.QToolButton(self.arrangeGrpBox)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/fossildigtools/icons/arrange-to-top.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.arrangeToTopBtn.setIcon(icon9)
        self.arrangeToTopBtn.setIconSize(QtCore.QSize(20, 20))
        self.arrangeToTopBtn.setObjectName(_fromUtf8("arrangeToTopBtn"))
        self.gridLayout.addWidget(self.arrangeToTopBtn, 0, 2, 1, 1)
        self.arrangeToBottomBtn = QtGui.QToolButton(self.arrangeGrpBox)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/fossildigtools/icons/arrange-to-bottom.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.arrangeToBottomBtn.setIcon(icon10)
        self.arrangeToBottomBtn.setIconSize(QtCore.QSize(20, 20))
        self.arrangeToBottomBtn.setObjectName(_fromUtf8("arrangeToBottomBtn"))
        self.gridLayout.addWidget(self.arrangeToBottomBtn, 0, 3, 1, 1)
        self.verticalLayout_5.addWidget(self.arrangeGrpBox)
        self.attributesGrpBox = QgsCollapsibleGroupBox(self.scrollAreaWidgetContents_2)
        self.attributesGrpBox.setObjectName(_fromUtf8("attributesGrpBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.attributesGrpBox)
        self.gridLayout_2.setMargin(6)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.attributesOpenFormBtn = QtGui.QPushButton(self.attributesGrpBox)
        self.attributesOpenFormBtn.setObjectName(_fromUtf8("attributesOpenFormBtn"))
        self.gridLayout_2.addWidget(self.attributesOpenFormBtn, 0, 0, 1, 1)
        self.verticalLayout_5.addWidget(self.attributesGrpBox)
        spacerItem3 = QtGui.QSpacerItem(20, 445, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem3)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_2.addWidget(self.scrollArea_2)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/fossildigtools/icons/bone.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.featuresTab, icon11, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi(MainWidget)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWidget)

    def retranslateUi(self, MainWidget):
        MainWidget.setWindowTitle(_translate("MainWidget", "Fossil Dig Tools", None))
        self.noticeLabel.setText(_translate("MainWidget", "Notice", None))
        self.originsGrpBx.setTitle(_translate("MainWidget", "Location pins", None))
        self.originPinLabel.setText(_translate("MainWidget", "Origin pins", None))
        self.originPinEditBtn.setToolTip(_translate("MainWidget", "Edit origin pin", None))
        self.originPinEditBtn.setText(_translate("MainWidget", "...", None))
        self.originPinRemoveBtn.setToolTip(_translate("MainWidget", "Remove origin pin", None))
        self.originPinRemoveBtn.setText(_translate("MainWidget", "...", None))
        self.originPinGoToBtn.setToolTip(_translate("MainWidget", "Go to origin pin", None))
        self.originPinGoToBtn.setText(_translate("MainWidget", "...", None))
        self.originPinAddBtn.setToolTip(_translate("MainWidget", "Add origin pin", None))
        self.originPinAddBtn.setText(_translate("MainWidget", "...", None))
        self.directPinList.setSortingEnabled(True)
        self.directPinAddBtn.setToolTip(_translate("MainWidget", "Add directional pin", None))
        self.directPinAddBtn.setText(_translate("MainWidget", "...", None))
        self.directPinEditBtn.setToolTip(_translate("MainWidget", "Edit directional pin", None))
        self.directPinEditBtn.setText(_translate("MainWidget", "...", None))
        self.directPinRemoveBtn.setToolTip(_translate("MainWidget", "Remove directional pin", None))
        self.directPinRemoveBtn.setText(_translate("MainWidget", "...", None))
        self.directPinGoToBtn.setToolTip(_translate("MainWidget", "Go to directional pin", None))
        self.directPinGoToBtn.setText(_translate("MainWidget", "...", None))
        self.directPinLabel.setText(_translate("MainWidget", "Directional pins", None))
        self.gridsGrpBx.setTitle(_translate("MainWidget", "Grids", None))
        self.addGridSEBtn.setText(_translate("MainWidget", "SE", None))
        self.addGridSBtn.setText(_translate("MainWidget", "S", None))
        self.addGridSWBtn.setText(_translate("MainWidget", "SW", None))
        self.addGridNEBtn.setText(_translate("MainWidget", "NE", None))
        self.addGridNBtn.setText(_translate("MainWidget", "N", None))
        self.gridsAddBtn.setToolTip(_translate("MainWidget", "Add grid(s)", None))
        self.addGridEBtn.setText(_translate("MainWidget", "E", None))
        self.addGridWBtn.setText(_translate("MainWidget", "W", None))
        self.addGridNWBtn.setText(_translate("MainWidget", "NW", None))
        self.addGridLabel.setText(_translate("MainWidget", "Add around ", None))
        self.addGridGridRadio.setText(_translate("MainWidget", "grid", None))
        self.addGridOriginRadio.setText(_translate("MainWidget", "origin", None))
        self.gridsEditBtn.setToolTip(_translate("MainWidget", "Edit directional pin", None))
        self.gridsEditBtn.setText(_translate("MainWidget", "...", None))
        self.gridsRemoveBtn.setToolTip(_translate("MainWidget", "Remove grid", None))
        self.gridsRemoveBtn.setText(_translate("MainWidget", "-", None))
        self.gridsGoToBtn.setToolTip(_translate("MainWidget", "Go to grid", None))
        self.gridsGoToBtn.setText(_translate("MainWidget", "...", None))
        self.gridsZoomToAllBtn.setToolTip(_translate("MainWidget", "Zoom to all grids extent", None))
        self.gridsZoomToAllBtn.setText(_translate("MainWidget", "-", None))
        self.label_2.setText(_translate("MainWidget", "Zoom all", None))
        self.label.setText(_translate("MainWidget", "Delete all", None))
        self.gridsRemoveAllBtn.setToolTip(_translate("MainWidget", "Remove all grids for current origin", None))
        self.gridsRemoveAllBtn.setText(_translate("MainWidget", "-", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.gridsTab), _translate("MainWidget", "Grids", None))
        self.arrangeGrpBox.setTitle(_translate("MainWidget", "Arrange", None))
        self.arrangeRaiseBtn.setToolTip(_translate("MainWidget", "Move up", None))
        self.arrangeRaiseBtn.setText(_translate("MainWidget", "...", None))
        self.arrangeLowerBtn.setToolTip(_translate("MainWidget", "Move down", None))
        self.arrangeLowerBtn.setText(_translate("MainWidget", "...", None))
        self.arrangeToTopBtn.setToolTip(_translate("MainWidget", "Move to top", None))
        self.arrangeToTopBtn.setText(_translate("MainWidget", "...", None))
        self.arrangeToBottomBtn.setToolTip(_translate("MainWidget", "Move to bottom", None))
        self.arrangeToBottomBtn.setText(_translate("MainWidget", "...", None))
        self.attributesGrpBox.setTitle(_translate("MainWidget", "Atrributes", None))
        self.attributesOpenFormBtn.setText(_translate("MainWidget", "Open attribute form", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.featuresTab), _translate("MainWidget", "Features", None))

from qgis.gui import QgsCollapsibleGroupBox
import resources_rc
