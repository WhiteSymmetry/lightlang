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
import TranslateBrowser
import TextSearchFrame


##### Public classes #####
class TabbedTranslateBrowser(Qt.QWidget) :
	def __init__(self, parent = None) :
		Qt.QWidget.__init__(self, parent)

		#####

		self.__main_layout = Qt.QVBoxLayout()
		self.__main_layout.setContentsMargins(0, 0, 0, 0)
		self.__main_layout.setSpacing(0)
		self.setLayout(self.__main_layout)

		#####

		self.__shred_lock_flag = False

		self.__translate_browsers_list = []
		self.__old_index = -1

		self.__tmp_text_cursor = Qt.QTextCursor()

		#####

		self.__tab_widget = Qt.QTabWidget(self)
		self.__tab_widget.setTabsClosable(True)
		self.__main_layout.addWidget(self.__tab_widget)

		self.__add_tab_button = Qt.QToolButton(self)
		self.__add_tab_button.setIcon(IconsLoader.icon("tab-new"))
		self.__add_tab_button.setIconSize(Qt.QSize(16, 16))
		self.__add_tab_button.setCursor(Qt.Qt.ArrowCursor)
		self.__add_tab_button.setAutoRaise(True)
		self.__tab_widget.setCornerWidget(self.__add_tab_button, Qt.Qt.TopLeftCorner)

		self.__remove_tab_button = Qt.QToolButton(self)
		self.__remove_tab_button.setIcon(IconsLoader.icon("tab-close"))
		self.__remove_tab_button.setIconSize(Qt.QSize(16, 16))
		self.__remove_tab_button.setCursor(Qt.Qt.ArrowCursor)
		self.__remove_tab_button.setAutoRaise(True)
		self.__tab_widget.setCornerWidget(self.__remove_tab_button, Qt.Qt.TopRightCorner)

		self.__text_search_frame = TextSearchFrame.TextSearchFrame(self)
		self.__text_search_frame.hide()
		self.__main_layout.addWidget(self.__text_search_frame)

		#####

		self.connect(self.__add_tab_button, Qt.SIGNAL("clicked()"), self.addTab)
		self.connect(self.__remove_tab_button, Qt.SIGNAL("clicked()"), self.removeTab)

		self.connect(self.__tab_widget, Qt.SIGNAL("currentChanged(int)"), self.tabChanged)
		self.connect(self.__tab_widget, Qt.SIGNAL("tabCloseRequested(int)"), self.removeTab)

		self.connect(self.__text_search_frame, Qt.SIGNAL("findNextRequest(const QString &)"), self.findNext)
		self.connect(self.__text_search_frame, Qt.SIGNAL("findPreviousRequest(const QString &)"), self.findPrevious)
		self.connect(self.__text_search_frame, Qt.SIGNAL("instantSearchRequest(const QString &)"), self.instantSearch)

		#####

		self.addTab()


	### Public ###

	def setShredLock(self, shred_lock_flag) :
		self.__shred_lock_flag = shred_lock_flag

	def showTextSearchFrame(self) :
		self.__text_search_frame.show()

	def hideTextSearchFrame(self) :
		self.__text_search_frame.hide()

	###

	def addTab(self) :
		translate_browser = TranslateBrowser.TranslateBrowser(self.__tab_widget)
		self.__translate_browsers_list.append(translate_browser)
		index = len(self.__translate_browsers_list) - 1

		self.connect(translate_browser, Qt.SIGNAL("newTabRequest()"), self.addTab)
		self.connect(translate_browser, Qt.SIGNAL("uFindRequest(const QString &)"), self.uFindRequestSignal)
		self.connect(translate_browser, Qt.SIGNAL("cFindRequest(const QString &)"), self.cFindRequestSignal)
		self.connect(translate_browser, Qt.SIGNAL("statusChanged(const QString &)"), self.statusChangedSignal)
		self.connect(translate_browser, Qt.SIGNAL("showTextSearchFrameRequest()"), self.__text_search_frame.show)
		self.connect(translate_browser, Qt.SIGNAL("hideTextSearchFrameRequest()"), self.__text_search_frame.hide)
		self.connect(translate_browser, Qt.SIGNAL("setFoundRequest(bool)"), self.__text_search_frame.setFound)

		translate_browser.setText(tr("<font class=\"info_font\">Empty</font>"))
		self.__tab_widget.addTab(translate_browser, tr("(Untitled)"))
		self.__tab_widget.setCurrentIndex(index)

	def removeTab(self, index = -1) :
		if self.__shred_lock_flag :
			return

		index = ( self.__tab_widget.currentIndex() if index < 0 else index )

		self.__tab_widget.removeTab(index)
		translate_browser = self.__translate_browsers_list.pop(index)
		del translate_browser

		if self.__tab_widget.count() == 0 :
			self.addTab()

	###

	def count(self) :
		return self.__tab_widget.count()

	def currentIndex(self) :
		return self.__tab_widget.currentIndex()

	###

	def setText(self, index, text) :
		self.__translate_browsers_list[index].setText(text)

	def setCaption(self, index, word) :
		self.__tab_widget.setTabText(index, word)

	###

	def text(self, index = -1) :
		index = ( self.__tab_widget.currentIndex() if index < 0 else index )
		return self.__translate_browsers_list[index].text()

	def caption(self, index = -1) :
		index = ( self.__tab_widget.currentIndex() if index < 0 else index )
		return self.__tab_widget.tabText(index)

	def browser(self, index = -1) :
		index = ( self.__tab_widget.currentIndex() if index < 0 else index )
		return self.__translate_browsers_list[index]

	def document(self, index = -1) :
		index = ( self.__tab_widget.currentIndex() if index < 0 else index )
		return self.__translate_browsers_list[index].document()

	###

	def clearPage(self, index = -1) :
		if self.__shred_lock_flag :
			return

		index = ( self.__tab_widget.currentIndex() if index < 0 else index )
		self.__translate_browsers_list[index].setText(tr("<font class=\"info_font\">Empty</font>"))
		self.__tab_widget.setTabText(index, tr("(Untitled)"))

	def clearAll(self) :
		if self.__shred_lock_flag :
			return

		for count in xrange(self.count()) :
			self.removeTab(0)

		self.__text_search_frame.hide()
		self.__text_search_frame.clear()

	def clear(self, index = -1) :
		if self.__shred_lock_flag :
			return

		index = ( self.__tab_widget.currentIndex() if index < 0 else index )
		self.__translate_browsers_list[index].clear()
		self.__tab_widget.setTabText(index, Qt.QString())

	def clearSpecials(self, index = -1) :
		if self.__shred_lock_flag :
			return

		index = ( self.__tab_widget.currentIndex() if index < 0 else index )
		self.__translate_browsers_list[index].clearSpecials()

	###

	def zoomIn(self, index = -1, range = 1) :
		index = ( self.__tab_widget.currentIndex() if index < 0 else index )
		self.__translate_browsers_list[index].zoomIn(range)

	def zoomOut(self, index = -1, range = 1) :
		index = ( self.__tab_widget.currentIndex() if index < 0 else index )
		self.__translate_browsers_list[index].zoomOut(range)

	def zoomNormal(self, index = -1) :
		index = ( self.__tab_widget.currentIndex() if index < 0 else index )
		self.__translate_browsers_list[index].zoomNormal()


	### Private ###

	def findNext(self, word) :
		self.__translate_browsers_list[self.currentIndex()].findNext(word)

	def findPrevious(self, word) :
		self.__translate_browsers_list[self.currentIndex()].findPrevious(word)

	def instantSearch(self, word) :
		self.__translate_browsers_list[self.currentIndex()].instantSearch(word)

	###

	def tabChanged(self, index) :
		self.__translate_browsers_list[self.__old_index].clearSpecials()
		self.__old_index = index
		self.tabChangedSignal(index)


	### Signals ###

	def tabChangedSignal(self, index) :
		self.emit(Qt.SIGNAL("tabChanged(int)"), index)

	def uFindRequestSignal(self, word) :
		self.emit(Qt.SIGNAL("uFindRequest(const QString &)"), word)

	def cFindRequestSignal(self, word) :
		self.emit(Qt.SIGNAL("cFindRequest(const QString &)"), word)

	def statusChangedSignal(self, status) :
		self.emit(Qt.SIGNAL("statusChanged(const QString &)"), status)


	### Handlers ###

	def mouseDoubleClickEvent(self, event) :
		self.addTab()

