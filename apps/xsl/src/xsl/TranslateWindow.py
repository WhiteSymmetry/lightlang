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
import Css
import IconsLoader
import PopupWindow
import TextSearchFrame
import TranslateBrowser


##### Public classes #####
class TranslateWindow(PopupWindow.PopupWindow) :
	def __init__(self, parent = None) :
		PopupWindow.PopupWindow.__init__(self, parent)

		#####

		self.__main_layout = Qt.QVBoxLayout()
		self.__main_layout.setContentsMargins(0, 0, 0, 0)
		self.__main_layout.setSpacing(0)
		self.setLayout(self.__main_layout)

		self.__caption_frame = Qt.QFrame(self)
		self.__caption_frame.setMouseTracking(True)
		self.__caption_frame.setFrameShape(Qt.QFrame.Box)
		self.__caption_frame.setFrameShadow(Qt.QFrame.Raised)
		if self.font().pixelSize() > 0 :
			self.__caption_frame.setMaximumHeight((self.font().pixelSize()) * 4)
		elif self.font().pointSize() > 0 :
			self.__caption_frame.setMaximumHeight((self.font().pointSize()) * 4)
		else :
			self.__caption_frame.setMaximumHeight(40)
		self.__main_layout.addWidget(self.__caption_frame)

		self.__caption_frame_layout = Qt.QHBoxLayout()
		self.__caption_frame_layout.setContentsMargins(20, 1, 2, 1)
		self.__caption_frame_layout.setSpacing(1)
		self.__caption_frame.setLayout(self.__caption_frame_layout)

		#####

		self.__settings = Settings.Settings(self)

		self.__css = Css.Css()

		#####

		self.__caption_label = Qt.QLabel(self)
		self.__caption_label.setTextFormat(Qt.Qt.RichText)
		self.__caption_label.setWordWrap(True)
		self.__caption_frame_layout.addWidget(self.__caption_label)

		self.__close_button = Qt.QToolButton(self)
		self.__close_button.setIcon(IconsLoader.icon("dialog-cancel"))
		self.__close_button.setIconSize(Qt.QSize(16, 16))
		self.__close_button.setFixedSize(Qt.QSize(16, 16))
		self.__close_button.setCursor(Qt.Qt.ArrowCursor)
		self.__close_button.setAutoRaise(True)
		self.__caption_frame_layout.addWidget(self.__close_button)

		self.__translate_browser = TranslateBrowser.TranslateBrowser(self)
		self.__main_layout.addWidget(self.__translate_browser)

		self.__text_search_frame = TextSearchFrame.TextSearchFrame(self)
		self.__text_search_frame.hide()
		self.__main_layout.addWidget(self.__text_search_frame)

		#####

		self.connect(self.__close_button, Qt.SIGNAL("clicked()"), self.close)

		self.connect(self.__translate_browser, Qt.SIGNAL("showTextSearchFrameRequest()"), self.__text_search_frame.show)
		self.connect(self.__translate_browser, Qt.SIGNAL("hideTextSearchFrameRequest()"), self.__text_search_frame.hide)
		self.connect(self.__translate_browser, Qt.SIGNAL("setFoundRequest(bool)"), self.__text_search_frame.setFound)
		self.connect(self.__translate_browser, Qt.SIGNAL("newTabRequest()"), self.newTabRequestSignal)
		self.connect(self.__translate_browser, Qt.SIGNAL("uFindRequest(const QString &)"), self.uFindRequestSignal)
		self.connect(self.__translate_browser, Qt.SIGNAL("cFindRequest(const QString &)"), self.cFindRequestSignal)

		self.connect(self.__text_search_frame, Qt.SIGNAL("findNextRequest(const QString &)"), self.__translate_browser.findNext)
		self.connect(self.__text_search_frame, Qt.SIGNAL("findPreviousRequest(const QString &)"), self.__translate_browser.findPrevious)
		self.connect(self.__text_search_frame, Qt.SIGNAL("instantSearchRequest(const QString &)"), self.__translate_browser.instantSearch)

		self.connect(self.__close_button, Qt.SIGNAL("clicked()"), self.close)


	### Public ###

	def setCaption(self, caption) :
		self.__caption_label.setText(Utils.styledHtml(self.__css.css(), caption))

	def setText(self, text) :
		self.__translate_browser.setText(text)

	def clear(self) :
		self.__translate_browser.clear()

	###

	def saveSettings(self) :
		self.__settings.setValue(Qt.QString("%1/size").arg(self.objectName()), Qt.QVariant(self.size()))

	def loadSettings(self) :
		self.resize(self.__settings.value(Qt.QString("%1/size").arg(self.objectName()), Qt.QVariant(Qt.QSize(550, 400))).toSize())

	###

	def setFocus(self, reason = Qt.Qt.OtherFocusReason) :
		self.__translate_browser.setFocus(reason)


	### Private ###

	### Handlers ###

	def showEvent(self, event) :
		self.__text_search_frame.hide()
		PopupWindow.PopupWindow.showEvent(self, event)


	### Signals ###

	def newTabRequestSignal(self) :
		self.emit(Qt.SIGNAL("newTabRequest()"))

	def uFindRequestSignal(self, word) :
		self.emit(Qt.SIGNAL("uFindRequest(const QString &)"), word)

	def cFindRequestSignal(self, word) :
		self.emit(Qt.SIGNAL("cFindRequest(const QString &)"), word)


