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
import IconsLoader
import LineEdit


##### Public classes #####
class TextSearchFrame(Qt.QFrame) :
	def __init__(self, parent = None) :
		Qt.QFrame.__init__(self, parent)

		self.setFrameShape(Qt.QFrame.Box)

		#####

		self.__main_layout = Qt.QHBoxLayout()
		self.__main_layout.setContentsMargins(3, 0, 3, 0)
		self.setLayout(self.__main_layout)

		#####

		self.__close_button = Qt.QToolButton(self)
		self.__close_button.setIcon(IconsLoader.icon("dialog-cancel"))
		self.__close_button.setIconSize(Qt.QSize(16, 16))
		self.__main_layout.addWidget(self.__close_button)

		self.__vertical_frame1 = Qt.QFrame(self)
		self.__vertical_frame1.setFrameStyle(Qt.QFrame.VLine|Qt.QFrame.Sunken)
		self.__vertical_frame1.setMinimumSize(22, 22)
		self.__main_layout.addWidget(self.__vertical_frame1)

		self.__line_edit_label = Qt.QLabel(tr("Search:"), self)
		self.__main_layout.addWidget(self.__line_edit_label)

		self.__line_edit = LineEdit.LineEdit(self)
		self.__main_layout.addWidget(self.__line_edit)

		self.__vertical_frame2 = Qt.QFrame(self)
		self.__vertical_frame2.setFrameStyle(Qt.QFrame.VLine|Qt.QFrame.Sunken)
		self.__main_layout.addWidget(self.__vertical_frame2)

		self.__next_button = Qt.QToolButton(self)
		self.__next_button.setIcon(IconsLoader.icon("go-down"))
		self.__next_button.setIconSize(Qt.QSize(16, 16))
		self.__next_button.setEnabled(False)
		self.__main_layout.addWidget(self.__next_button)

		self.__previous_button = Qt.QToolButton(self)
		self.__previous_button.setIcon(IconsLoader.icon("go-up"))
		self.__previous_button.setIconSize(Qt.QSize(16, 16))
		self.__previous_button.setEnabled(False)
		self.__main_layout.addWidget(self.__previous_button)

		#####

		self.__found_flag = True

		self.__css_collection = CssCollection.CssCollection()

		self.__line_edit_default_palette = Qt.QPalette()
		self.__line_edit_red_alert_palette = Qt.QPalette()

		#####

		self.connect(self.__close_button, Qt.SIGNAL("clicked()"), self.hide)

		self.connect(self.__line_edit, Qt.SIGNAL("returnPressed()"), self.__next_button.animateClick)
		self.connect(self.__line_edit, Qt.SIGNAL("textChanged(const QString &)"), self.setStatusFromLineEdit)
		self.connect(self.__line_edit, Qt.SIGNAL("textChanged(const QString &)"), self.instantSearchRequest)

		self.connect(self.__next_button, Qt.SIGNAL("clicked()"), self.findNextRequest)

		self.connect(self.__previous_button, Qt.SIGNAL("clicked()"), self.findPreviousRequest)

		self.connect(self.__css_collection, Qt.SIGNAL("cssChanged()"), self.initDrawInstruments)

		#####

		self.initDrawInstruments()


	### Public ###

	def show(self) :
		Qt.QFrame.show(self)
		self.raise_()
		self.setFocus()

	def setFocus(self, reason = Qt.Qt.OtherFocusReason) :
		self.__line_edit.setFocus(reason)
		self.__line_edit.selectAll()

	###

	def setFound(self, found_flag) :
		self.__line_edit.setPalette(self.__line_edit_default_palette if found_flag else self.__line_edit_red_alert_palette)
		found_flag = self.__found_flag

	###

	def clear(self) :
		self.__line_edit.clear()


	### Private ###

	def initDrawInstruments(self) :
		self.__line_edit_default_palette = Qt.QPalette(Qt.QApplication.palette())

		self.__line_edit_red_alert_palette = Qt.QPalette()
		alert_color = self.__css_collection.value("red_alert_background", "color")
		if alert_color.isValid() :
			self.__line_edit_red_alert_palette.setColor(Qt.QPalette.Base, alert_color)

		self.setFound(self.__found_flag)

	###

	def findNextRequest(self) :
		word = self.__line_edit.text()
		if word.simplified().isEmpty() :
			return
		self.findNextRequestSignal(word)

	def findPreviousRequest(self) :
		word = self.__line_edit.text()
		if word.simplified().isEmpty() :
			return
		self.findPreviousRequestSignal(word)

	def instantSearchRequest(self, word) :
		self.instantSearchRequestSignal(word)

	###

	def setStatusFromLineEdit(self, word) :
		line_edit_empty_flag = word.simplified().isEmpty()
		self.__next_button.setEnabled(not line_edit_empty_flag)
		self.__previous_button.setEnabled(not line_edit_empty_flag)


	### Signals ###

	def findNextRequestSignal(self, word) :
		self.emit(Qt.SIGNAL("findNextRequest(const QString &)"), word)

	def findPreviousRequestSignal(self, word) :
		self.emit(Qt.SIGNAL("findPreviousRequest(const QString &)"), word)

	def instantSearchRequestSignal(self, word) :
		self.emit(Qt.SIGNAL("instantSearchRequest(const QString &)"), word)


	### Handlers ###

	def keyPressEvent(self, event) :
		if event.key() == Qt.Qt.Key_Escape :
			self.hide()
		Qt.QFrame.keyPressEvent(self, event)

	def hideEvent(self, event) :
		self.instantSearchRequestSignal(Qt.QString())
		Qt.QFrame.hideEvent(self, event)

	def closeEvent(self, event) :
		self.instantSearchRequestSignal(Qt.QString())
		Qt.QFrame.closeEvent(self, event)

