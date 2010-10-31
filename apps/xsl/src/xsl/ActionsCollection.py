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
class ActionsCollectionMultiple(Qt.QObject) :
	def __init__(self, parent = None) :
		Qt.QObject.__init__(self, parent)

		#####

		self.__actions_dict = {}


	### Public ###

	def setAction(self, group, name, action) :
		group = str(group)
		name = str(name)
		if not self.__actions_dict.has_key(group) :
			self.__actions_dict[group] = {}
		self.__actions_dict[group][name] = action

	def action(self, group, name) :
		group = str(group)
		name = str(name)
		if self.__actions_dict.has_key(group) and self.__actions_dict[group].has_key(name) :
			return self.__actions_dict[group][name]
		else :
			return None


##### Public classes #####
class ActionsCollection(ActionsCollectionMultiple) :
	__actions_collection_multiple_object = None

	def __new__(self, parent = None) :
		if self.__actions_collection_multiple_object == None :
			self.__actions_collection_multiple_object = ActionsCollectionMultiple.__new__(self, parent)
			ActionsCollectionMultiple.__init__(self.__actions_collection_multiple_object, parent)
		return self.__actions_collection_multiple_object

	def __init__(self, parent = None) :
		pass

