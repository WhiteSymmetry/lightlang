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
import IconsLoader


##### Public classes #####
class CssSettingsTab(Qt.QWidget) :
	def __init__(self, parent = None) :
		Qt.QWidget.__init__(self, parent)

		self._main_layout = Qt.QVBoxLayout()
		self.setLayout(self._main_layout)

		#####

		self._css_browser = Qt.QTextBrowser()
		self._main_layout.addWidget(self._css_browser)

		self._readme_label = Qt.QLabel(tr("With <a href=\"http://wikipedia.org/wiki/CSS\">CSS</a> you can customize the "
			"appearance of any element of XSL.<br>Use <a href=\"http://doc.qt.nokia.com/stylesheet.html\">Qt</a> CSS and "
			"built-in classes <a href=\"xslhelp://common_style_sheets.html\">SL/XSL</a> to override the properties of the elements.<br>"
			"Edit user CSS in an <a href=\"file://%1\">external editor</a>. The new settings will be applied the next run.")
				.arg(Css.userStyleCssPath()))
		self._readme_label.setOpenExternalLinks(True)
		self._readme_label.setTextFormat(Qt.Qt.RichText)
		self._main_layout.addWidget(self._readme_label)


	### Public ###

	def requisites(self) :
		return {
			"icon" : IconsLoader.icon("text-css"),
			"title" : tr("Style Sheets"),
		}

	###

	def saveSettings(self) :
		pass

	def loadSettings(self) :
		self._css_browser.setText(Css.css().trimmed())

