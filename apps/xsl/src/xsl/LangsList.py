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


##### Private classes #####
class LangsListMultiple(Qt.QObject) :
	def __init__(self, parent = None) :
		Qt.QObject.__init__(self, parent)

		#####

		self.__langs_list = []
		self.__lang_codes_dict = {}

		#####

		self.translateObject()


	### Public ###

	def langs(self) :
		return self.__langs_list

	def langName(self, short_name) :
		short_name = str(short_name)

		if self.__lang_codes_dict.has_key(short_name) :
			return Qt.QString(self.__lang_codes_dict[short_name])
		else :
			return Qt.QString(short_name)


	### Private ###

	def translateObject(self) :
		self.__lang_codes_dict = {
			"af" : tr("Afrikaans"), "sq" : tr("Albanian"), "ar" : tr("Arabic"), "be" : tr("Belarusian"),
			"bg" : tr("Bulgarian"), "ca" : tr("Catalan"), "zh" : tr("Chinese"), "hz" : tr("Croatian"),
			"cs" : tr("Czech"), "da" : tr("Danish"), "nl" : tr("Dutch"), "en" : tr("English"),
			"et" : tr("Estonian"), "tl" : tr("Filipino"), "fi" : tr("Finnish"), "fr" : tr("French"),
			"gl" : tr("Galician"), "de" : tr("German"), "el" : tr("Greek"), "iw" : tr("Hebrew"),
			"hi" : tr("Hindi"), "hu" : tr("Hungarian"), "is" : tr("Icelandic"), "id" : tr("Indonesian"),
			"ga" : tr("Irish"), "it" : tr("Italian"), "ja" : tr("Japanese"), "ko" : tr("Korean"),
			"lv" : tr("Latvian"), "lt" : tr("Lithuanian"), "mk" : tr("Macedonian"), "ms" : tr("Malay"),
			"mt" : tr("Maltese"), "no" : tr("Norwegian"), "fa" : tr("Persian"), "pl" : tr("Polish"),
			"pt" : tr("Portuguese"), "ro" : tr("Romanian"), "ru" : tr("Russian"), "sr" : tr("Serbian"),
			"sk" : tr("Slovak"), "sl" : tr("Slovenian"), "es" : tr("Spanish"), "sw" : tr("Swahili"),
			"sv" : tr("Swedish"), "th" : tr("Thai"), "tr" : tr("Turkish"), "uk" : tr("Ukrainian"),
			"vi" : tr("Vietnamese"), "cy" : tr("Welsh"), "yi" : tr("Yiddish")
		}


		self.__langs_list = []
		for lang_codes_dict_key in self.__lang_codes_dict.keys() :
			self.__langs_list.append({
				"name" : Qt.QString(self.__lang_codes_dict[lang_codes_dict_key]),
				"code" : Qt.QString(lang_codes_dict_key)
				})

		self.sortLangsList(self.__langs_list)

	def sortLangsList(self, langs_list, left = None, right = None) :
		if left == right == None :
			left = 0
			right = len(langs_list) - 1

		if left >= right :
			return

		i = j = left
		while j <= right :
			if langs_list[j]["name"] <= langs_list[right]["name"] :
				(langs_list[i], langs_list[j]) = (langs_list[j], langs_list[i])
				i += 1
			j += 1

		self.sortLangsList(langs_list, left, i - 2)
		self.sortLangsList(langs_list, i, right)


	### Handlers ###

	def event(self, event) :
		if event.type() == Qt.QEvent.LanguageChange :
			self.translateObject()
			return True
		else :
			return Qt.QObject.event(self, event)


##### Public classes #####
class LangsList(LangsListMultiple) :
	__langs_list_multiple_object = None

	def __new__(self, parent = None) :
		if self.__langs_list_multiple_object == None :
			self.__langs_list_multiple_object = LangsListMultiple.__new__(self, parent)
			LangsListMultiple.__init__(self.__langs_list_multiple_object, parent)
		return self.__langs_list_multiple_object

	def __init__(self, parent = None) :
		pass

