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
import LineEdit
import SlWordSearch
import SlListBrowser


##### Public classes #####
class SlSearchPanel(Qt.QDockWidget) : # TODO: setObjectName("sl_search_panel")
	def __init__(self, parent = None) :
		Qt.QDockWidget.__init__(self, parent)

		self.setAllowedAreas(Qt.Qt.AllDockWidgetAreas)
		self.setFeatures(Qt.QDockWidget.DockWidgetFloatable|Qt.QDockWidget.DockWidgetMovable)


		#####

		self.__main_widget = Qt.QWidget(self)
		self.setWidget(self.__main_widget)

		self.__main_layout = Qt.QVBoxLayout()
		self.__main_widget.setLayout(self.__main_layout)

		self.__line_edit_layout = Qt.QHBoxLayout()
		self.__main_layout.addLayout(self.__line_edit_layout)

		self.__list_browser_layout = Qt.QVBoxLayout()
		self.__main_layout.addLayout(self.__list_browser_layout)

		self.__bottom_search_buttons_layout = Qt.QHBoxLayout()
		self.__main_layout.addLayout(self.__bottom_search_buttons_layout)

		#####

		self.__delay_timer = Qt.QTimer(self)
		self.__delay_timer.setInterval(300)

		self.__internal_word_search = SlWordSearch.SlWordSearch(self)
		self.__external_word_search = SlWordSearch.SlWordSearch(self)

		#####

		self.__line_edit = LineEdit.LineEdit(self)
		self.__line_edit_layout.addWidget(self.__line_edit)

		self.__u_find_button = Qt.QPushButton(self)
		self.__u_find_button.setEnabled(False)
		self.__line_edit_layout.addWidget(self.__u_find_button)

		self.__list_browser = SlListBrowser.SlListBrowser(self)
		self.__list_browser_layout.addWidget(self.__list_browser)

		self.__c_find_button = Qt.QPushButton(self)
		self.__c_find_button.setEnabled(False)
		self.__bottom_search_buttons_layout.addWidget(self.__c_find_button)

		self.__i_find_button = Qt.QPushButton(self)
		self.__i_find_button.setEnabled(False)
		self.__bottom_search_buttons_layout.addWidget(self.__i_find_button)

		#####

		self.connect(self, Qt.SIGNAL("visibilityChanged(bool)"), self.activateDockWidget)

		self.connect(self.__delay_timer, Qt.SIGNAL("timeout()"), self.lFindAfterDelay)

		self.connect(self.__internal_word_search, Qt.SIGNAL("clearRequest()"), self.__list_browser.clear)
		self.connect(self.__internal_word_search, Qt.SIGNAL("listChanged(const QStringList &)"), self.__list_browser.setList)

		self.connect(self.__external_word_search, Qt.SIGNAL("processStarted()"), self.processStarted)
		self.connect(self.__external_word_search, Qt.SIGNAL("processFinished()"), self.processFinished)
		self.connect(self.__external_word_search, Qt.SIGNAL("clearRequest()"), self.clearRequestSignal)
		self.connect(self.__external_word_search, Qt.SIGNAL("textChanged(const QString &)"), self.textChangedSignal)

		self.connect(self.__line_edit, Qt.SIGNAL("returnPressed()"), self.__u_find_button.animateClick)
		self.connect(self.__line_edit, Qt.SIGNAL("textChanged(const QString &)"), self.setStatusFromLineEdit)
		self.connect(self.__line_edit, Qt.SIGNAL("textChanged(const QString &)"), self.__delay_timer.start)

		self.connect(self.__u_find_button, Qt.SIGNAL("clicked()"), self.uFind)
		self.connect(self.__u_find_button, Qt.SIGNAL("clicked()"), self.setFocus)

		self.connect(self.__list_browser, Qt.SIGNAL("uFindRequest(const QString &)"), self.uFind)
		self.connect(self.__list_browser, Qt.SIGNAL("uFindInNewTabRequest(const QString &)"), self.uFindInNewTab)
		self.connect(self.__list_browser, Qt.SIGNAL("cFindInNewTabRequest(const QString &)"), self.cFindInNewTab)

		self.connect(self.__c_find_button, Qt.SIGNAL("clicked()"), self.cFind)
		self.connect(self.__c_find_button, Qt.SIGNAL("clicked()"), self.setFocus)

		self.connect(self.__i_find_button, Qt.SIGNAL("clicked()"), self.iFind)
		self.connect(self.__i_find_button, Qt.SIGNAL("clicked()"), self.setFocus)

		#####

		self.translateUi()


	### Public ###

	def requisites(self) :
		return {
			"icon" : IconsLoader.icon("xsl"),
			"title" : Qt.QT_TR_NOOP("SL Search"),
			"area" : Qt.Qt.LeftDockWidgetArea,
			"hotkey" : Qt.QKeySequence("Ctrl+S")
		}

	def translateMethods(self) :
		return [
			{
				"title" : Qt.QT_TR_NOOP("SL usually search"),
				"object_name" : self.objectName(),
				"method_name" : self.uFindTranslateMethod.__name__,
				"method" : self.uFindTranslateMethod
			},
			{
				"title" : Qt.QT_TR_NOOP("SL expanded search"),
				"object_name" : self.objectName(),
				"method_name" : self.cFindTranslateMethod.__name__,
				"method" : self.cFindTranslateMethod
			}
		]

	###

	def setWord(self, word) :
		self.__line_edit.setText(word)
		self.setFocus()

	def setDictsList(self, dicts_list) :
		self.__internal_word_search.setDictsList(dicts_list)
		self.__external_word_search.setDictsList(dicts_list)

	###

	def uFind(self, word = None) :
		word = ( self.__line_edit.text().simplified() if word == None else word.simplified() )
		if word.isEmpty() :
			return
		self.__external_word_search.uFind(word)
		self.wordChangedSignal(word)

	def cFind(self, word = None) :
		word = ( self.__line_edit.text().simplified() if word == None else word.simplified() )
		if word.isEmpty() :
			return
		self.__external_word_search.cFind(word)
		self.wordChangedSignal(word)

	def lFind(self, word = None) :
		word = ( self.__line_edit.text().simplified() if word == None else word.simplified() )
		if word.isEmpty() :
			self.__list_browser.setText(tr("Enter the word, please"))
			return
		self.__internal_word_search.lFind(word)

	def iFind(self, word = None) :
		word = ( self.__line_edit.text().simplified() if word == None else word.simplified() )
		if word.isEmpty() :
			self.__list_browser.setText(tr("Enter the word, please"))
			return
		self.__internal_word_search.iFind(word)

	def uFindInNewTab(self, word = None) :
		word = ( self.__line_edit.text().simplified() if word == None else word.simplified() )
		if word.isEmpty() :
			return
		self.newTabRequestSignal()
		self.__external_word_search.uFind(word)
		self.wordChangedSignal(word)

	def cFindInNewTab(self, word = None) :
		word = ( self.__line_edit.text().simplified() if word == None else word.simplified() )
		if word.isEmpty() :
			return
		self.newTabRequestSignal()
		self.__external_word_search.cFind(word)
		self.wordChangedSignal(word)

	###

	def uFindTranslateMethod(self, word) :
		self.setWord(word)
		self.uFind(word)

	def cFindTranslateMethod(self, word) :
		self.setWord(word)
		self.cFind(word)

	###

	def saveSettings(self) :
		pass

	def loadSettings(self) :
		pass

	###

	def show(self) :
		Qt.QDockWidget.show(self)
		self.raise_()
		self.setFocus()

	def setFocus(self, reason = Qt.Qt.OtherFocusReason) :
		self.__line_edit.setFocus(reason)
		self.__line_edit.selectAll()

	def hasInternalFocus(self) :
		return self.__line_edit.hasFocus()

	def clear(self) :
		self.__line_edit.clear()


	### Private ###

	def translateUi(self) :
		self.setWindowTitle(tr("SL Search"))

		self.__u_find_button.setText(tr("&Search"))
		self.__c_find_button.setText(tr("&Expanded search"))
		self.__i_find_button.setText(tr("S&imilar words"))

		self.lFind()

	###

	def lFindAfterDelay(self) :
		self.__delay_timer.stop()
		self.lFind()

	###

	def processStarted(self) :
		self.__u_find_button.setEnabled(False)
		self.__c_find_button.setEnabled(False)
		self.__i_find_button.setEnabled(False)

		self.processStartedSignal()

	def processFinished(self) :
		line_edit_empty_flag = self.__line_edit.text().simplified().isEmpty()
		self.__u_find_button.setEnabled(not line_edit_empty_flag)
		self.__c_find_button.setEnabled(not line_edit_empty_flag)
		self.__i_find_button.setEnabled(not line_edit_empty_flag)

		self.processFinishedSignal()
	###

	def setStatusFromLineEdit(self, word) :
		line_edit_empty_flag = word.simplified().isEmpty()
		self.__u_find_button.setEnabled(not line_edit_empty_flag)
		self.__c_find_button.setEnabled(not line_edit_empty_flag)
		self.__i_find_button.setEnabled(not line_edit_empty_flag)

	###

	def activateDockWidget(self, activate_flag) :
		if activate_flag :
			self.__line_edit.setFocus(Qt.Qt.OtherFocusReason)
			self.__line_edit.selectAll()


	### Signals ###

	def processStartedSignal(self) :
		self.emit(Qt.SIGNAL("processStarted()"))

	def processFinishedSignal(self) :
		self.emit(Qt.SIGNAL("processFinished()"))

	def wordChangedSignal(self, word) :
		self.emit(Qt.SIGNAL("wordChanged(const QString &)"), word)

	def textChangedSignal(self, text) :
		self.emit(Qt.SIGNAL("textChanged(const QString &)"), text)

	def newTabRequestSignal(self) :
		self.emit(Qt.SIGNAL("newTabRequest()"))

	def clearRequestSignal(self) :
		self.emit(Qt.SIGNAL("clearRequest()"))


	### Handlers ###

	def changeEvent(self, event) :
		if event.type() == Qt.QEvent.LanguageChange :
			self.translateUi()
		else :
			Qt.QDockWidget.changeEvent(self, event)

