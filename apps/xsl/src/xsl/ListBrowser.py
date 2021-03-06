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
import ListBrowserInfoItem
import ListBrowserCaptionItem


##### Public classes #####
class ListBrowser(Qt.QListWidget) :
	def __init__(self, parent = None) :
		Qt.QListWidget.__init__(self, parent)

		#####

		self.__info_item_regexp = Qt.QRegExp("\\{\\{(.*)\\}\\}")
		self.__info_item_regexp.setMinimal(True)

		self.__caption_item_regexp = Qt.QRegExp("\\[\\[(.*)\\]\\]")
		self.__caption_item_regexp.setMinimal(True)


	### Public ###

	def setList(self, items_list) :
		self.clear()

		for items_list_item in items_list :
			if self.__info_item_regexp.exactMatch(items_list_item) :
				self.addItem(ListBrowserInfoItem.ListBrowserInfoItem(self.__info_item_regexp.cap(1), self))
			elif self.__caption_item_regexp.exactMatch(items_list_item) :
				self.addItem(ListBrowserCaptionItem.ListBrowserCaptionItem(self.__caption_item_regexp.cap(1), self))
			else :
				self.addItem(items_list_item)

	def setText(self, text) :
		self.clear()
		self.addItem(ListBrowserInfoItem.ListBrowserInfoItem(text, self))

