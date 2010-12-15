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
import Css
import IconsLoader
import LangsList
import HorizontalGrabWidget
import DictInfoWindow


##### Public classes #####
class DictsListWidgetItem(Qt.QWidget) :
	def __init__(self, dict_state_flag, dict_name, parent = None) :
		Qt.QWidget.__init__(self, parent)

		if self.font().pixelSize() > 0 :
			self.setFixedHeight((self.font().pixelSize()) * 4)
		elif self.font().pointSize() > 0 :
			self.setFixedHeight((self.font().pointSize()) * 4)
		else :
			self.setFixedHeight(40)

		#####

		self.__main_layout = Qt.QHBoxLayout()
		self.__main_layout.setContentsMargins(2, 0, 0, 0)
		self.__main_layout.setSpacing(0)
		self.setLayout(self.__main_layout)

		self.__horizontal_grab_widget = HorizontalGrabWidget.HorizontalGrabWidget(self)
		self.__main_layout.addWidget(self.__horizontal_grab_widget)

		self.__enable_dict_checkbox_layout = Qt.QVBoxLayout()
		self.__enable_dict_checkbox_layout.setContentsMargins(5, 5, 5, 5)
		self.__enable_dict_checkbox_layout.setSpacing(3)
		self.__main_layout.addLayout(self.__enable_dict_checkbox_layout)

		self.__vertical_frame1 = Qt.QFrame(self)
		self.__vertical_frame1.setFrameStyle(Qt.QFrame.VLine|Qt.QFrame.Sunken)
		self.__main_layout.addWidget(self.__vertical_frame1)

		self.__dict_info_layout = Qt.QVBoxLayout()
		self.__dict_info_layout.setContentsMargins(10, 1, 10, 1)
		self.__dict_info_layout.setSpacing(1)
		self.__main_layout.addLayout(self.__dict_info_layout)

		self.__dict_name_layout = Qt.QHBoxLayout()
		self.__dict_info_layout.addLayout(self.__dict_name_layout)

		self.__dict_details_layout = Qt.QHBoxLayout()
		self.__dict_info_layout.addLayout(self.__dict_details_layout)

		#####

		self.__dict_name = Qt.QString(dict_name)

		self.__css = Css.Css(self)
		self.__dict_info_window = None

		#####

		self.__enable_dict_checkbox = Qt.QCheckBox(self)
		self.__enable_dict_checkbox.setChecked(dict_state_flag)
		self.__enable_dict_checkbox_layout.addWidget(self.__enable_dict_checkbox)

		###

		self.__dict_caption_label = Qt.QLabel(self)
		self.__dict_caption_label.setTextFormat(Qt.Qt.RichText)
		self.__dict_name_layout.addWidget(self.__dict_caption_label)

		self.__dict_name_layout.addStretch()

		self.__dict_direction_label = Qt.QLabel(self)
		self.__dict_direction_label.setTextFormat(Qt.Qt.RichText)
		self.__dict_name_layout.addWidget(self.__dict_direction_label)

		self.__dict_details_layout.addItem(Qt.QSpacerItem(40, 0))

		self.__dict_full_direction_label = Qt.QLabel(self)
		self.__dict_full_direction_label.setTextFormat(Qt.Qt.RichText)
		self.__dict_details_layout.addWidget(self.__dict_full_direction_label)

		self.__dict_details_layout.insertSpacing(0, 10)
		self.__dict_details_layout.addStretch()

		###

		self.__show_info_button = Qt.QToolButton(self)
		self.__show_info_button.setIcon(IconsLoader.icon("help-about"))
		self.__show_info_button.setIconSize(Qt.QSize(16, 16))
		self.__show_info_button.setCursor(Qt.Qt.ArrowCursor)
		self.__show_info_button.setAutoRaise(True)
		self.__dict_details_layout.addWidget(self.__show_info_button)

		#####

		self.connect(self.__css, Qt.SIGNAL("cssChanged()"), self.setCaptions)

		self.connect(self.__enable_dict_checkbox, Qt.SIGNAL("stateChanged(int)"), self.stateChangedSignal)
		self.connect(self.__show_info_button, Qt.SIGNAL("clicked()"), self.showDictInfo)

		#####

		self.translateUi()


	### Public ###

	def dictState(self) :
		return self.__enable_dict_checkbox.isChecked()

	def dictName(self) :
		return Qt.QString(self.__dict_name)

	###

	def invertDictState(self) :
		self.__enable_dict_checkbox.setChecked(not self.__enable_dict_checkbox.isChecked())


	### Private ###

	def translateUi(self) :
		self.__enable_dict_checkbox.setToolTip(tr("Enter"))
		self.setCaptions()

	###

	def setCaptions(self) :
		dict_name_regexp = Qt.QRegExp("([^\\.]+)\\.((..)-(..))")
		if dict_name_regexp.exactMatch(self.__dict_name) :
			lang_codes_dict = LangsList.langCodes()

			dict_caption = dict_name_regexp.cap(1).replace(Qt.QRegExp("[\\._]"), " ")
			dict_direction = dict_name_regexp.cap(2)
			sl_lang_name = LangsList.langName(dict_name_regexp.cap(3), lang_codes_dict)
			tl_lang_name = LangsList.langName(dict_name_regexp.cap(4), lang_codes_dict)

			self.__dict_caption_label.setText(Utils.styledHtml(self.__css.css(),
				Qt.QString("<font class=\"text_label_font\">%1</font>").arg(dict_caption)))
			self.__dict_direction_label.setText(Utils.styledHtml(self.__css.css(),
				 Qt.QString("<font class=\"text_label_font\">%1</font>").arg(dict_direction)))
			self.__dict_full_direction_label.setText(Qt.QString("%1 &#187; %2").arg(sl_lang_name).arg(tl_lang_name))
		else :
			self.__dict_caption_label.setText(Utils.styledHtml(self.__css.css(),
				Qt.QString("<font class=\"text_label_font\">%1</font>").arg(self.__dict_name)))

	def showDictInfo(self) :
		if self.__dict_info_window == None :
			self.__dict_info_window = DictInfoWindow.DictInfoWindow(self.__dict_name)
		self.__dict_info_window.show()


	### Signals ###

	def stateChangedSignal(self, state) :
		self.emit(Qt.SIGNAL("stateChanged(int)"), state)


	### Handlers ###

	def changeEvent(self, event) :
		if event.type() == Qt.QEvent.LanguageChange :
			self.translateUi()
		else :
			Qt.QWidget.changeEvent(self, event)

