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


import Qt
import Settings
import MouseSelector


##### Public classes #####
class Spy(Qt.QObject) :
	def __init__(self, parent = None) :
		Qt.QObject.__init__(self, parent)

		#####

		self.__settings = Settings.Settings()
		self.__show_translate_window_flag = self.__settings.value("application/spy/show_translate_window_flag", Qt.QVariant(True)).toBool()
		self.__ignore_own_windows_flag = self.__settings.value("application/spy/ignore_own_windows_flag", Qt.QVariant(True)).toBool()

		self.__mouse_selector = MouseSelector.MouseSelector(self)
		self.__mouse_selector.setModifier(self.__settings.value("application/spy/keyboard_modifier", Qt.QVariant(-1)).toInt()[0])

		#####

		self.connect(self.__settings, Qt.SIGNAL("settingsChanged(const QString &)"), self.applySettingsSpy)

		self.connect(self.__mouse_selector, Qt.SIGNAL("selectionChanged(const QString &)"), self.selectionChangedSignal)
		self.connect(self.__mouse_selector, Qt.SIGNAL("selectionChanged(const QString &)"), self.showTranslateWindow)


	### Public ###

	def start(self) :
		self.__mouse_selector.start()

	def stop(self) :
		self.__mouse_selector.stop()

	def isRunning(self) :
		return self.__mouse_selector.isRunning()


	### Private ###

	def showTranslateWindow(self) :
		if self.__show_translate_window_flag :
			if self.__ignore_own_windows_flag :
				if Qt.QApplication.activeWindow() == None :
					self.showTranslateWindowRequestSignal()
			else :
				self.showTranslateWindowRequestSignal()

	def applySettingsSpy(self, key) :
		if key == "application/spy/show_translate_window_flag" :
			self.__show_translate_window_flag = self.__settings.value("application/spy/show_translate_window_flag").toBool()
		elif key == "application/spy/ignore_own_windows_flag" :
			self.__ignore_own_windows_flag = self.__settings.value("application/spy/ignore_own_windows_flag").toBool()
		elif key == "application/spy/keyboard_modifier" :
			self.__mouse_selector.setModifier(self.__settings.value("application/spy/keyboard_modifier").toInt()[0])

	### Signals ###

	def selectionChangedSignal(self, text) :
		self.emit(Qt.SIGNAL("selectionChanged(const QString &)"), text)

	def showTranslateWindowRequestSignal(self) :
		self.emit(Qt.SIGNAL("showTranslateWindowRequest()"))

