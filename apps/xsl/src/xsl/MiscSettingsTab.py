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
import Utils
import Locale
import Settings
import LangsList
import IconsLoader


##### Public classes #####
class MiscSettingsTab(Qt.QWidget) :
	def __init__(self, parent = None) :
		Qt.QWidget.__init__(self, parent)

		self.__main_layout = Qt.QGridLayout()
		self.setLayout(self.__main_layout)

		#####

		self.__settings = Settings.Settings(self)

		#####

		self.__show_tray_icon_checkbox = Qt.QCheckBox(self)
		self.__main_layout.addWidget(self.__show_tray_icon_checkbox, 0, 0, 1, 2)

		self.__show_splash_checkbox = Qt.QCheckBox(self)
		self.__main_layout.addWidget(self.__show_splash_checkbox, 1, 0, 1, 2)

		self.__debug_mode_checkbox = Qt.QCheckBox(self)
		self.__main_layout.addWidget(self.__debug_mode_checkbox, 2, 0, 1, 2)

		self.__main_layout.setRowStretch(3, 1)

		self.__force_main_lang_label = Qt.QLabel(self)
		self.__main_layout.addWidget(self.__force_main_lang_label, 4, 0)

		self.__force_main_lang_combobox = Qt.QComboBox(self)
		self.__main_layout.addWidget(self.__force_main_lang_combobox, 4, 1)

		#####

		self.translateUi()


	### Public ###

	def requisites(self) :
		return {
			"icon" : IconsLoader.icon("configure"),
			"title" : Qt.QT_TR_NOOP("Misc"),
		}

	###

	def saveSettings(self) :
		self.__settings.setValue("application/misc/show_tray_icon_flag", Qt.QVariant(self.__show_tray_icon_checkbox.isChecked()))
		self.__settings.setValue("application/misc/show_splash_flag", Qt.QVariant(self.__show_splash_checkbox.isChecked()))
		self.__settings.setValue("application/logger/debug_mode_flag", Qt.QVariant(self.__debug_mode_checkbox.isChecked()))

		self.__settings.setValue("application/locale/force_main_lang",
			self.__force_main_lang_combobox.itemData(self.__force_main_lang_combobox.currentIndex()).toString())

	def loadSettings(self) :
		self.__show_tray_icon_checkbox.setChecked(self.__settings.value("application/misc/show_tray_icon_flag", Qt.QVariant(True)).toBool())
		self.__show_splash_checkbox.setChecked(self.__settings.value("application/misc/show_splash_flag", Qt.QVariant(True)).toBool())
		self.__debug_mode_checkbox.setChecked(self.__settings.value("application/logger/debug_mode_flag").toBool())

		###

		force_main_lang = self.__settings.value("application/locale/force_main_lang").toString()
		for count in xrange(self.__force_main_lang_combobox.count()) :
			if ( self.__force_main_lang_combobox.itemData(count).toString() == force_main_lang and
				not self.__force_main_lang_combobox.itemText(count).isEmpty() ) :
				self.__force_main_lang_combobox.setCurrentIndex(count)



	### Private ###

	def translateUi(self) :
		self.__show_tray_icon_checkbox.setText(tr("Show tray icon"))
		self.__show_splash_checkbox.setText(tr("Show splash screen on startup"))
		self.__force_main_lang_label.setText(tr("Force language:"))
		self.__debug_mode_checkbox.setText(tr("Debug mode (write info to stderr)"))

		###

		last_index = self.__force_main_lang_combobox.currentIndex()
		self.__force_main_lang_combobox.clear()

		lang_codes_dict = LangsList.langCodes()
		system_lang = Locale.Locale.systemLang()

		self.__force_main_lang_combobox.addItem(IconsLoader.icon(Utils.joinPath("flags", system_lang)),
			tr("By default (%1)").arg(LangsList.langName(system_lang, lang_codes_dict)), Qt.QVariant(""))

		self.__force_main_lang_combobox.insertSeparator(1)

		for langs_list_item in Locale.Locale.validLangs() :
			self.__force_main_lang_combobox.addItem(IconsLoader.icon(Utils.joinPath("flags", langs_list_item)),
				LangsList.langName(langs_list_item, lang_codes_dict), Qt.QVariant(langs_list_item))
		self.__force_main_lang_combobox.setCurrentIndex(last_index)


	### Handlers ###

	def changeEvent(self, event) :
		if event.type() == Qt.QEvent.LanguageChange :
			self.translateUi()
		else :
			Qt.QWidget.changeEvent(self, event)

