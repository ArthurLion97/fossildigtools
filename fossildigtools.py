# -*- coding: utf-8 -*-
"""
/***************************************************************************
 FossilDigTools
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

import os.path

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import ui.resources_rc

from fdt_mainwidget import FdtMainWidget


class FossilDigTools:

    def __init__(self, iface):
        # save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n',
                                  'fossildigtools_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

    def initGui(self):
        # create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/fossildigtools/icon.png"),
            u"Fossil Dig Tools", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&Fossil Dig Tools", self.action)

        # load custom settings
        self.settings = QSettings("bhigr", "fossildigtools")

        # add dock widget
        self.dockWidget = QDockWidget(u"Fossil Dig Tools",
                                      self.iface.mainWindow())
        self.toolswidget = FdtMainWidget(self.dockWidget,
                                         self.iface,
                                         self.settings)
        self.dockWidget.setWidget(self.toolswidget)
        self.dockWidget.layout().setContentsMargins(0, 0, 0, 0)
        self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget)

    def unload(self):
        # remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Fossil Dig Tools", self.action)
        self.iface.removeToolBarIcon(self.action)

        # clear out any signal/slot connections
        self.toolswidget.remove_layer_connections()

        self.settings.setValue("currentTab",
                               self.toolswidget.tabWidget.currentIndex())

        self.dockWidget.setParent(None)  # remove parent for garbage collection
        del self.dockWidget

    # run method that performs all the real work
    def run(self):
        # toggle the dock
        self.toggleDockWidget()

    def toggleDockWidget(self):
        self.dockWidget.setVisible(not self.dockWidget.isVisible())
