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
import SpySettingsTab
import CssSettingsTab


##### Public classes #####
class SettingsWindow(Qt.QDialog) :
	def __init__(self, parent = None) :
		Qt.QDialog.__init__(self, parent)

		self.setWindowIcon(IconsLoader.icon("configure"))

		#####

		left_margin = self.style().pixelMetric(Qt.QStyle.PM_LayoutLeftMargin)
		top_margin = self.style().pixelMetric(Qt.QStyle.PM_LayoutTopMargin)
		right_margin = self.style().pixelMetric(Qt.QStyle.PM_LayoutRightMargin)
		bottom_margin = self.style().pixelMetric(Qt.QStyle.PM_LayoutBottomMargin)
		vertical_spacing = self.style().pixelMetric(Qt.QStyle.PM_LayoutVerticalSpacing)

		self.__main_layout = Qt.QVBoxLayout()
		self.__main_layout.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self.__main_layout)

		self.__tabs_layout = Qt.QHBoxLayout()
		self.__tabs_layout.setContentsMargins(0, 0, right_margin, 0)
		self.__main_layout.addLayout(self.__tabs_layout)

		self.__control_buttons_layout = Qt.QHBoxLayout()
		self.__control_buttons_layout.setContentsMargins(left_margin, vertical_spacing, right_margin, bottom_margin)
		self.__main_layout.addLayout(self.__control_buttons_layout)

		#####

		self.__settings = Settings.Settings(self)

		#####

		self.__tabs_list_browser = Qt.QListWidget(self)
		self.__tabs_list_browser.setViewMode(Qt.QListWidget.IconMode)
		self.__tabs_list_browser.setIconSize(Qt.QSize(48, 48))
		self.__tabs_list_browser.setHorizontalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOff)
		self.__tabs_list_browser.setDragDropMode(Qt.QAbstractItemView.NoDragDrop)
		self.__tabs_layout.addWidget(self.__tabs_list_browser)

		self.__stacked_layout = Qt.QStackedLayout()
		self.__stacked_layout.setContentsMargins(left_margin, vertical_spacing, right_margin, bottom_margin)
		self.__tabs_layout.addLayout(self.__stacked_layout)

		###

		self.__control_buttons_layout.addStretch()

		self.__ok_button = Qt.QPushButton(self)
		self.__ok_button.setIcon(IconsLoader.icon("dialog-ok"))
		self.__ok_button.setAutoDefault(False)
		self.__ok_button.setDefault(False)
		self.__control_buttons_layout.addWidget(self.__ok_button)

		self.__apply_button = Qt.QPushButton(self)
		self.__apply_button.setIcon(IconsLoader.icon("dialog-ok-apply"))
		self.__apply_button.setAutoDefault(False)
		self.__apply_button.setDefault(False)
		self.__control_buttons_layout.addWidget(self.__apply_button)

		self.__cancel_button = Qt.QPushButton(self)
		self.__cancel_button.setIcon(IconsLoader.icon("dialog-cancel"))
		self.__cancel_button.setAutoDefault(False)
		self.__cancel_button.setDefault(False)
		self.__control_buttons_layout.addWidget(self.__cancel_button)

		#####

		self.addSettingsTab(MiscSettingsTab.MiscSettingsTab(self))
		self.addSettingsTab(NetworkSettingsTab.NetworkSettingsTab(self))
		self.addSettingsTab(SpySettingsTab.SpySettingsTab(self))
		self.addSettingsTab(CssSettingsTab.CssSettingsTab(self))

		#####

		self.connect(self.__tabs_list_browser, Qt.SIGNAL("currentRowChanged(int)"), self.__stacked_layout.setCurrentIndex)

		self.connect(self.__ok_button, Qt.SIGNAL("clicked()"), self.accept)
		self.connect(self.__apply_button, Qt.SIGNAL("clicked()"), self.saveSettingsSignal)
		self.connect(self.__cancel_button, Qt.SIGNAL("clicked()"), self.reject)

		#####

		self.__tabs_list_browser.setCurrentRow(0)
		self.__stacked_layout.setCurrentIndex(0)

		self.translateUi()


	##### Public #####

	def saveSettings(self) :
		self.__settings.setValue(Qt.QString("%1/size").arg(self.objectName()), Qt.QVariant(self.size()))

	def loadSettings(self) :
		self.resize(self.__settings.value(Qt.QString("%1/size").arg(self.objectName()), Qt.QVariant(Qt.QSize(600, 450))).toSize())


	##### Private #####

	def translateUi(self) :
		self.setWindowTitle(tr("Settings"))

		for count in xrange(self.__tabs_list_browser.count()) :
			item = self.__tabs_list_browser.item(count)
			item.setText(tr(item.data(Qt.Qt.UserRole).toString()))
		self.resizeTabsBrowser()

		self.__ok_button.setText(tr("&OK"))
		self.__apply_button.setText(tr("&Apply"))
		self.__cancel_button.setText(tr("&Cancel"))

	###

	def addSettingsTab(self, tab) :
		requisites = tab.requisites()

		item = Qt.QListWidgetItem(requisites["icon"], tr(requisites["title"]), self.__tabs_list_browser)
		item.setData(Qt.Qt.UserRole, Qt.QVariant(requisites["title"]))
		self.__tabs_list_browser.addItem(item)

		self.__stacked_layout.addWidget(tab)

		self.connect(self, Qt.SIGNAL("loadSettings()"), tab.loadSettings)
		self.connect(self, Qt.SIGNAL("saveSettings()"), tab.saveSettings)

		self.resizeTabsBrowser()

	def resizeTabsBrowser(self) :
		max_size = Qt.QSize()
		for count in xrange(self.__tabs_list_browser.count()) :
			item_size = Qt.QStyledItemDelegate().sizeHint(self.__tabs_list_browser.viewOptions(), # FIXME: Infinity zooming
				self.__tabs_list_browser.indexFromItem(self.__tabs_list_browser.item(count)))

			if item_size.width() > max_size.width() :
				max_size.setWidth(item_size.width())
			if item_size.height() > max_size.height() :
				max_size.setHeight(item_size.height())
		max_size.setWidth(max_size.width() + 10)

 		for count in xrange(self.__tabs_list_browser.count()) :
			self.__tabs_list_browser.item(count).setSizeHint(max_size)

		self.__tabs_list_browser.setGridSize(max_size)
		width = max_size.width() + self.__tabs_list_browser.rect().width() - self.__tabs_list_browser.contentsRect().width()
		self.__tabs_list_browser.setFixedWidth(width)

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

	def changeEvent(self, event) :
		if event.type() == Qt.QEvent.LanguageChange :
			self.translateUi()
		else :
			Qt.QDialog.changeEvent(self, event)

	def showEvent(self, event) :
		self.loadSettingsSignal()
		Qt.QDialog.showEvent(self, event)

