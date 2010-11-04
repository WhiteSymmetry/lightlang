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


##### Public classes #####
class AboutWindow(Qt.QDialog) :
	def __init__(self, parent = None) :
		Qt.QDialog.__init__(self, parent)

		self.setModal(True)

		self.setWindowIcon(IconsLoader.icon("xsl"))

		#####

		self.__main_layout = Qt.QVBoxLayout()
		self.setLayout(self.__main_layout)

		self.__info_label_layout = Qt.QHBoxLayout()
		self.__main_layout.addLayout(self.__info_label_layout)

		self.__ok_button_layout = Qt.QHBoxLayout()
		self.__ok_button_layout.setAlignment(Qt.Qt.AlignRight)
		self.__main_layout.addLayout(self.__ok_button_layout)

		#####

		self.__icon_label = Qt.QLabel(self)
		self.__icon_label.setAlignment(Qt.Qt.AlignTop)
		self.__icon_label.setPixmap(IconsLoader.icon("xsl_64").pixmap(Qt.QSize(64, 64)))
		self.__info_label_layout.addWidget(self.__icon_label)

		self.__text_label = Qt.QLabel(self)
		self.__text_label.setTextFormat(Qt.Qt.RichText)
		self.__text_label.setOpenExternalLinks(True)
		self.__info_label_layout.addWidget(self.__text_label)

		self.__ok_button = Qt.QPushButton(self)
		self.__ok_button.setDefault(True)
		self.__ok_button_layout.addWidget(self.__ok_button)

		#####

		self.translateUi()

		#####

		self.connect(self.__ok_button, Qt.SIGNAL("clicked()"), self.accept)


	### Private ###

	def translateUi(self) :
		self.setWindowTitle(tr("About %1").arg(Const.MyName))

		self.__text_label.setText(tr("<h3>%1 - the graphical interface for SL</h3>"
			"All the programs of the <strong>%2</strong> package are distributable, according<br>"
			"to the license <strong>GPLv2</strong>. For details visit <em>License agreement</em> of the<br>"
			"<strong>%2</strong> manual.<br>"
			"<br>"
			"Author of the <strong>%2</strong> package:<br>"
			"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<em>Devaev Maxim</em><br>"
			"Thanks to:<br>"
			"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<em>Baburina Elisabeth</em><br>"
			"Valuable assistants:<br>"
			"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<em>Vladimir Fomkin</em><br>"
			"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<em>Tihonov Sergey</em><br>"
			"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<em>Renat Nasyrov</em><br>"
			"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<em>Du Vinh</em><br>"
			"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<em>Aleksey Yum</em><br>"
			"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<em>Olga Polyakova</em><br>"
			"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<em>Vitaly Lipatov</em><br>"
			"Translators:<br>"
			"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<em>Kirill Nebogin</em><br>"
			"<br>"
			"<em>Copyright &copy; 2007-2016 Devaev Maxim (<a href=\"mailto:%3?subject=%2\">%3</a>)</em>")
				.arg(Const.MyName).arg(Const.Package).arg(Const.DeveloperMail))

		self.__ok_button.setText(tr("&OK"))


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

