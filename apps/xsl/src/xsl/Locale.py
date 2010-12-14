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
import Const
import Utils
import Settings
import Logger


##### Public constants #####
DefaultLang = "en"


##### Private classes #####
class LocaleMultiple(Qt.QObject) :
	def __init__(self, parent = None) :
		Qt.QObject.__init__(self, parent)

		#####

		self.__settings = Settings.Settings(self)

		force_main_lang = self.__settings.value("application/locale/force_main_lang").toString()
		self.__locale = ( Qt.QLocale() if force_main_lang.isEmpty() else Qt.QLocale(force_main_lang) )

		#####

		self.connect(self.__settings, Qt.SIGNAL("settingsChanged(const QString &)"), self.applySettingsLocale)


	### Public static ###

	@classmethod
	def validLangs(self) :
		tr_dir = Qt.QDir(Const.TrDirPath)
		tr_dir.setSorting(Qt.QDir.Name)
		tr_dir.setNameFilters(Qt.QStringList() << "*.qm")

		tr_dir_entry_list = tr_dir.entryList()
		tr_dir_entry_list.replaceInStrings(Qt.QRegExp("^(.*)\\.qm$"), "\\1")
		tr_dir_entry_list.append(DefaultLang)

		return tr_dir_entry_list

	@classmethod
	def systemLang(self) :
		lang = Qt.QLocale().name()
		lang.remove(lang.indexOf("_"), lang.length())

		if lang.simplified().isEmpty() :
			lang = DefaultLang

		return Qt.QString(lang)


	### Public ###

	def locale(self) :
		return Qt.QLocale(self.__locale)

	def mainLang(self) :
		lang = self.__locale.name()
		lang.remove(lang.indexOf("_"), lang.length())

		if lang.simplified().isEmpty() :
			lang = DefaultLang

		return Qt.QString(lang)

	###

	def htmlDocsLang(self) :
		main_lang = self.mainLang()
		docs_dir_path = Utils.joinPath(Const.HtmlDocsDirPath, main_lang)
		if not Qt.QFile.exists(docs_dir_path) :
			return Qt.QString(DefaultLang)
		return main_lang


	### Private ###

	def applySettingsLocale(self, key) :
		if key == "application/locale/force_main_lang" :
			force_main_lang = self.__settings.value("application/locale/force_main_lang").toString()
			if force_main_lang != self.mainLang() :
				self.__locale = ( Qt.QLocale() if force_main_lang.isEmpty() else Qt.QLocale(force_main_lang) )
				self.localeChangedSignal(self.__locale.name())
				Logger.debug(Qt.QString("Accepted new locale \"%1\"").arg(self.__locale.name()))


	### Signals ###

	def localeChangedSignal(self, name) :
		self.emit(Qt.SIGNAL("localeChanged(const QString &)"), name)


##### Public classes #####
class Locale(LocaleMultiple) :
	__locale_multiple_object = None

	def __new__(self, parent = None) :
		if self.__locale_multiple_object == None :
			self.__locale_multiple_object = LocaleMultiple.__new__(self, parent)
			LocaleMultiple.__init__(self.__locale_multiple_object, parent)
		return self.__locale_multiple_object

	def __init__(self, parent = None) :
		pass

