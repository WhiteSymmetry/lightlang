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
import IconsLoader
import TextBrowser
import SlDictsInfo


##### Public classes #####
class DictInfoWindow(Qt.QDialog) :
	def __init__(self, dict_name, parent = None) :
		Qt.QDialog.__init__(self, parent)

		self.setWindowIcon(IconsLoader.icon("xsl"))

		self.setMinimumSize(550, 400)
		self.resize(550, 400)

		#####

		self.__main_layout = Qt.QVBoxLayout()
		self.__main_layout.setContentsMargins(0, 0, 0, 0)
		self.__main_layout.setSpacing(0)
		self.setLayout(self.__main_layout)

		self.__dict_info_browser_layout = Qt.QVBoxLayout()
		self.__dict_info_browser_layout.setContentsMargins(0, 0, 0, 0)
		self.__dict_info_browser_layout.setSpacing(0)
		self.__main_layout.addLayout(self.__dict_info_browser_layout)

		self.__control_buttons_layout = Qt.QHBoxLayout()
		self.__control_buttons_layout.setContentsMargins(6, 6, 6, 6)
		self.__control_buttons_layout.setSpacing(6)
		self.__main_layout.addLayout(self.__control_buttons_layout)

		#####

		self.__dict_name = Qt.QString(dict_name)
		self.__info_loaded_flag = False

		self.__sl_dicts_info = SlDictsInfo.SlDictsInfo(self)

		#####

		self.__dict_info_browser = TextBrowser.TextBrowser(self)
		self.__dict_info_browser_layout.addWidget(self.__dict_info_browser)

		self.__wait_picture_movie = IconsLoader.gifMovie("circular")
		icon_width = icon_height = self.style().pixelMetric(Qt.QStyle.PM_SmallIconSize)
		self.__wait_picture_movie.setScaledSize(Qt.QSize(icon_width, icon_height))
		self.__wait_picture_movie.jumpToFrame(0)
		self.__wait_picture_movie_label = Qt.QLabel(self)
		self.__wait_picture_movie_label.setMovie(self.__wait_picture_movie)
		self.__wait_picture_movie_label.hide()
		self.__control_buttons_layout.addWidget(self.__wait_picture_movie_label)

		self.__wait_message_label = Qt.QLabel(self)
		self.__wait_message_label.hide()
		self.__control_buttons_layout.addWidget(self.__wait_message_label)

		self.__control_buttons_layout.addStretch()

		self.__update_info_button = Qt.QPushButton(self)
		self.__update_info_button.setIcon(IconsLoader.icon("view-refresh"))
		self.__control_buttons_layout.addWidget(self.__update_info_button)

		self.__ok_button = Qt.QPushButton(self)
		self.__ok_button.setIcon(IconsLoader.icon("dialog-ok-apply"))
		self.__ok_button.setDefault(True)
		self.__control_buttons_layout.addWidget(self.__ok_button)

		#####

		self.translateUi()

		#####

		self.connect(self.__update_info_button, Qt.SIGNAL("clicked()"), self.updateInfo)
		self.connect(self.__ok_button, Qt.SIGNAL("clicked()"), self.accept)


	### Private ###

	def translateUi(self) :
		self.setWindowTitle(tr("Dict Information"))

		self.__wait_message_label.setText(tr("Please wait..."))
		self.__update_info_button.setText(tr("&Update"))
		self.__ok_button.setText(tr("&OK"))

		if self.isVisible() :
			self.updateInfo()
		else :
			self.__info_loaded_flag = False

	###

	def updateInfo(self) :
		if self.__dict_name.isEmpty() :
			return

		self.__sl_dicts_info.clearInfo(self.__dict_name)

		self.__update_info_button.blockSignals(True)
		self.__update_info_button.setEnabled(False)

		self.__wait_picture_movie_label.show()
		self.__wait_picture_movie.start()
		self.__wait_message_label.show()

		###

		dict_info = Qt.QString()
		dict_info.append(self.tagInfo(tr("Caption"), SlDictsInfo.CaptionTag)).append("<hr>")
		dict_info.append(self.tagInfo(tr("Translate direction"), SlDictsInfo.DirectionTag)).append("<hr>")
		dict_info.append(self.tagInfo(tr("Dictionary group"), SlDictsInfo.GroupTag)).append("<hr>")
		dict_info.append(self.tagInfo(tr("Dictionary version"), SlDictsInfo.VersionTag)).append("<hr>")
		dict_info.append(self.tagInfo(tr("Count of words"), SlDictsInfo.WordCountTag)).append("<hr>")
		dict_info.append(self.tagInfo(tr("File size (KB)"), SlDictsInfo.FileSizeTag)).append("<hr>")
		dict_info.append(self.tagInfo(tr("Author"), SlDictsInfo.AuthorTag)).append("<hr>")
		dict_info.append(self.tagInfo(tr("Homepage"), SlDictsInfo.UrlTag)).append("<hr>")
		dict_info.append(self.tagInfo(tr("License"), SlDictsInfo.LicenseTag)).append("<hr>")
		dict_info.append(self.tagInfo(tr("Copyright"), SlDictsInfo.CopyrightTag)).append("<hr>")
		dict_info.append(self.tagInfo(tr("Description"), SlDictsInfo.MiscTag))
		self.__dict_info_browser.setText(dict_info)

		###

		self.__wait_picture_movie_label.hide()
		self.__wait_picture_movie.stop()
		self.__wait_picture_movie.jumpToFrame(0)
		self.__wait_message_label.hide()

		self.__update_info_button.setEnabled(True)
		self.__update_info_button.blockSignals(False)

	###

	def tagInfo(self, caption, tag) :
		return Qt.QString("<font class=\"text_label_font\">%1</font>: %2").arg(caption,
			self.__sl_dicts_info.info(self.__dict_name, tag))


	### Handlers ###

	def changeEvent(self, event) :
		if event.type() == Qt.QEvent.LanguageChange :
			self.translateUi()
		else :
			Qt.QDialog.changeEvent(self, event)

	def showEvent(self, event) :
		Qt.QDialog.showEvent(self, event)
		self.raise_()
		self.activateWindow()

		if not self.__info_loaded_flag :
			self.updateInfo()
			self.__info_loaded_flag = True

