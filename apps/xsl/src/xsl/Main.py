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


import sys
import __builtin__

import Qt
import Config
import Const
import Utils
import Settings
import IconsLoader
import Locale
import StartupLock
import Css
import MainApplication
import TrayIcon
import MainWindow


##### Public objects #####
MainObject = None


##### Public classes #####
class Main(Qt.QObject) :
	def __init__(self, parent = None) :
		Qt.QObject.__init__(self, parent)

		#####

		__builtin__.__dict__["tr"] = ( lambda text : Qt.QApplication.translate("@default", text) )


	### Public ###

	def run(self) :
		self._app = MainApplication.MainApplication(sys.argv)
		show_tray_icon_flag = Settings.settings().value("application/misc/show_tray_icon_flag", Qt.QVariant(True)).toBool()
		show_splash_flag = Settings.settings().value("application/misc/show_splash_flag", Qt.QVariant(True)).toBool()
		self._app.setQuitOnLastWindowClosed(not show_tray_icon_flag)

		tr_file_path = Utils.joinPath(Const.TrDir, Locale.mainLang()+Const.TrPostfix)
		if Qt.QFile.exists(tr_file_path) :
			self._translator = Qt.QTranslator()
			self._translator.load(tr_file_path)
			self._app.installTranslator(self._translator)

		qt_tr_file_path = Utils.joinPath(Config.QtTrDir, "qt_"+Locale.mainLang()+Const.TrPostfix)
		if Qt.QFile.exists(qt_tr_file_path) :
			self._qt_translator = Qt.QTranslator()
			self._qt_translator.load(qt_tr_file_path)
			self._app.installTranslator(self._qt_translator)

		self._app.setStyleSheet(Css.css())

		StartupLock.test()

		#####

		if show_splash_flag :
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

		Qt.QObject.connect(self._tray_icon, Qt.SIGNAL("visibleChangeRequest()"), self._main_window.visibleChange)

		#####

		self._main_window.load()
		if show_tray_icon_flag :
			self._tray_icon.show()

		if show_splash_flag :
			self._splash.finish(self._main_window)

		#####

		global MainObject
		MainObject = self

		#####

		self._app.exec_()

