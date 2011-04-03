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
import Logger

try :
	import X11Inputs
except :
	Logger.warning("Ignored X11Inputs")
	Logger.attachException(Logger.WarningMessage)


##### Public classes #####
class SpySettingsTab(Qt.QWidget) :
	def __init__(self, parent = None) :
		Qt.QWidget.__init__(self, parent)

		self.__main_layout = Qt.QGridLayout()
		self.setLayout(self.__main_layout)

		#####

		self.__settings = Settings.Settings(self)

		#####

		self.__show_translate_window_checkbox = Qt.QCheckBox(self)
		self.__main_layout.addWidget(self.__show_translate_window_checkbox, 0, 0)

		self.__ignore_own_windows_checkbox = Qt.QCheckBox(self)
		self.__main_layout.addWidget(self.__ignore_own_windows_checkbox, 1, 0)

		self.__keyboard_modifiers_label = Qt.QLabel(self)
		self.__main_layout.addWidget(self.__keyboard_modifiers_label, 2, 0)

		self.__keyboard_modifiers_combobox = Qt.QComboBox(self)
		self.__main_layout.addWidget(self.__keyboard_modifiers_combobox, 2, 1)

		self.__main_layout.setRowStretch(3, 1)

		#####

		self.translateUi()


	### Public ###

	def requisites(self) :
		return {
			"icon" : IconsLoader.icon("xsl_48"),
			"title" : Qt.QT_TR_NOOP("Spy"),
		}

	###

	def saveSettings(self) :
		self.__settings.setValue("application/spy/show_translate_window_flag",
			Qt.QVariant(self.__show_translate_window_checkbox.isChecked()))
		self.__settings.setValue("application/spy/ignore_own_windows_flag",
			Qt.QVariant(self.__ignore_own_windows_checkbox.isChecked()))

		if sys.modules.has_key("X11Inputs") :
			self.__settings.setValue("application/spy/keyboard_modifier",
				self.__keyboard_modifiers_combobox.itemData(self.__keyboard_modifiers_combobox.currentIndex()).toInt()[0])

	def loadSettings(self) :
		self.__show_translate_window_checkbox.setChecked(self.__settings.value(
			"application/spy/show_translate_window_flag", Qt.QVariant(True)).toBool())
		self.__ignore_own_windows_checkbox.setChecked(self.__settings.value(
			"application/spy/ignore_own_windows_flag", Qt.QVariant(True)).toBool())

		if sys.modules.has_key("X11Inputs") :
			keyboard_modifier = self.__settings.value("application/spy/keyboard_modifier", Qt.QVariant(X11Inputs.NoModifier)).toInt()[0]
			for count in xrange(self.__keyboard_modifiers_combobox.count()) :
				if self.__keyboard_modifiers_combobox.itemData(count).toInt()[0] == keyboard_modifier :
					self.__keyboard_modifiers_combobox.setCurrentIndex(count)
					break


	### Private ###

	def translateUi(self) :
		self.__keyboard_modifiers_label.setText(tr("Keyboard modifiers:"))
		self.__show_translate_window_checkbox.setText(tr("Show translate window"))
		self.__ignore_own_windows_checkbox.setText(tr("Ignore their own windows"))

		self.__keyboard_modifiers_label.setText(tr("Keyboard modifiers:"))
		if sys.modules.has_key("X11Inputs") :
			self.__keyboard_modifiers_combobox.clear()
			self.__keyboard_modifiers_combobox.addItem(tr("Left Ctrl"), Qt.QVariant(X11Inputs.LeftCtrlModifier))
			self.__keyboard_modifiers_combobox.addItem(tr("Left Alt"), Qt.QVariant(X11Inputs.LeftAltModifier))
			self.__keyboard_modifiers_combobox.addItem(tr("Left Shift"), Qt.QVariant(X11Inputs.LeftShiftModifier))
			self.__keyboard_modifiers_combobox.addItem(tr("Left Win"), Qt.QVariant(X11Inputs.LeftWinModifier))
			self.__keyboard_modifiers_combobox.insertSeparator(4)
			self.__keyboard_modifiers_combobox.addItem(tr("Right Ctrl"), Qt.QVariant(X11Inputs.RightCtrlModifier))
			self.__keyboard_modifiers_combobox.addItem(tr("Right Alt"), Qt.QVariant(X11Inputs.RightAltModifier))
			self.__keyboard_modifiers_combobox.addItem(tr("Right Shift"), Qt.QVariant(X11Inputs.RightShiftModifier))
			self.__keyboard_modifiers_combobox.addItem(tr("Right Win"), Qt.QVariant(X11Inputs.RightWinModifier))
			self.__keyboard_modifiers_combobox.insertSeparator(9)
			self.__keyboard_modifiers_combobox.addItem(tr("No modifier"), Qt.QVariant(X11Inputs.NoModifier))


	### Handlers ###

	def changeEvent(self, event) :
		if event.type() == Qt.QEvent.LanguageChange :
			self.translateUi()
		else :
			Qt.QWidget.changeEvent(self, event)

