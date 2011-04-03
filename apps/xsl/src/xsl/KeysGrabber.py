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


import Xlib.display
import Xlib.XK
import Xlib.X

import Qt


##### Public constants #####
Key_L = Xlib.XK.XK_L
Key_F1 = Xlib.XK.XK_F1 # For example

CtrlModifier = Xlib.X.ControlMask
AltModifier = Xlib.X.Mod1Mask
ShiftModifier = Xlib.X.ShiftMask
WinModifier = Xlib.X.Mod4Mask


##### Private classes #####
class KeysGrabberMultiple(Qt.QThread) :
	def __init__(self, parent = None) :
		Qt.QThread.__init__(self, parent)

		#####

		self.__is_stopped_flag = True

		self.__hotkeys_list = []

		self.__display = Xlib.display.Display()
		self.__root = self.__display.screen().root
		self.__root.change_attributes(event_mask = Xlib.X.PropertyChangeMask|Xlib.X.KeyPressMask)

		#####

		self.connect(Qt.QApplication.instance(), Qt.SIGNAL("aboutToQuit()"), self.stop)


	### Public ###

	def addHotkey(self, key, modifier) :
		self.__is_stopped_flag = True
		if not self.wait(100) :
			self.terminate()

		key = self.__display.keysym_to_keycode(key)
		modifier = modifier & ~(Xlib.X.AnyModifier << 1)
		identifier = str(key)+str(modifier)
		self.__hotkeys_list.append({ "key" : key, "modifier" : modifier, "identifier" : identifier })
		self.__root.grab_key(key, modifier, True, Xlib.X.GrabModeAsync, Xlib.X.GrabModeAsync)

		self.__is_stopped_flag = False
		self.start()

		return Qt.QString(identifier)


	### Private ###

	def run(self) :
		while not self.__is_stopped_flag :
			event = self.__root.display.next_event()
			if event.type != Xlib.X.KeyRelease :
				continue

			for hotkeys_list_item in self.__hotkeys_list :
				if ( (event.state & hotkeys_list_item["modifier"]) == hotkeys_list_item["modifier"] and
					event.detail == hotkeys_list_item["key"] ) :
					self.keyPressedSignal(hotkeys_list_item["identifier"])

	def stop(self) :
		self.__is_stopped_flag = True
		if not self.wait(100) :
			self.terminate()

		for hotkeys_list_item in self.__hotkeys_list :
			self.__root.ungrab_key(hotkeys_list_item["key"], hotkeys_list_item["modifier"])


	### Signals ###

	def keyPressedSignal(self, identifier) :
		self.emit(Qt.SIGNAL("keyPressed(const QString &)"), identifier)


##### Public classes #####
class KeysGrabber(KeysGrabberMultiple) :
	__keys_grabber_multiple_object = None

	def __new__(self, parent = None) :
		if self.__keys_grabber_multiple_object == None :
			self.__keys_grabber_multiple_object = KeysGrabberMultiple.__new__(self, parent)
			KeysGrabberMultiple.__init__(self.__keys_grabber_multiple_object, parent)
		return self.__keys_grabber_multiple_object

	def __init__(self, parent = None) :
		pass

