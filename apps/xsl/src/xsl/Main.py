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

import Qt
import Settings
import IconsLoader
import StartupLock
import MainApplication
import MainWindow


##### Public classes #####
class Main(Qt.QObject) :
	def __init__(self, parent = None) :
		Qt.QObject.__init__(self, parent)


	### Public ###

	def run(self) :
		self.__app = MainApplication.MainApplication(sys.argv)

		StartupLock.test()

		show_splash_flag = Settings.Settings().value("application/misc/show_splash_flag", Qt.QVariant(True)).toBool()

		if show_splash_flag :
			splash_pixmap = IconsLoader.pixmap("xsl_splash")
			splash = Qt.QSplashScreen(splash_pixmap)
			if not self.__app.isSessionRestored() :
				splash.show()

		self.__app.processEvents()

		self.__main_window = MainWindow.MainWindow()
		self.connect(self.__app, Qt.SIGNAL("focusChanged(QWidget *, QWidget*)"), self.__main_window.focusChanged)
		self.connect(self.__app, Qt.SIGNAL("saveSettingsRequest()"), self.__main_window.exit)
		self.__main_window.load()

		if show_splash_flag :
			splash.finish(self.__main_window)

		self.__app.exec_()

