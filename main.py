#!/usr/bin/python
# -*- coding: utf-8 -*-
## Copyright (c) 2017, The Sumokoin Project (www.sumokoin.org)
## Copyright (c) 2018, The OMBRE Project

import os

import sys, os, hashlib
from PySide import QtCore

from PySide.QtGui import QMessageBox

from app.QSingleApplication import QSingleApplication
from utils.common import DummyStream, getAppPath, readFile
from settings import APP_NAME

from app.hub import Hub
from webui import MainWebUI


def main():
    if getattr(sys, "frozen", False) and sys.platform in ['win32','cygwin','win64']:
        # and now redirect all default streams to DummyStream:
        sys.stdout = DummyStream()
        sys.stderr = DummyStream()
        sys.stdin = DummyStream()
        sys.__stdout__ = DummyStream()
        sys.__stderr__ = DummyStream()
        sys.__stdin__ = DummyStream()

    # Get application path

    abspath = os.path.abspath(__file__)
    app_path = os.path.dirname(abspath)
    #os.chdir(app_path)
    if sys.platform == 'darwin' and hasattr(sys, 'frozen'):
        resources_path = os.path.normpath(os.path.abspath(os.path.join(app_path, "..", "Resources")))
    else:
        resources_path = os.path.normpath(os.path.abspath(os.path.join(app_path, "Resources")))

    # Application setup

    app = QSingleApplication(sys.argv)
    app.setOrganizationName('Solace')
    app.setOrganizationDomain('www.solace-coin.com')
    app.setApplicationName(APP_NAME)
    app.setProperty("AppPath", app_path)
    app.setProperty("ResPath", resources_path)
    if sys.platform == 'darwin':
        app.setAttribute(QtCore.Qt.AA_DontShowIconsInMenus)

    hub = Hub(app=app)
    ui = MainWebUI(app=app, hub=hub, debug=False)
    hub.setUI(ui)
    app.singleStart(ui)

    sys.exit(app.exec_())
