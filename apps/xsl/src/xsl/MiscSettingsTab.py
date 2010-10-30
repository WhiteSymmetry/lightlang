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
import IconsLoader
import LineEdit


##### Public classes #####
class MiscSettingsTab(Qt.QWidget) :
	def __init__(self, parent = None) :
		Qt.QWidget.__init__(self, parent)

		self._main_layout = Qt.QGridLayout()
		self.setLayout(self._main_layout)

		#####

		self._show_tray_icon_checkbox = Qt.QCheckBox(tr("Show tray icon (on next start)"), self)
		self._main_layout.addWidget(self._show_tray_icon_checkbox, 0, 0)

		self._show_splash_checkbox = Qt.QCheckBox(tr("Show splash screen"), self)
		self._main_layout.addWidget(self._show_splash_checkbox, 1, 0)

		self._force_locale_label = Qt.QLabel(tr("Force locale (on next start, for example, \"ru_RU\"):"), self)
		self._main_layout.addWidget(self._force_locale_label, 2, 0)

		self._force_locale_line_edit = LineEdit.LineEdit(self)
		self._main_layout.addWidget(self._force_locale_line_edit, 2, 1)

		self._main_layout.setRowStretch(3, 1)

		self._debug_mode_checkbox = Qt.QCheckBox(tr("Debug mode (write info to stderr)"), self)
		self._main_layout.addWidget(self._debug_mode_checkbox, 4, 0)


	### Public ###

	def requisites(self) :
		return {
			"icon" : IconsLoader.icon("configure"),
			"title" : tr("Misc"),
		}

	###

	def saveSettings(self) :
		settings = Settings.settings()
		settings.setValue("application/misc/show_tray_icon_flag", Qt.QVariant(self._show_tray_icon_checkbox.isChecked()))
		settings.setValue("application/misc/show_splash_flag", Qt.QVariant(self._show_splash_checkbox.isChecked()))
		settings.setValue("application/locale/force_locale", Qt.QVariant(self._force_locale_line_edit.text()))
		settings.setValue("application/logger/debug_mode_flag", Qt.QVariant(self._debug_mode_checkbox.isChecked()))

	def loadSettings(self) :
		settings = Settings.settings()
		self._show_tray_icon_checkbox.setChecked(settings.value("application/misc/show_tray_icon_flag", Qt.QVariant(True)).toBool())
		self._show_splash_checkbox.setChecked(settings.value("application/misc/show_splash_flag", Qt.QVariant(True)).toBool())
		self._force_locale_line_edit.setText(settings.value("application/locale/force_locale").toString())
		self._debug_mode_checkbox.setChecked(settings.value("application/logger/debug_mode_flag", Qt.QVariant(False)).toBool())

