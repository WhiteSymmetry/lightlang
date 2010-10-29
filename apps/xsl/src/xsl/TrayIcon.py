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
import IconsLoader
import ActionsCollection
import EntitledMenu
import Logger

try :
	import KeysGrabberThread
except :
	Logger.warning("Ignored X11 hooks: KeysGrabberThread")
	Logger.attachException(Logger.WarningMessage)


##### Public classes #####
class TrayIcon(Qt.QSystemTrayIcon) :
	def __init__(self, parent = None) :
		Qt.QSystemTrayIcon.__init__(self, parent)

		self.setIcon(IconsLoader.icon("xsl_22"))
		self.setToolTip(tr("%1 - graphical interface for SL\nSpy is stopped").arg(Const.MyName))

		#####

		self.connect(ActionsCollection.action("spy_menu", "start_spy"), Qt.SIGNAL("changed()"), self.startSpyChanged)

		try :
			self._keys_grabber_thread = KeysGrabberThread.KeysGrabberThread()
			signal = self._keys_grabber_thread.addHotkey(self.objectName(), KeysGrabberThread.Key_L, KeysGrabberThread.WinModifier)
			self.connect(self._keys_grabber_thread, Qt.SIGNAL(signal), self.visibleChangeRequestSignal)
		except :
			Logger.attachException(Logger.DebugMessage)

		self.connect(self, Qt.SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.act)


	### Private ###

	def act(self, reason) :
		if reason == Qt.QSystemTrayIcon.Trigger :
			self.visibleChangeRequestSignal()
		elif reason == Qt.QSystemTrayIcon.Context :
			menu = EntitledMenu.EntitledMenu(IconsLoader.icon("xsl"), Const.Organization+" "+Const.MyName)
			menu.addAction(ActionsCollection.action("spy_menu", "start_spy"))
			menu.addAction(ActionsCollection.action("spy_menu", "stop_spy"))
			menu.addSeparator()
			menu.addAction(tr("Dictionary window")+( "\tWin+L" if self.__dict__.has_key("_keys_grabber_thread") else "" ),
				self.visibleChangeRequestSignal)
			menu.addSeparator()
			menu.addAction(ActionsCollection.action("application", "exit"))
			menu.exec_(Qt.QCursor.pos())

	###

	def startSpyChanged(self) :
		if ActionsCollection.action("spy_menu", "start_spy").isEnabled() :
			self.setIcon(IconsLoader.icon("xsl_22"))
			self.setToolTip(tr("%1 - graphical interface for SL\nSpy is stopped").arg(Const.MyName))
		else :
			self.setIcon(IconsLoader.icon("xsl+spy_22"))
			self.setToolTip(tr("%1 - graphical interface for SL\nSpy is running").arg(Const.MyName))


	### Signals ###

	def visibleChangeRequestSignal(self) :
		self.emit(Qt.SIGNAL("visibleChangeRequest()"))

