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
import CssCollection


##### Public classes #####
class ListBrowserCaptionItem(Qt.QListWidgetItem) :
	def __init__(self, text, parent = None) :
		Qt.QListWidgetItem.__init__(self, text, parent)

		self.setFlags(Qt.Qt.NoItemFlags)
		self.setTextAlignment(Qt.Qt.AlignHCenter|Qt.Qt.AlignVCenter)

		#####

		self.__css_collection = CssCollection.CssCollection()
		self.initDrawInstruments()

		#####

		Qt.QObject.connect(self.__css_collection, Qt.SIGNAL("cssChanged()"), self.initDrawInstruments)


	### Private ###

	def initDrawInstruments(self) :
		font = self.font()
		font.setBold(self.__css_collection.value("dict_header_font", "bold_flag"))
		font.setItalic(self.__css_collection.value("dict_header_font", "italic_flag"))
		if self.__css_collection.value("dict_header_font", "large_flag") :
			if font.pixelSize() > 0 : # FIXME: largest to infinity
				font.setPixelSize(font.pixelSize() + 1)
			elif font.pointSize() > 0 :
				font.setPointSize(font.pointSize() + 1)
		self.setFont(font)

		foreground_brush = self.foreground()
		foreground_brush.setStyle(Qt.Qt.SolidPattern)
		if self.__css_collection.value("dict_header_font", "color").isValid() :
			foreground_brush.setColor(self.__css_collection.value("dict_header_font", "color"))
		self.setForeground(foreground_brush)

		background_brush = self.background()
		background_brush.setStyle(Qt.Qt.SolidPattern)
		if self.__css_collection.value("dict_header_background", "color").isValid() :
			background_brush.setColor(self.__css_collection.value("dict_header_background", "color"))
		self.setBackground(background_brush)

