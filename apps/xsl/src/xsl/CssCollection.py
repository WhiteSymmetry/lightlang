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
import Css


##### Private classes #####
class CssCollectionMultiple(Qt.QObject) :
	def __init__(self, parent = None) :
		Qt.QObject.__init__(self, parent = None)

		#####

		self.__css_collection_dict = {
			"dict_header_font" : {
				"bold_flag" : (None, False, bool),
				"italic_flag" : (None, False, bool),
				"large_flag" : (None, False, bool),
				"color" : (None, Qt.QColor(), Qt.QColor)
			},
			"dict_header_background" : {
				"color" : (None, Qt.QColor(), Qt.QColor)
			},
			"red_alert_background" : {
				"color" : (None, Qt.QColor(), Qt.QColor)
			},
			"highlight_background" : {
				"color" : (None, Qt.QColor(), Qt.QColor),
				"opacity" : (None, 255, int)
			},
			"transparent_frame_background" : {
				"color" : (None, Qt.QColor(), Qt.QColor),
				"opacity" : (None, 255, int)
			}
		}

		self.__css = Css.Css()

		###

		self.__css_class_regexp = Qt.QRegExp("\\.([^(\\{|\\})]*)\\{([^(\\{|\\})]*)\\}")
		self.__css_class_regexp.setMinimal(True)

		self.__css_option_regexp = Qt.QRegExp("([^(\\{|\\})]*):([^(\\{|\\})]*);")
		self.__css_option_regexp.setMinimal(True)

		#####

		self.connect(self.__css, Qt.SIGNAL("cssChanged()"), self.applyCss)

		#####

		self.blockSignals(True)
		self.applyCss()
		self.blockSignals(False)


	### Public ###

	def value(self, group, name) :
		group = str(group)
		name = str(name)
		if self.__css_collection_dict.has_key(group) and self.__css_collection_dict[group].has_key(name) :
			return self.__css_collection_dict[group][name][0]
		else :
			return None

	### Private ###

	def setValue(self, group, name, value = None) :
		group = str(group)
		name = str(name)
		(old_value, default_value, validator) = self.__css_collection_dict[group][name]
		self.__css_collection_dict[group][name] = (validator( value if value != None else default_value ), default_value, validator)

	###

	def applyCss(self) :
		for group_key in self.__css_collection_dict.keys() :
			for name_key in self.__css_collection_dict[group_key].keys() :
				self.setValue(group_key, name_key)

		css = self.__css.css().remove(Qt.QRegExp("\\s"))

		css_class_pos = self.__css_class_regexp.indexIn(css)
		while css_class_pos != -1 :
			css_class_name = self.__css_class_regexp.cap(1)
			css_class_body = self.__css_class_regexp.cap(2)

			css_option_pos = self.__css_option_regexp.indexIn(css_class_body)
			while css_option_pos != -1 :
				css_option_name = self.__css_option_regexp.cap(1)
				css_option_value = self.__css_option_regexp.cap(2)

				if css_class_name == "dict_header_font" :
					if css_option_name == "font-weight" :
						self.setValue(css_class_name, "bold_flag", ( css_option_value == "bold" ))
					elif css_option_name == "font-style" :
						self.setValue(css_class_name, "italic_flag", ( css_option_value == "italic" ))
					elif css_option_name == "font-size" :
						self.setValue(css_class_name, "large_flag", ( css_option_value == "large" ))
					elif css_option_name == "color" :
						self.setValue(css_class_name, "color", css_option_value)

				elif css_class_name == "dict_header_background" :
					if css_option_name == "background-color" :
						self.setValue(css_class_name, "color", css_option_value)

				elif css_class_name == "red_alert_background" :
					if css_option_name == "background-color" :
						self.setValue(css_class_name, "color", css_option_value)

				elif css_class_name == "highlight_background" :
					if css_option_name == "background-color" :
						if css_option_value == "from-palette" :
							self.setValue(css_class_name, "color", Qt.QApplication.palette().color(Qt.QPalette.Highlight))
						else :
							self.setValue(css_class_name, "color", css_option_value)
					if css_option_name == "opacity" :
						self.setValue(css_class_name, "opacity", ( css_option_value.toInt()[0] if css_option_value.toInt()[1] else 255 ))

				elif css_class_name == "transparent_frame_background" :
					if css_option_name == "background-color" :
						if css_option_value == "from-palette" :
							self.setValue(css_class_name, "color", Qt.QApplication.palette().color(Qt.QPalette.Window))
						else :
							self.setValue(css_class_name, "color", css_option_value)
					if css_option_name == "opacity" :
						self.setValue(css_class_name, "opacity", ( css_option_value.toInt()[0] if css_option_value.toInt()[1] else 255 ))

				css_option_pos = self.__css_option_regexp.indexIn(css_class_body, css_option_pos + self.__css_option_regexp.matchedLength())
			css_class_pos = self.__css_class_regexp.indexIn(css, css_class_pos + self.__css_class_regexp.matchedLength())

		self.cssChangedSignal()


	### Signals ###

	def cssChangedSignal(self) :
		self.emit(Qt.SIGNAL("cssChanged()"))


##### Public classes #####
class CssCollection(CssCollectionMultiple) :
	__css_collection_multiple_object = None

	def __new__(self, parent = None) :
		if self.__css_collection_multiple_object == None :
			self.__css_collection_multiple_object = CssCollectionMultiple.__new__(self, parent)
			CssCollectionMultiple.__init__(self.__css_collection_multiple_object, parent)
		return self.__css_collection_multiple_object

	def __init__(self, parent = None) :
		pass

