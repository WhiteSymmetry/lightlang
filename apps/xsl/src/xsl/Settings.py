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


##### Private constants #####
SettingsPostfix = ".conf"


##### Private classes #####
class SettingsMultiple(Qt.QSettings) :
	def __init__(self, parent = None) :
		settings_file_path = Utils.joinPath(self.dirPath(), Const.MyName.toLower()+SettingsPostfix)
		Qt.QSettings.__init__(self, settings_file_path, Qt.QSettings.IniFormat, parent)


	### Public static ###

	@classmethod
	def dirPath(self) :
		return Utils.joinPath(Qt.QDir.homePath(), "."+Const.MyName.toLower())


	### Public ###

	def setValue(self, key, value) :
		if not self.contains(key) or self.value(key) != Qt.QVariant(value) :
			Qt.QSettings.setValue(self, key, value)
			self.sync() # FIXME: Bug with C++ destructor in QSettings()
			self.settingsChangedSignal(key)


	### Signals ###

	def settingsChangedSignal(self, key) :
		self.emit(Qt.SIGNAL("settingsChanged(const QString &)"), key)


##### Public classes #####
class Settings(SettingsMultiple) :
	__settings_multiple_object = None

	def __new__(self, parent = None) :
		if self.__settings_multiple_object == None :
			self.__settings_multiple_object = SettingsMultiple.__new__(self, parent)
			SettingsMultiple.__init__(self.__settings_multiple_object, parent)
		return self.__settings_multiple_object

	def __init__(self, parent = None) :
		pass

