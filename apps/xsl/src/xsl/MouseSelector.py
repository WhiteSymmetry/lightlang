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
import Logger

try : # Optional python-xlib requires
	import X11Inputs
except :
	Logger.warning("Ignored X11Inputs")
	Logger.attachException(Logger.WarningMessage)


##### Public classes #####
class MouseSelector(Qt.QObject) :
	def __init__(self, parent = None) :
		Qt.QObject.__init__(self, parent)

		#####

		self.__clipboard = Qt.QApplication.clipboard()
		self.__old_selection = Qt.QString()

		self.__timer = Qt.QTimer(self)
		self.__timer.setInterval(300)

		if sys.modules.has_key("X11Inputs") :
			self.__x11_inputs = X11Inputs.X11Inputs()
			self.__modifier = KeyboardModifiersTest.NoModifier

		#####

		self.connect(self.__timer, Qt.SIGNAL("timeout()"), self.checkSelection)


	### Public ###

	def start(self) :
		self.__clipboard.setText(Qt.QString(""), Qt.QClipboard.Selection)
		self.__old_selection.clear()
		self.__timer.start()

	def stop(self) :
		self.__timer.stop()

	def isRunning(self) :
		return self.__timer.isActive()

	###

	def setModifier(self, modifier) :
		self.__modifier = modifier


	### Private ###

	def checkSelection(self) :
		if self.__dict__.has_key("__x11_inputs") :
			if self.__x11_inputs.checkMouseButtons() or self.__x11_inputs.checkModifier(self.__modifier) :
				return

		word = self.__clipboard.text(Qt.QClipboard.Selection)
		word = word.simplified().toLower()
		if word.isEmpty() :
			return

		if word == self.__old_selection : # FIXME (Issue 78)
			return
		self.__old_selection = word

		self.selectionChangedSignal(word)


	### Signals ###

	def selectionChangedSignal(self, word) :
		self.emit(Qt.SIGNAL("selectionChanged(const QString &)"), word)

