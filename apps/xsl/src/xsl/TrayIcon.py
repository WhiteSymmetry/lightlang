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


import sys

import Qt
import Const
import Locale
import IconsLoader
import ActionsCollection
import EntitledMenu
import Logger

try :
	import KeysGrabber
except :
	Logger.warning("Ignored X11 hooks: KeysGrabber")
	Logger.attachException(Logger.WarningMessage)


##### Public classes #####
class TrayIcon(Qt.QSystemTrayIcon) :
	def __init__(self, parent = None) :
		Qt.QSystemTrayIcon.__init__(self, parent)

		#####

		self.__locale = Locale.Locale()
		self.__actions_collection = ActionsCollection.ActionsCollection()

		#####

		self.connect(self.__locale, Qt.SIGNAL("localeChanged(const QString &)"), self.translateObject)

		self.connect(self.__actions_collection.action("spy_menu", "start_spy"), Qt.SIGNAL("changed()"), self.translateObject)

		if sys.modules.has_key("KeysGrabber") :
			self.__keys_grabber = KeysGrabber.KeysGrabber()
			self.__hotkey = self.__keys_grabber.addHotkey(KeysGrabber.Key_L, KeysGrabber.WinModifier)
			self.connect(self.__keys_grabber, Qt.SIGNAL("keyPressed(const QString &)"), self.act)

		self.connect(self, Qt.SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.act)

		#####

		self.translateObject()


	### Private ###

	def translateObject(self) :
		if self.__actions_collection.action("spy_menu", "start_spy").isEnabled() :
			self.setIcon(IconsLoader.icon("xsl_22"))
			self.setToolTip(tr("%1 - graphical interface for SL\nSpy is stopped").arg(Const.MyName))
		else :
			self.setIcon(IconsLoader.icon("xsl+spy_22"))
			self.setToolTip(tr("%1 - graphical interface for SL\nSpy is running").arg(Const.MyName))

	###

	def act(self, reason) :
		if self.__dict__.has_key("__keys_grabber") and reason == self.__hotkey :
			self.visibleChangeRequestSignal()
		elif reason == Qt.QSystemTrayIcon.Trigger :
			self.visibleChangeRequestSignal()
		elif reason == Qt.QSystemTrayIcon.Context :
			menu = EntitledMenu.EntitledMenu(IconsLoader.icon("xsl"), Const.Organization+" "+Const.MyName)
			menu.addAction(self.__actions_collection.action("spy_menu", "start_spy"))
			menu.addAction(self.__actions_collection.action("spy_menu", "stop_spy"))
			menu.addSeparator()
			menu.addAction(tr("Dictionary window")+( "\tWin+L" if self.__dict__.has_key("__keys_grabber") else "" ),
				self.visibleChangeRequestSignal)
			menu.addSeparator()
			menu.addAction(self.__actions_collection.action("application", "exit"))
			menu.exec_(Qt.QCursor.pos())


	### Signals ###

	def visibleChangeRequestSignal(self) :
		self.emit(Qt.SIGNAL("visibleChangeRequest()"))

