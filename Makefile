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

# CONFIGURATION
PLUGIN_UPLOAD = $(CURDIR)/plugin_upload.py

# Makefile for a P.qgis2 plugin

# translation
SOURCES = fossildigtools.py __init__.py fossildigtoolsdialog.py
#TRANSLATIONS = i18n/fossildigtools_en.ts
TRANSLATIONS =

# global
PLUGINNAME = fossildigtools
PLUGIN_DIR = $(HOME)/.qgis2/python/plugins/$(PLUGINNAME)

PY_FILES = __init__.py \
fdt_emitpoint.py \
fdt_geomagdlg.py \
fdt_mainwidget.py \
fdt_pindlg.py \
fdt_settingsdlg.py \
fdt_utils.py \
fossildigtools.py

EXTRAS = icon.png \
metadata.txt \
geomag

RESOURCE_FILES =

HELP = help/build/html

default: compile

compile: uifiles $(RESOURCE_FILES)

# make ui subdir
uifiles:
	$(MAKE) -C ui

%_rc.py : %.qrc
	/usr/local/bin/pyrcc4 -o $*_rc.py  $<

%.qm : %.ts
	/usr/bin/lrelease $<

# The deploy  target only works on unix like operating system where
# the Python plugin directory is located at:
# $HOME/.qgis2/python/plugins
# deploy: compile doc transcompile
deploy: compile deploy-uifiles
	mkdir -p $(PLUGIN_DIR)
	cp -vf $(PY_FILES) $(PLUGIN_DIR)
	cp -vRf $(EXTRAS) $(PLUGIN_DIR)

# 	cp -vf $(RESOURCE_FILES) $(PLUGIN_DIR)
#	cp -vfr i18n $(PLUGIN_DIR)
#	cp -vfr $(HELP) $(PLUGIN_DIR)/help

# deploy ui subdir
deploy-uifiles:
	$(MAKE) deploy -C ui

# The dclean target removes compiled python files from plugin directory
# also deletes any .git entries
dclean:
	find $(PLUGIN_DIR) -iname "*.pyc" -delete
	find $(PLUGIN_DIR) -iname ".git" -prune -exec rm -Rf {} \;

# The derase deletes deployed plugin
derase:
	rm -Rf $(PLUGIN_DIR)

# The zip target deploys the plugin and creates a zip file with the deployed
# content. You can then upload the zip file on http://plugins.qgis2.org
zip: deploy dclean
	rm -f $(PLUGINNAME).zip
	cd $(HOME)/.qgis2/python/plugins && zip -9r $(CURDIR)/$(PLUGINNAME).zip $(PLUGINNAME)
	mv -f $(PLUGINNAME).zip $(HOME)/Dropbox-Personal/Dropbox/QGIS/fossildigtools

# Create a zip package of the plugin named $(PLUGINNAME).zip.
# This requires use of git (your plugin development directory must be a
# git repository).
# To use, pass a valid commit or tag as follows:
#   make package VERSION=Version_0.3.2
package: compile
		rm -f $(PLUGINNAME).zip
		git archive --prefix=$(PLUGINNAME)/ -o $(PLUGINNAME).zip $(VERSION)
		echo "Created package: $(PLUGINNAME).zip"

upload: zip
	$(PLUGIN_UPLOAD) $(PLUGINNAME).zip

# transup
# update .ts translation files
transup:
	pylupdate4 Makefile

# transcompile
# compile translation files into .qm binary format
transcompile: $(TRANSLATIONS:.ts=.qm)

# transclean
# deletes all .qm files
transclean:
	rm -f i18n/*.qm

clean:
	rm $(RESOURCE_FILES)

# build documentation with sphinx
doc:
	cd help; make html
