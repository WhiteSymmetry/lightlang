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
import Locale
import Settings
import IconsLoader
import GoogleTranslate
import LangsList
import TextEdit


##### Public classes #####
class GoogleTranslatePanel(Qt.QDockWidget) :
	def __init__(self, parent = None) :
		Qt.QDockWidget.__init__(self, parent)

		self.setAllowedAreas(Qt.Qt.AllDockWidgetAreas)

		#####

		self.__main_widget = Qt.QWidget(self)
		self.setWidget(self.__main_widget)

		self.__main_layout = Qt.QVBoxLayout()
		self.__main_widget.setLayout(self.__main_layout)

		self.__langs_layout = Qt.QHBoxLayout()
		self.__main_layout.addLayout(self.__langs_layout)

		self.__text_edit_layout = Qt.QHBoxLayout()
		self.__main_layout.addLayout(self.__text_edit_layout)

		self.__control_buttons_layout = Qt.QHBoxLayout()
		self.__main_layout.addLayout(self.__control_buttons_layout)

		#####

		self.__settings = Settings.Settings(self)
		self.__google_translate = GoogleTranslate.GoogleTranslate(self)

		#####

		self.__sl_combobox = Qt.QComboBox(self)
		self.__sl_combobox.setSizeAdjustPolicy(Qt.QComboBox.AdjustToMinimumContentsLength)
		self.__sl_combobox.setMaxVisibleItems(15)
		self.__langs_layout.addWidget(self.__sl_combobox)

		self.__invert_langs_button = Qt.QToolButton(self)
		self.__invert_langs_button.setIcon(IconsLoader.icon("go-jump"))
		self.__invert_langs_button.setIconSize(Qt.QSize(16, 16))
		self.__invert_langs_button.setCursor(Qt.Qt.ArrowCursor)
		self.__invert_langs_button.setAutoRaise(True)
		self.__langs_layout.addWidget(self.__invert_langs_button)

		self.__tl_combobox = Qt.QComboBox(self)
		self.__tl_combobox.setSizeAdjustPolicy(Qt.QComboBox.AdjustToMinimumContentsLength)
		self.__tl_combobox.setMaxVisibleItems(15)
		self.__langs_layout.addWidget(self.__tl_combobox)

		self.__text_edit = TextEdit.TextEdit(self)
		self.__text_edit_layout.addWidget(self.__text_edit)

		self.__translate_button = Qt.QPushButton(self)
		self.__translate_button.setEnabled(False)
		self.__control_buttons_layout.addWidget(self.__translate_button)

		self.__abort_button = Qt.QToolButton(self)
		self.__abort_button.setIcon(IconsLoader.icon("dialog-cancel"))
		self.__abort_button.setIconSize(Qt.QSize(16, 16))
		self.__abort_button.setEnabled(False)
		self.__control_buttons_layout.addWidget(self.__abort_button)

		#####

		self.connect(self, Qt.SIGNAL("visibilityChanged(bool)"), self.activateDockWidget)

		self.connect(self.__google_translate, Qt.SIGNAL("processStarted()"), self.processStarted)
		self.connect(self.__google_translate, Qt.SIGNAL("processFinished()"), self.processFinished)
		self.connect(self.__google_translate, Qt.SIGNAL("clearRequest()"), self.clearRequestSignal)
		self.connect(self.__google_translate, Qt.SIGNAL("wordChanged(const QString &)"), self.wordChangedSignal)
		self.connect(self.__google_translate, Qt.SIGNAL("textChanged(const QString &)"), self.textChangedSignal)
		self.connect(self.__google_translate, Qt.SIGNAL("statusChanged(const QString &)"), self.statusChangedSignal)

		self.connect(self.__invert_langs_button, Qt.SIGNAL("clicked()"), self.invertLangs)

		self.connect(self.__text_edit, Qt.SIGNAL("textChanged()"), self.setStatusFromTextEdit)
		self.connect(self.__text_edit, Qt.SIGNAL("textApplied()"), self.__translate_button.animateClick)

		self.connect(self.__translate_button, Qt.SIGNAL("clicked()"), self.translate)
		self.connect(self.__translate_button, Qt.SIGNAL("clicked()"), self.setFocus)
		self.connect(self.__abort_button, Qt.SIGNAL("clicked()"), self.abort)

		#####

		self.translateUi()


	### Public ###

	def requisites(self) :
		return {
			"icon" : IconsLoader.icon("applications-internet"),
			"title" : Qt.QT_TR_NOOP("Google Translate"),
			"area" : Qt.Qt.LeftDockWidgetArea,
			"hotkey" : Qt.QKeySequence("Ctrl+G")
		}

	def translateMethods(self) :
		return [
			{
				"title" : Qt.QT_TR_NOOP("Google Translate"),
				"object_name" : self.objectName(),
				"method_name" : self.googleTranslateMethod.__name__,
				"method" : self.googleTranslateMethod
			}
		]

	###

	def setText(self, text) :
		self.__text_edit.setText(text)

	###

	def googleTranslateMethod(self, text) :
		self.setText(text)
		self.translate()

	###

	def saveSettings(self) :
		for (combobox, key) in ((self.__sl_combobox, "sl_lang"), (self.__tl_combobox, "tl_lang")) :
			self.__settings.setValue(Qt.QString("%1/%2").arg(self.objectName()).arg(key),
				combobox.itemData(combobox.currentIndex()).toString())

	def loadSettings(self) :
		for (combobox, key) in ((self.__sl_combobox, "sl_lang"), (self.__tl_combobox, "tl_lang")) :
			lang = self.__settings.value(Qt.QString("%1/%2").arg(self.objectName()).arg(key)).toString()
			for count in xrange(combobox.count()) :
				if combobox.itemData(count).toString() == lang and not combobox.itemText(count).isEmpty() :
					combobox.setCurrentIndex(count)
					break

	###

	def show(self) :
		Qt.QDockWidget.show(self)
		self.raise_()
		self.setFocus()

	def setFocus(self, reason = Qt.Qt.OtherFocusReason) :
		self.__text_edit.setFocus(reason)
		self.__text_edit.selectAll()

	def hasInternalFocus(self) :
		return self.__text_edit.hasFocus()

	def clear(self) :
		self.__text_edit.clear()


	### Private ###

	def translateUi(self) :
		self.setWindowTitle(tr("Google Translate"))
		self.__translate_button.setText(tr("T&ranslate"))
		self.__translate_button.setToolTip(tr("Ctrl+Enter"))

		###

		lang_codes_dict = LangsList.langCodes()
		main_lang = Locale.Locale().mainLang()

		sl_lang = self.__sl_combobox.itemData(self.__sl_combobox.currentIndex()).toString()
		self.__sl_combobox.clear()
		self.__sl_combobox.addItem(IconsLoader.icon("help-hint"), tr("Guess"), Qt.QVariant(""))
		self.__sl_combobox.insertSeparator(1)

		tl_lang = self.__tl_combobox.itemData(self.__tl_combobox.currentIndex()).toString()
		self.__tl_combobox.clear()
		self.__tl_combobox.addItem(IconsLoader.icon(Utils.joinPath("flags", main_lang)),
			LangsList.langName(main_lang, lang_codes_dict), Qt.QVariant(main_lang))
		self.__tl_combobox.insertSeparator(1)

		for combobox in (self.__sl_combobox, self.__tl_combobox) :
			for lang_codes_dict_key in lang_codes_dict.keys() :
				combobox.addItem(IconsLoader.icon(Utils.joinPath("flags", lang_codes_dict_key)),
					LangsList.langName(lang_codes_dict_key, lang_codes_dict), Qt.QVariant(lang_codes_dict_key))

		for (combobox, lang) in ((self.__sl_combobox, sl_lang), (self.__tl_combobox, tl_lang)) :
			for count in xrange(combobox.count()) :
				if combobox.itemData(count).toString() == lang and not combobox.itemText(count).isEmpty() :
					combobox.setCurrentIndex(count)

	###

	def invertLangs(self) :
		sl_index = self.__sl_combobox.currentIndex()
		tl_index = self.__tl_combobox.currentIndex()

		self.__sl_combobox.setCurrentIndex(tl_index)
		self.__tl_combobox.setCurrentIndex(sl_index)

	def translate(self) :
		text = self.__text_edit.toPlainText()
		if text.simplified().isEmpty() :
			return

		sl = self.__sl_combobox.itemData(self.__sl_combobox.currentIndex()).toString()
		tl = self.__tl_combobox.itemData(self.__tl_combobox.currentIndex()).toString()
		self.__google_translate.translate(sl, tl, text)

	def abort(self) :
		self.__google_translate.abort()

	###

	def processStarted(self) :
		self.__abort_button.setEnabled(True)
		self.__translate_button.setEnabled(False)

		self.processStartedSignal()

	def processFinished(self) :
		self.__abort_button.setEnabled(False)
		self.__translate_button.setEnabled(not self.__text_edit.toPlainText().simplified().isEmpty())

		self.processFinishedSignal()

	###

	def setStatusFromTextEdit(self) :
		self.__translate_button.setEnabled(not self.__text_edit.toPlainText().simplified().isEmpty())

	###

	def activateDockWidget(self, activate_flag) :
		if activate_flag :
			self.__text_edit.setFocus(Qt.Qt.OtherFocusReason)
			self.__text_edit.selectAll()


	### Signals ###

	def processStartedSignal(self) :
		self.emit(Qt.SIGNAL("processStarted()"))

	def processFinishedSignal(self) :
		self.emit(Qt.SIGNAL("processFinished()"))

	def wordChangedSignal(self, word) :
		self.emit(Qt.SIGNAL("wordChanged(const QString &)"), word)

	def textChangedSignal(self, text) :
		self.emit(Qt.SIGNAL("textChanged(const QString &)"), text)

	def clearRequestSignal(self) :
		self.emit(Qt.SIGNAL("clearRequest()"))

	def statusChangedSignal(self, status) :
		self.emit(Qt.SIGNAL("statusChanged(const QString &)"), status)


	### Handlers ###

	def changeEvent(self, event) :
		if event.type() == Qt.QEvent.LanguageChange :
			self.translateUi()
		else :
			Qt.QDockWidget.changeEvent(self, event)

