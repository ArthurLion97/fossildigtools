#/***************************************************************************
# FossilDigTools
#
# Interface and tools to help illustrate fossil digs
#                             -------------------
#        begin                : 2013-07-02
#        copyright            : (C) 2013 by Larry Shaffer / BHIGR
#        email                : larrys@bhigr.com
# ***************************************************************************/
#
#/***************************************************************************
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or     *
# *   (at your option) any later version.                                   *
# *                                                                         *
# ***************************************************************************/

PLUGINNAME = fossildigtools
PLUGIN_UIDIR = $(HOME)/.qgis2/python/plugins/$(PLUGINNAME)/ui

UI_FILES = Ui_fdt_geomagdlg.py \
Ui_fdt_mainwidget.py \
Ui_fdt_pindlg.py \
Ui_fdt_settingsdlg.py

RESOURCE_FILES = resources_rc.py

PY_FILES = __init__.py

default: compile

compile: $(UI_FILES) $(RESOURCE_FILES)

Ui_%.py : %.ui
	/usr/local/bin/pyuic4 -x --from-imports -o Ui_$*.py $<

%_rc.py : %.qrc
	/usr/local/bin/pyrcc4 -o $*_rc.py  $<

deploy:
	mkdir -p $(PLUGIN_UIDIR)
	cp -vRf $(PY_FILES) $(PLUGIN_UIDIR)
	cp -vf $(CURDIR)/Ui_*.py $(PLUGIN_UIDIR)
	cp -vf $(CURDIR)/*_rc.py $(PLUGIN_UIDIR)
	mkdir -p $(PLUGIN_UIDIR)/icons
	cp -vf $(CURDIR)/icons/*.svg $(PLUGIN_UIDIR)/icons

