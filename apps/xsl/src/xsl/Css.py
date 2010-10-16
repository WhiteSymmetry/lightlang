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
import Utils
import Settings


##### Private constants #####
UserStyleCssName = "user-style.css"

DefaultCss = Qt.QString("\n.dict_header_background {background-color: #DFEDFF;}\n"
	".red_alert_background {background-color: #FF6E6E;}\n"
	".highlight_background {background-color: from-palette; opacity: 70;}\n"
	".transparent_frame_background {background-color: from-palette; opacity: 180;}\n"
	".dict_header_font {font-size: large; font-weight: bold;}\n"
	".word_header_font {color: #494949;}\n"
	".list_item_number_font {font-style: italic;}\n"
	".article_number_font {font-style: italic; font-weight: bold;}\n"
	".strong_font {font-weight: bold;}\n"
	".italic_font {font-style: italic;}\n"
	".green_font {color: #0A7700;}\n"
	".underline_font {font-decoration: underline;}\n"
	".word_link_font {color: #DFEDFF; font-decoration: underline;}\n"
	".sound_link_font {}\n"
	".info_font {font-style: italic;}\n"
	".text_label_font {color: #494949; font-weight: bold;}\n")


##### Private objects #####
CssObject = None


##### Private methods #####
def initCss() :
	global CssObject

	CssObject = Qt.QString(DefaultCss)

	user_style_css_file = Qt.QFile(Utils.joinPath(Settings.settingsPath(), UserStyleCssName))
	user_style_css_file_stream = Qt.QTextStream(user_style_css_file)

	if user_style_css_file.open(Qt.QIODevice.ReadOnly) :
		CssObject.append("\n"+user_style_css_file_stream.readAll()+"\n")
		CssObject.remove(Qt.QRegExp("/\\*([^*]|\\*[^/]|\\n)*\\*/"))
		user_style_css_file.close()


##### Public methods #####
def css() :
	if CssObject == None :
		initCss()

	return Qt.QString(CssObject)

