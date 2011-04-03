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
import Utils
import Locale
import Settings
import IconsLoader
import TextBrowser
import TextSearchFrame
import TransparentFrame


##### Private classes #####
class HelpBrowserWindowMultiple(Qt.QDialog) :
	def __init__(self, parent = None) :
		Qt.QDialog.__init__(self, parent)

		self.setWindowIcon(IconsLoader.icon("xsl"))

		#####

		self.__main_layout = Qt.QVBoxLayout()
		self.__main_layout.setContentsMargins(0, 0, 0, 0)
		self.__main_layout.setSpacing(0)
		self.setLayout(self.__main_layout)

		#####

		self.__index_file_url = Qt.QUrl()

		self.__settings = Settings.Settings(self)
		self.__locale = Locale.Locale()

		#####

		self.__text_browser = TextBrowser.TextBrowser(self)
		self.__text_browser_layout = Qt.QHBoxLayout()
		self.__text_browser_layout.setAlignment(Qt.Qt.AlignLeft|Qt.Qt.AlignTop)
		self.__text_browser.setLayout(self.__text_browser_layout)
		self.__main_layout.addWidget(self.__text_browser)

		###

		self.__control_buttons_frame = TransparentFrame.TransparentFrame(self)
		self.__control_buttons_frame_layout = Qt.QHBoxLayout()
		self.__control_buttons_frame_layout.setContentsMargins(0, 0, 0, 0)
		self.__control_buttons_frame.setLayout(self.__control_buttons_frame_layout)
		self.__text_browser_layout.addWidget(self.__control_buttons_frame)

		self.__backward_button = Qt.QToolButton(self)
		self.__backward_button.setIcon(IconsLoader.icon("go-previous"))
		self.__backward_button.setIconSize(Qt.QSize(22, 22))
		self.__backward_button.setCursor(Qt.Qt.ArrowCursor)
		self.__backward_button.setAutoRaise(True)
		self.__backward_button.setEnabled(False)
		self.__control_buttons_frame_layout.addWidget(self.__backward_button)

		self.__forward_button = Qt.QToolButton(self)
		self.__forward_button.setIcon(IconsLoader.icon("go-next"))
		self.__forward_button.setIconSize(Qt.QSize(22, 22))
		self.__forward_button.setCursor(Qt.Qt.ArrowCursor)
		self.__forward_button.setAutoRaise(True)
		self.__forward_button.setEnabled(False)
		self.__control_buttons_frame_layout.addWidget(self.__forward_button)

		self.__vertical_frame1 = Qt.QFrame(self)
		self.__vertical_frame1.setFrameStyle(Qt.QFrame.VLine|Qt.QFrame.Sunken)
		self.__control_buttons_frame_layout.addWidget(self.__vertical_frame1)

		self.__home_button = Qt.QToolButton(self)
		self.__home_button.setIcon(IconsLoader.icon("go-home"))
		self.__home_button.setIconSize(Qt.QSize(22, 22))
		self.__home_button.setCursor(Qt.Qt.ArrowCursor)
		self.__home_button.setAutoRaise(True)
		self.__control_buttons_frame_layout.addWidget(self.__home_button)

		self.__control_buttons_frame.setFixedSize(self.__control_buttons_frame_layout.minimumSize())

		###

		self.__tools_buttons_frame = TransparentFrame.TransparentFrame(self)
		self.__tools_buttons_frame_layout = Qt.QHBoxLayout()
		self.__tools_buttons_frame_layout.setContentsMargins(0, 0, 0, 0)
		self.__tools_buttons_frame.setLayout(self.__tools_buttons_frame_layout)
		self.__text_browser_layout.addWidget(self.__tools_buttons_frame)

		self.__show_text_search_frame_button = Qt.QToolButton(self)
		self.__show_text_search_frame_button.setIcon(IconsLoader.icon("edit-find"))
		self.__show_text_search_frame_button.setIconSize(Qt.QSize(22, 22))
		self.__show_text_search_frame_button.setCursor(Qt.Qt.ArrowCursor)
		self.__show_text_search_frame_button.setAutoRaise(True)
		self.__tools_buttons_frame_layout.addWidget(self.__show_text_search_frame_button)

		self.__tools_buttons_frame.setFixedSize(self.__tools_buttons_frame_layout.minimumSize())

		###

		self.__text_search_frame = TextSearchFrame.TextSearchFrame(self)
		self.__text_search_frame.hide()
		self.__main_layout.addWidget(self.__text_search_frame)

		#####

		self.connect(self.__text_search_frame, Qt.SIGNAL("findNextRequest(const QString &)"), self.__text_browser.findNext)
		self.connect(self.__text_search_frame, Qt.SIGNAL("findPreviousRequest(const QString &)"), self.__text_browser.findPrevious)
		self.connect(self.__text_search_frame, Qt.SIGNAL("instantSearchRequest(const QString &)"), self.__text_browser.instantSearch)

		self.connect(self.__text_browser, Qt.SIGNAL("backwardRequest()"), self.__backward_button.animateClick)

		self.connect(self.__backward_button, Qt.SIGNAL("clicked()"), self.__text_browser.backward)
		self.connect(self.__forward_button, Qt.SIGNAL("clicked()"), self.__text_browser.forward)
		self.connect(self.__home_button, Qt.SIGNAL("clicked()"), self.home)

		self.connect(self.__show_text_search_frame_button, Qt.SIGNAL("clicked()"), self.__text_search_frame.show)

		self.connect(self.__text_browser, Qt.SIGNAL("showTextSearchFrameRequest()"), self.__text_search_frame.show)
		self.connect(self.__text_browser, Qt.SIGNAL("hideTextSearchFrameRequest()"), self.__text_search_frame.hide)
		self.connect(self.__text_browser, Qt.SIGNAL("setFoundRequest(bool)"), self.__text_search_frame.setFound)
		self.connect(self.__text_browser, Qt.SIGNAL("sourceChanged(const QUrl &)"), self.updateTitle)
		self.connect(self.__text_browser, Qt.SIGNAL("backwardAvailable(bool)"), self.__backward_button.setEnabled)
		self.connect(self.__text_browser, Qt.SIGNAL("forwardAvailable(bool)"), self.__forward_button.setEnabled)

		#####

		Qt.QDesktopServices.setUrlHandler("xslhelp", self.showInternalHelp)

		self.translateUi()


	### Public ###

	def saveSettings(self) :
		self.__settings.setValue(Qt.QString("%1/size").arg(self.objectName()), Qt.QVariant(self.size()))
		self.__settings.setValue(Qt.QString("%1/url").arg(self.objectName()), Qt.QVariant(self.__text_browser.source()))

	def loadSettings(self) :
		self.resize(self.__settings.value(Qt.QString("%1/size").arg(self.objectName()), Qt.QVariant(Qt.QSize(800, 600))).toSize())
		self.__text_browser.setSource(self.__settings.value(Qt.QString("%1/url").arg(self.objectName()),
			Qt.QVariant(self.__index_file_url)).toUrl())

	###

	@Qt.pyqtSignature("QUrl")
	def showInternalHelp(self, url) :
		relative_file_path = url.toString().remove("xslhelp://")
		absolute_file_path = Utils.joinPath(HtmlDocsDirPath, self.__locale.htmlDocsLang(), relative_file_path)
		self.__text_browser.setSource(Qt.QUrl(absolute_file_path))
		self.show()


	### Private ###

	def translateUi(self) :
		self.__index_file_url = Qt.QUrl(Utils.joinPath(Const.HtmlDocsDirPath, self.__locale.htmlDocsLang(), "index.html"))

		self.__backward_button.setToolTip(tr("Backspace"))
		self.__show_text_search_frame_button.setToolTip(tr("Ctrl+F, /"))

		self.updateTitle()

	###

	def home(self) :
		self.__text_browser.setSource(self.__index_file_url)

	###

	def updateTitle(self) :
		self.setWindowTitle(tr("%1 Manual - %2").arg(Const.Package).arg(self.__text_browser.documentTitle()))


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
		self.__text_browser.setFocus(Qt.Qt.OtherFocusReason)


	def keyPressEvent(self, event) :
		if event.key() != Qt.Qt.Key_Escape :
			Qt.QDialog.keyPressEvent(self, event)


##### Public classes #####
class HelpBrowserWindow(HelpBrowserWindowMultiple) :
	__help_browser_window_multiple_object = None

	def __new__(self, parent = None) :
		if self.__help_browser_window_multiple_object == None :
			self.__help_browser_window_multiple_object = HelpBrowserWindowMultiple.__new__(self, parent)
			HelpBrowserWindowMultiple.__init__(self.__help_browser_window_multiple_object, parent)
		return self.__help_browser_window_multiple_object

	def __init__(self, parent = None) :
		pass

