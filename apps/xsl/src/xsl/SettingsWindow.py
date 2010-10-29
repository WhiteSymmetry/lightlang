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


##### Public classes #####
class SettingsWindow(Qt.QDialog) :
	def __init__(self, parent = None) :
		Qt.QDialog.__init__(self, parent)

		self.setObjectName("settings_window")

		self.setWindowTitle(tr("Settings"))
		self.setWindowIcon(IconsLoader.icon("configure"))

		#####

		self._main_layout = Qt.QVBoxLayout()
		self._main_layout.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self._main_layout)

		self._label = Qt.QLabel("TODO") # TODO
		self._main_layout.addWidget(self._label)

		left_margin = self.style().pixelMetric(Qt.QStyle.PM_LayoutLeftMargin)
		top_margin = self.style().pixelMetric(Qt.QStyle.PM_LayoutTopMargin)
		right_margin = self.style().pixelMetric(Qt.QStyle.PM_LayoutRightMargin)
		bottom_margin = self.style().pixelMetric(Qt.QStyle.PM_LayoutBottomMargin)
		vertical_spacing = self.style().pixelMetric(Qt.QStyle.PM_LayoutVerticalSpacing)

		self._control_buttons_layout = Qt.QHBoxLayout()
		self._control_buttons_layout.setContentsMargins(left_margin, vertical_spacing, right_margin, bottom_margin)
		self._main_layout.addLayout(self._control_buttons_layout)

		#####

		self._control_buttons_layout.addStretch()

		self._ok_button = Qt.QPushButton(IconsLoader.icon("dialog-ok-apply"), tr("&OK"))
		self._ok_button.setAutoDefault(False)
		self._ok_button.setDefault(False)
		self._control_buttons_layout.addWidget(self._ok_button)

		#####

		self.connect(self._ok_button, Qt.SIGNAL("clicked()"), self.accept)


	##### Public #####

	def saveSettings(self) :
		settings = Settings.settings()
		settings.setValue("settings_window/size", Qt.QVariant(self.size()))

	def loadSettings(self) :
		settings = Settings.settings()
		self.resize(settings.value("settings_window/size", Qt.QVariant(Qt.QSize(500, 350))).toSize())

