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
import Logger


##### Private constants #####
UserStyleCssFileName = "user-style.css"

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


##### Private classes #####
class CssMultiple(Qt.QObject) :
	def __init__(self, parent = None) :
		Qt.QObject.__init__(self, parent)

		#####

		self.__css = Qt.QString(DefaultCss)
		self.__user_style_css_watcher = Qt.QFileSystemWatcher(self)
		self.applyUserStyleCss(False)

		#####

		self.connect(self.__user_style_css_watcher, Qt.SIGNAL("fileChanged(const QString &)"), ( lambda : self.applyUserStyleCss(True) ))


	### Public static ###

	@classmethod
	def userStyleCssPath(self) :
		return Utils.joinPath(Settings.Settings.dirPath(), UserStyleCssFileName)


	### Public ###

	def css(self) :
		return Qt.QString(self.__css)


	### Private ### :

	def applyUserStyleCss(self, send_signal_flag) :
		user_style_css_file_path = self.userStyleCssPath()
		user_style_css_file = Qt.QFile(user_style_css_file_path)
		user_style_css_file_stream = Qt.QTextStream(user_style_css_file)

		if not user_style_css_file.exists() :
			if user_style_css_file.open(Qt.QIODevice.WriteOnly) :
				Logger.debug(Qt.QString("Created empty CSS file \"%1\"").arg(user_style_css_file_path))
			else :
				Logger.warning(Qt.QString("Cannot open CSS file \"%1\" for reading").arg(user_style_css_file_path))
			user_style_css_file.close()

		if self.__user_style_css_watcher.files().count() < 1 :
			 self.__user_style_css_watcher.addPath(user_style_css_file_path)

		if user_style_css_file.open(Qt.QIODevice.ReadOnly) :
			Logger.debug(Qt.QString("Apply user CSS from \"%1\"").arg(user_style_css_file_path))
			user_style_css = Qt.QString("%1\n%2\n").arg(DefaultCss).arg(user_style_css_file_stream.readAll())
			user_style_css.remove(Qt.QRegExp("/\\*([^*]|\\*[^/]|\\n)*\\*/"))
			user_style_css_file.close()

			if self.__css.trimmed() != user_style_css.trimmed() :
				self.__css = user_style_css
				if send_signal_flag :
					Logger.debug("CSS has been updated")
					self.cssChangedSignal()
		else :
			Logger.warning(Qt.QString("Cannot open CSS file\"%1\" for reading").arg(user_style_css_file_path))


	### Signals ###

	def cssChangedSignal(self) :
		self.emit(Qt.SIGNAL("cssChanged()"))


##### Public classes #####
class Css(CssMultiple) :
	__css_multiple_object = None

	def __new__(self, parent = None) :
		if self.__css_multiple_object == None :
			self.__css_multiple_object = CssMultiple.__new__(self, parent)
			CssMultiple.__init__(self.__css_multiple_object, parent)
		return self.__css_multiple_object

	def __init__(self, parent = None) :
		pass

