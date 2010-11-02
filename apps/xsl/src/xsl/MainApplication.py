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


import __builtin__

import Qt
import Const
import Utils
import Locale
import Css
import Logger


##### Public classes #####
class MainApplication(Qt.QApplication) :
	def __init__(self, argv) :
		Qt.QApplication.__init__(self, argv)

		#####

		__builtin__.__dict__["tr"] = ( lambda text : Qt.QApplication.translate("@default", text) )
		self.__locale = Locale.Locale()
		self.__translators_list = []
		self.applyTranslate()

		self.__css = Css.Css()
		self.applyCss()

		#####

		self.connect(self.__locale, Qt.SIGNAL("localeChanged(const QString &)"), self.applyTranslate)

		self.connect(self.__css, Qt.SIGNAL("cssChanged()"), self.applyCss)


	### Private ###

	def applyTranslate(self) :
		for translators_list_item in self.__translators_list :
			self.removeTranslator(translators_list_item)
		self.__translators_list = []

		main_lang = self.__locale.mainLang()
		Logger.debug(Qt.QString("Request to new main lang \"%1\"").arg(main_lang))
		for tr_file_path in ( Utils.joinPath(Const.TrDirPath, main_lang),
			Utils.joinPath(Qt.QLibraryInfo.location(Qt.QLibraryInfo.TranslationsPath), "qt_"+main_lang) ) :

			translator = Qt.QTranslator()
			translator.load(tr_file_path)
			self.installTranslator(translator)
			self.__translators_list.append(translator)
			if not translator.isEmpty() :
				Logger.debug(Qt.QString("Installed new tr file \"%1\"").arg(tr_file_path))

	def applyCss(self) :
		self.setStyleSheet(self.__css.css())

	###

	def commitData(self, session_manager) :
		if session_manager.allowsInteraction() :
			self.saveSettingsRequestSignal()
			session_manager.setRestartHint(Qt.QSessionManager.RestartIfRunning)
			session_manager.release()
			Logger.debug("Session saved")
		else :
			Logger.warning("Cannot save session")


	### Signals ###

	def saveSettingsRequestSignal(self) :
		self.emit(Qt.SIGNAL("saveSettingsRequest()"))

