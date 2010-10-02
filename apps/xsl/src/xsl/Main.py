# -*- coding: utf8 -*-
#
# XSL - graphical interface for SL
# Copyright (C) 2007-2016 Devaev Maxim
#
# This file is part of XSL.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


import __builtin__

import Qt
import Config
import Const
import Utils
import IconsLoader
import Locale
import StartupLock
import UserStyleCss
import MainApplication
import TrayIcon
import MainWindow


##### Private constants #####
TrPostfix = ".qm"
TrDir = Config.DataRootDir+"/xsl/tr/"


##### Public objects #####
MainObject = None


##### Public classes #####
class Main(object) :
	def __init__(self, argv, no_splash_flag = False, no_tray_icon = False) :
		object.__init__(self)

		#####

		self._argv = argv
		self._no_splash_flag = no_splash_flag
		self._no_tray_icon = no_tray_icon

		#####

		__builtin__.__dict__["tr"] = ( lambda text : Qt.QApplication.translate("@default", text) )


	### Public ###

	def run(self) :
		self._app = MainApplication.MainApplication(self._argv)
		self._app.setQuitOnLastWindowClosed(self._no_tray_icon)

		tr_file_path = Utils.joinPath(TrDir, Locale.mainLang()+TrPostfix)
		if Qt.QFile.exists(tr_file_path) :
			self._translator = Qt.QTranslator()
			self._translator.load(tr_file_path)
			self._app.installTranslator(self._translator)

		qt_tr_file_path = Utils.joinPath(Config.QtTrDir, "qt_"+Locale.mainLang()+TrPostfix)
		if Qt.QFile.exists(qt_tr_file_path) :
			self._qt_translator = Qt.QTranslator()
			self._qt_translator.load(qt_tr_file_path)
			self._app.installTranslator(self._qt_translator)

		self._app.setStyleSheet(UserStyleCss.userStyleCss())

		StartupLock.test()

		#####

		if not self._no_splash_flag :
			self._splash_pixmap = IconsLoader.pixmap("xsl_splash")
			self._splash = Qt.QSplashScreen(self._splash_pixmap)
			if not self._app.isSessionRestored() :
				self._splash.show()

		self._app.processEvents()

		self._main_window = MainWindow.MainWindow()
		self._tray_icon = TrayIcon.TrayIcon()

		#####

		Qt.QObject.connect(self._app, Qt.SIGNAL("focusChanged(QWidget *, QWidget*)"), self._main_window.focusChanged)
		Qt.QObject.connect(self._app, Qt.SIGNAL("saveSettingsRequest()"), self._main_window.exit)

		Qt.QObject.connect(self._main_window, Qt.SIGNAL("spyStarted()"), self._tray_icon.spyStarted)
		Qt.QObject.connect(self._main_window, Qt.SIGNAL("spyStopped()"), self._tray_icon.spyStopped)

		Qt.QObject.connect(self._tray_icon, Qt.SIGNAL("startSpyRequest()"), self._main_window.startSpy)
		Qt.QObject.connect(self._tray_icon, Qt.SIGNAL("stopSpyRequest()"), self._main_window.stopSpy)
		Qt.QObject.connect(self._tray_icon, Qt.SIGNAL("visibleChangeRequest()"), self._main_window.visibleChange)
		Qt.QObject.connect(self._tray_icon, Qt.SIGNAL("exitRequest()"), self._main_window.exit)

		#####

		self._main_window.load()
		if not self._no_tray_icon :
			self._tray_icon.show()

		if not self._no_splash_flag :
			self._splash.finish(self._main_window)

		#####

		global MainObject
		MainObject = self

		#####

		self._app.exec_()

