# -*- coding: utf-8 -*-
"""
/***************************************************************************
 FossilDigTools
                                 A QGIS plugin
 Interface and tools to help illustrate fossil digs
                             -------------------
        begin                : 2013-07-02
        copyright            : (C) 2013 by Larry Shaffer / BHIGR
        email                : larrys@bhigr.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


def name():
    return "Fossil Dig Tools"


def description():
    return "Interface and tools to help illustrate fossil digs"


def version():
    return "Version 0.1"


def icon():
    return "icon.png"


def qgisMinimumVersion():
    return "2.0"

def author():
    return "Larry Shaffer / BHIGR"

def email():
    return "larrys@bhigr.com"

def classFactory(iface):
    # load FossilDigTools class from file FossilDigTools
    from fossildigtools import FossilDigTools
    return FossilDigTools(iface)
