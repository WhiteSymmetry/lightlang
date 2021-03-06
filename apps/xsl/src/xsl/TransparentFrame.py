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
class TransparentFrame(Qt.QFrame) :
	def __init__(self, parent = None) :
		Qt.QFrame.__init__(self, parent)

		self.setFrameShape(Qt.QFrame.Box)
		self.setFrameShadow(Qt.QFrame.Raised)

		#####

		self.__enter_flag = False

		self.__css_collection = CssCollection.CssCollection()

		self.__transparent_color = Qt.QColor()
		self.__transparent_alpha = 0

		self.initDrawInstruments()

		#####

		self.connect(self.__css_collection, Qt.SIGNAL("cssChanged()"), self.initDrawInstruments)


	### Private ###

	def initDrawInstruments(self) :
		self.__transparent_color = self.__css_collection.value("transparent_frame_background", "color")
		self.__transparent_alpha = self.__css_collection.value("transparent_frame_background", "opacity")

		self.setAlpha(self.__enter_flag)

	###

	def setAlpha(self, enter_flag) :
		alpha = ( 255 if self.__enter_flag else self.__transparent_alpha )
		self.setStyleSheet(Qt.QString("QFrame {border: 1px solid gray; border-radius: 4px; background-color: rgb(%1, %2, %3, %4);}")
			.arg(self.__transparent_color.red()).arg(self.__transparent_color.green()).arg(self.__transparent_color.blue()).arg(alpha))
		self.__enter_flag = enter_flag

	### Handlers ###

	def enterEvent(self, event) :
		self.setAlpha(True)
		Qt.QFrame.enterEvent(self, event)

	def leaveEvent(self, event) :
		self.setAlpha(False)
		Qt.QFrame.leaveEvent(self, event)

