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
import Settings
import IconsLoader
import LineEdit


##### Public classes #####
class HistoryPanel(Qt.QDockWidget) : # TODO: setObjectName("history_panel")
	def __init__(self, parent = None) :
		Qt.QDockWidget.__init__(self, parent)

		self.setAllowedAreas(Qt.Qt.AllDockWidgetAreas)


		#####

		self.__main_widget = Qt.QWidget(self)
		self.setWidget(self.__main_widget)

		self.__main_layout = Qt.QVBoxLayout()
		self.__main_widget.setLayout(self.__main_layout)

		#####

		self.__settings = Settings.Settings(self)

		#####

		self.__line_edit = LineEdit.LineEdit(self)
		self.__main_layout.addWidget(self.__line_edit)

		self.__history_browser = Qt.QListWidget(self)
		self.__main_layout.addWidget(self.__history_browser)

		self.__clear_history_button = Qt.QPushButton(self)
		self.__clear_history_button.setEnabled(False)
		self.__main_layout.addWidget(self.__clear_history_button)

		#####

		self.connect(self, Qt.SIGNAL("visibilityChanged(bool)"), self.activateDockWidget)

		self.connect(self.__line_edit, Qt.SIGNAL("textChanged(const QString &)"), self.setFilter)

		self.connect(self.__history_browser, Qt.SIGNAL("itemActivated(QListWidgetItem *)"), self.wordChangedSignal)
		self.connect(self.__clear_history_button, Qt.SIGNAL("clicked()"), self.clearHistory)

		#####

		self.translateUi()


	### Public ###

	def requisites(self) :
		return {
			"icon" : IconsLoader.icon("view-history"),
			"title" : Qt.QT_TR_NOOP("Search history"),
			"area" : Qt.Qt.LeftDockWidgetArea,
			"hotkey" : Qt.QKeySequence("Ctrl+H")
		}

	###

	def addWord(self, word) :
		self.__history_browser.insertItem(0, word)

		max_history_count = self.__settings.value(Qt.QString("%1/max_history_count").arg(self.objectName()),
			Qt.QVariant(100)).toInt()[0]

		count = 1
		while count < self.__history_browser.count() and count < max_history_count :
			if self.__history_browser.item(count).text() == word :
				self.__history_browser.takeItem(count)
				break
			count += 1

		count = self.__history_browser.count()
		while count > max_history_count :
			self.__history_browser.takeItem(count - 1)
			count -= 1

		self.__clear_history_button.setEnabled(True)

	###

	def saveSettings(self) :
		self.__settings.setValue(Qt.QString("%1/history_list").arg(self.objectName()), Qt.QVariant(self.historyList()))

	def loadSettings(self) :
		self.setHistoryList(self.__settings.value(Qt.QString("%1/history_list").arg(self.objectName())).toStringList())

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
		self.setWindowTitle(tr("Search history"))
		self.__clear_history_button.setText(tr("Clear history"))

	###

	def historyList(self) :
		history_list = Qt.QStringList()
		for count in xrange(self.__history_browser.count()) :
			history_list << self.__history_browser.item(count).text()
		return history_list

	def setHistoryList(self, history_list) :
		self.__history_browser.addItems(history_list)

		if history_list.count() > 0 :
			self.__clear_history_button.setEnabled(True)

	def setFilter(self, word) :
		word = word.simplified()
		for count in xrange(self.__history_browser.count()) :
			item = self.__history_browser.item(count)
			item_word = item.text();
			item.setHidden(not item_word.startsWith(word, Qt.Qt.CaseInsensitive))

	def clearHistory(self) :
		self.__history_browser.clear()
		self.__clear_history_button.setEnabled(False)

	def activateDockWidget(self, activate_flag) :
		if activate_flag :
			self.__line_edit.setFocus(Qt.Qt.OtherFocusReason)
			self.__line_edit.selectAll()


	### Signals ###

	def wordChangedSignal(self, item) :
		self.emit(Qt.SIGNAL("wordChanged(const QString &)"), item.text())


	### Handlers ###

	def changeEvent(self, event) :
		if event.type() == Qt.QEvent.LanguageChange :
			self.translateUi()
		else :
			Qt.QDockWidget.changeEvent(self, event)

