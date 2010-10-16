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


##### Private objects #####
CollectionDictObject = {
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


##### Private methods #####
def initCollection() :
	for section_name in CollectionDictObject.keys() :
		for option_name in CollectionDictObject[section_name].keys() :
			setValue(section_name, option_name)

	###

	css = Css.css().remove(Qt.QRegExp("\\s"))

	css_class_regexp = Qt.QRegExp("\\.([^(\\{|\\})]*)\\{([^(\\{|\\})]*)\\}")
	css_class_regexp.setMinimal(True)

	css_option_regexp = Qt.QRegExp("([^(\\{|\\})]*):([^(\\{|\\})]*);")
	css_option_regexp.setMinimal(True)

	css_class_pos = css_class_regexp.indexIn(css)
	while css_class_pos != -1 :
		css_class_name = css_class_regexp.cap(1)
		css_class_body = css_class_regexp.cap(2)

		css_option_pos = css_option_regexp.indexIn(css_class_body)
		while css_option_pos != -1 :
			css_option_name = css_option_regexp.cap(1)
			css_option_value = css_option_regexp.cap(2)

			if css_class_name == "dict_header_font" :
				if css_option_name == "font-weight" :
					setValue(str(css_class_name), "bold_flag", ( css_option_value == "bold" ))
				elif css_option_name == "font-style" :
					setValue(str(css_class_name), "italic_flag", ( css_option_value == "italic" ))
				elif css_option_name == "font-size" :
					setValue(str(css_class_name), "large_flag", ( css_option_value == "large" ))
				elif css_option_name == "color" :
					setValue(str(css_class_name), "color", css_option_value)

			elif css_class_name == "dict_header_background" :
				if css_option_name == "background-color" :
					setValue(str(css_class_name), "color", css_option_value)

			elif css_class_name == "red_alert_background" :
				if css_option_name == "background-color" :
					setValue(str(css_class_name), "color", css_option_value)

			elif css_class_name == "highlight_background" :
				if css_option_name == "background-color" :
					if css_option_value == "from-palette" :
						setValue(str(css_class_name), "color", Qt.QApplication.palette().color(Qt.QPalette.Highlight))
					else :
						setValue(str(css_class_name), "color", css_option_value)
				if css_option_name == "opacity" :
					setValue(str(css_class_name), "opacity", ( css_option_value.toInt()[0] if css_option_value.toInt()[1] else 255 ))

			elif css_class_name == "transparent_frame_background" :
				if css_option_name == "background-color" :
					if css_option_value == "from-palette" :
						setValue(str(css_class_name), "color", Qt.QApplication.palette().color(Qt.QPalette.Window))
					else :
						setValue(str(css_class_name), "color", css_option_value)
				if css_option_name == "opacity" :
					setValue(str(css_class_name), "opacity", ( css_option_value.toInt()[0] if css_option_value.toInt()[1] else 255 ))

			css_option_pos = css_option_regexp.indexIn(css_class_body, css_option_pos + css_option_regexp.matchedLength())
		css_class_pos = css_class_regexp.indexIn(css, css_class_pos + css_class_regexp.matchedLength())

def setValue(section_name, option_name, value = None) :
	(old_value, default_value, validator) = CollectionDictObject[section_name][option_name]
	CollectionDictObject[section_name][option_name] = (validator( value if value != None else default_value ), default_value, validator)


##### Public methods #####
def value(section_name, option_name) :
	if CollectionDictObject[section_name][option_name][0] == None :
		initCollection()
	return CollectionDictObject[section_name][option_name][0]

