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
import MiscSettingsTab
import NetworkSettingsTab
import CssSettingsTab


##### Public classes #####
class SettingsWindow(Qt.QDialog) :
	def __init__(self, parent = None) :
		Qt.QDialog.__init__(self, parent)

		self.setObjectName("settings_window")

		self.setWindowTitle(tr("Settings"))
		self.setWindowIcon(IconsLoader.icon("configure"))

		#####

		left_margin = self.style().pixelMetric(Qt.QStyle.PM_LayoutLeftMargin)
		top_margin = self.style().pixelMetric(Qt.QStyle.PM_LayoutTopMargin)
		right_margin = self.style().pixelMetric(Qt.QStyle.PM_LayoutRightMargin)
		bottom_margin = self.style().pixelMetric(Qt.QStyle.PM_LayoutBottomMargin)
		vertical_spacing = self.style().pixelMetric(Qt.QStyle.PM_LayoutVerticalSpacing)

		self._main_layout = Qt.QVBoxLayout()
		self._main_layout.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self._main_layout)

		self._tabs_layout = Qt.QHBoxLayout()
		self._tabs_layout.setContentsMargins(0, 0, right_margin, 0)
		self._main_layout.addLayout(self._tabs_layout)

		self._control_buttons_layout = Qt.QHBoxLayout()
		self._control_buttons_layout.setContentsMargins(left_margin, vertical_spacing, right_margin, bottom_margin)
		self._main_layout.addLayout(self._control_buttons_layout)

		#####

		self._tabs_list_browser = Qt.QListWidget(self)
		self._tabs_list_browser.setViewMode(Qt.QListWidget.IconMode)
		self._tabs_list_browser.setIconSize(Qt.QSize(48, 48))
		self._tabs_list_browser.setHorizontalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOff)
		self._tabs_layout.addWidget(self._tabs_list_browser)

		self._stacked_layout = Qt.QStackedLayout()
		self._stacked_layout.setContentsMargins(left_margin, vertical_spacing, right_margin, bottom_margin)
		self._tabs_layout.addLayout(self._stacked_layout)

		###

		self._control_buttons_layout.addStretch()

		self._ok_button = Qt.QPushButton(IconsLoader.icon("dialog-ok"), tr("&OK"), self)
		self._ok_button.setAutoDefault(False)
		self._ok_button.setDefault(False)
		self._control_buttons_layout.addWidget(self._ok_button)

		self._apply_button = Qt.QPushButton(IconsLoader.icon("dialog-ok-apply"), tr("&Apply"), self)
		self._apply_button.setAutoDefault(False)
		self._apply_button.setDefault(False)
		self._control_buttons_layout.addWidget(self._apply_button)

		self._cancel_button = Qt.QPushButton(IconsLoader.icon("dialog-cancel"), tr("&Cancel"), self)
		self._cancel_button.setAutoDefault(False)
		self._cancel_button.setDefault(False)
		self._control_buttons_layout.addWidget(self._cancel_button)

		#####

		self.addSettingsTab(MiscSettingsTab.MiscSettingsTab(self))
		self.addSettingsTab(NetworkSettingsTab.NetworkSettingsTab(self))
		self.addSettingsTab(CssSettingsTab.CssSettingsTab(self))

		#####

		self.connect(self._tabs_list_browser, Qt.SIGNAL("currentRowChanged(int)"), self._stacked_layout.setCurrentIndex)

		self.connect(self._ok_button, Qt.SIGNAL("clicked()"), self.accept)
		self.connect(self._apply_button, Qt.SIGNAL("clicked()"), self.saveSettingsSignal)
		self.connect(self._cancel_button, Qt.SIGNAL("clicked()"), self.reject)

		#####

		self._tabs_list_browser.setCurrentRow(0)
		self._stacked_layout.setCurrentIndex(0)


	##### Public #####

	def saveSettings(self) :
		settings = Settings.settings()
		settings.setValue("settings_window/size", Qt.QVariant(self.size()))

	def loadSettings(self) :
		settings = Settings.settings()
		self.resize(settings.value("settings_window/size", Qt.QVariant(Qt.QSize(600, 450))).toSize())


	##### Private #####

	def addSettingsTab(self, tab) :
		requisites = tab.requisites()

		self._tabs_list_browser.addItem(Qt.QListWidgetItem(requisites["icon"], requisites["title"], self._tabs_list_browser))

		tab_groupbox = Qt.QGroupBox(requisites["title"], self)
		tab_groupbox_layout = Qt.QVBoxLayout()
		tab_groupbox.setLayout(tab_groupbox_layout)
		tab_groupbox_layout.addWidget(tab)
		self._stacked_layout.addWidget(tab_groupbox)

		self.connect(self, Qt.SIGNAL("loadSettings()"), tab.loadSettings)
		self.connect(self, Qt.SIGNAL("saveSettings()"), tab.saveSettings)

		###

		max_size = Qt.QSize()
		for count in xrange(self._tabs_list_browser.count()) :
			item_size = Qt.QStyledItemDelegate().sizeHint(self._tabs_list_browser.viewOptions(),
				self._tabs_list_browser.indexFromItem(self._tabs_list_browser.item(count)))

			if item_size.width() > max_size.width() :
				max_size.setWidth(item_size.width())
			if item_size.height() > max_size.height() :
				max_size.setHeight(item_size.height())
		max_size.setWidth(max_size.width() + 10)

 		for count in xrange(self._tabs_list_browser.count()) :
			self._tabs_list_browser.item(count).setSizeHint(max_size)

		self._tabs_list_browser.setGridSize(max_size)
		width = max_size.width() + self._tabs_list_browser.rect().width() - self._tabs_list_browser.contentsRect().width()
		self._tabs_list_browser.setFixedWidth(width)

	###

	def accept(self) :
		self.saveSettingsSignal()
		Qt.QDialog.accept(self)


	### Signals ###

	def saveSettingsSignal(self) :
		self.emit(Qt.SIGNAL("saveSettings()"))

	def loadSettingsSignal(self) :
		self.emit(Qt.SIGNAL("loadSettings()"))


	### Handlers ###

	def showEvent(self, event) :
		self.loadSettingsSignal()
		Qt.QDialog.showEvent(self, event)

