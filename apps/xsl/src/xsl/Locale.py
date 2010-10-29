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
import Settings


##### Private objects #####
LocaleObject = None


##### Private methdos #####
def initLocale() :
	global LocaleObject

	force_locale = Settings.settings().value("application/locale/force_locale", Qt.QVariant(Qt.QString())).toString()
	LocaleObject = ( Qt.QLocale() if force_locale.isEmpty() else Qt.QLocale(force_locale) )


##### Public methods #####
def locale() :
	if LocaleObject == None :
		initLocale()
	return LocaleObject

def mainLang() :
	if LocaleObject == None :
		initLocale()

	lang = LocaleObject.name()
	lang.remove(lang.indexOf("_"), lang.length())

	if lang.simplified().isEmpty() :
		lang = Const.DefaultLang

	return Qt.QString(lang)

