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


import sys

import Qt
import Const
import Settings
import IconsLoader
import EntitledMenu
import SlSearchPanel
import GoogleTranslatePanel
import HistoryPanel
import TabbedTranslateBrowser
import TranslateWindow
import StatusBar
import DictsManagerWindow
import SettingsWindow
import Spy
import RadioButtonsMenu
import InternetLinksMenu
import HelpBrowserWindow
import AboutWindow
import Logger

try :
	import KeysGrabber
except :
	Logger.warning("Ignored X11 hooks: KeysGrabber")
	Logger.attachException(Logger.WarningMessage)


##### Public classes #####
class MainWindow(Qt.QMainWindow) :
	def __init__(self, parent = None) :
		Qt.QMainWindow.__init__(self, parent)

		self.setObjectName("main_window")

		self.setDockOptions(self.dockOptions()|Qt.QMainWindow.VerticalTabs)

		self.setWindowTitle(Const.Package+" "+Const.MyName)
		self.setWindowIcon(IconsLoader.icon("xsl"))

		#####

		self.__main_widget = Qt.QWidget(self)
		self.setCentralWidget(self.__main_widget)

		self.__main_layout = Qt.QVBoxLayout()
		self.__main_layout.setContentsMargins(0, 0, 0, 0)
		self.__main_widget.setLayout(self.__main_layout)

		#####

		self.__source_objects_list = []
		self.__panels_list = []
		self.__spy_methods_dict = {}

		###

		self.__settings = Settings.Settings(self)

		self.__status_bar = StatusBar.StatusBar(self)
		self.setStatusBar(self.__status_bar)

		self.__tabbed_translate_browser = TabbedTranslateBrowser.TabbedTranslateBrowser(self)
		self.__main_layout.addWidget(self.__tabbed_translate_browser)

		self.__translate_window = TranslateWindow.TranslateWindow(self)
		self.__translate_window.setObjectName("translate_window")

		self.__dicts_manager_window = DictsManagerWindow.DictsManagerWindow(self)
		self.__dicts_manager_window.setObjectName("dicts_manager_window")

		self.__settings_window = SettingsWindow.SettingsWindow(self)
		self.__settings_window.setObjectName("settings_window")

		self.__help_browser_window = HelpBrowserWindow.HelpBrowserWindow(self)
		self.__help_browser_window.setObjectName("help_browser_window")

		self.__about_window = AboutWindow.AboutWindow(self)

		self.__spy = Spy.Spy(self)

		self.__tray_icon = Qt.QSystemTrayIcon(self)
		self.__tray_icon.setIcon(IconsLoader.icon("xsl_22"))

		if sys.modules.has_key("KeysGrabber") :
			self.__keys_grabber = KeysGrabber.KeysGrabber()
			self.__main_window_hotkey = self.__keys_grabber.addHotkey(KeysGrabber.Key_L, KeysGrabber.WinModifier)

		#####

		self.__pages_menu = self.menuBar().addMenu(tr("&Pages"))
		self.__save_action = self.__pages_menu.addAction(IconsLoader.icon("document-save-as"),
			tr("Save current page"), self.saveCurrentPage)
		self.__print_action = self.__pages_menu.addAction(IconsLoader.icon("document-print"),
			tr("Print current page"), self.printCurrentPage)
		self.__pages_menu.addSeparator()
		self.__clear_action = self.__pages_menu.addAction(IconsLoader.icon("edit-clear"),
			tr("Clear current page"), self.clearCurrentPage, Qt.QKeySequence("Ctrl+E"))
		self.__clear_all_action = self.__pages_menu.addAction(IconsLoader.icon("edit-clear"),
			tr("Clear all"), self.clearAllPages, Qt.QKeySequence("Ctrl+K"))
		self.__pages_menu.addSeparator()
		self.__find_action = self.__pages_menu.addAction(IconsLoader.icon("edit-find"),
			tr("Search in translations"), self.__tabbed_translate_browser.showTextSearchFrame, Qt.QKeySequence("Ctrl+F"))
		self.__pages_menu.addSeparator()
		self.__new_tab_action = self.__pages_menu.addAction(IconsLoader.icon("tab-new"),
			tr("New tab"), self.addTab, Qt.QKeySequence("Ctrl+T"))
		self.__close_tab_action = self.__pages_menu.addAction(IconsLoader.icon("tab-close"),
			tr("Close tab"), self.removeTab, Qt.QKeySequence("Ctrl+W"))
		self.__pages_menu.addSeparator()
		self.__exit_action = self.__pages_menu.addAction(IconsLoader.icon("application-exit"),
			tr("Quit"), self.exit, Qt.QKeySequence("Ctrl+Q"))

		###

		self.__panels_menu = self.menuBar().addMenu(tr("Pane&ls"))

		###

		self.__spy_menu = self.menuBar().addMenu(tr("Sp&y"))
		self.__start_spy_action = self.__spy_menu.addAction(IconsLoader.icon("media-playback-start"),
			tr("Start Spy"), self.startSpy)
		self.__stop_spy_action = self.__spy_menu.addAction(IconsLoader.icon("media-playback-stop"),
			tr("Stop Spy"), self.stopSpy)
		self.__spy_menu.addSeparator()
		self.__spy_methods_menu = RadioButtonsMenu.RadioButtonsMenu(tr("Translate methods"), self.__spy_menu)
		self.__spy_methods_action = self.__spy_menu.addMenu(self.__spy_methods_menu)
		self.__stop_spy_action.setEnabled(False)

		###

		self.__view_menu = self.menuBar().addMenu(tr("&View"))
		self.__zoom_in_action = self.__view_menu.addAction(IconsLoader.icon("zoom-in"),
			tr("Zoom in"), self.__tabbed_translate_browser.zoomIn, Qt.QKeySequence("Ctrl++"))
		self.__zoom_out_action = self.__view_menu.addAction(IconsLoader.icon("zoom-out"),
			tr("Zoom out"), self.__tabbed_translate_browser.zoomOut, Qt.QKeySequence("Ctrl+-"))
		self.__zoom_normal_action = self.__view_menu.addAction(IconsLoader.icon("zoom-original"),
			tr("Zoom normal"), self.__tabbed_translate_browser.zoomNormal, Qt.QKeySequence("Ctrl+0"))

		###

		self.__tools_menu = self.menuBar().addMenu(tr("&Tools"))
		self.__dicts_manager_action = self.__tools_menu.addAction(IconsLoader.icon("configure"),
			tr("Dicts management"), self.__dicts_manager_window.show, Qt.QKeySequence("Ctrl+D"))
		self.__settings_action = self.__tools_menu.addAction(IconsLoader.icon("configure"),
			tr("Settings"), self.__settings_window.show)

		###

		self.__help_menu = self.menuBar().addMenu(tr("&Help"))
		self.__help_action = self.__help_menu.addAction(IconsLoader.icon("help-contents"),
			tr("%1 manual").arg(Const.Package), self.__help_browser_window.show, Qt.QKeySequence("F1"))
		self.__help_menu.addSeparator()
		internet_links_menu = InternetLinksMenu.InternetLinksMenu(tr("Internet links"), self.__help_menu)
		internet_links_menu.setIcon(IconsLoader.icon("applications-internet"))
		self.__links_action = self.__help_menu.addMenu(internet_links_menu)
		self.__help_menu.addSeparator()
		self.__about_action = self.__help_menu.addAction(IconsLoader.icon("xsl"),
			tr("About %1").arg(Const.MyName), self.__about_window.show)
		self.__about_qt_action = self.__help_menu.addAction(IconsLoader.icon("help-about"),
			tr("About Qt4"), lambda : Qt.QMessageBox.aboutQt(None))

		#####

		self.__sl_search_panel = SlSearchPanel.SlSearchPanel(self)
		self.__sl_search_panel.setObjectName("sl_search_panel")
		self.addPanel(self.__sl_search_panel)
		self.addSourceObject(self.__sl_search_panel)

		self.__history_panel = HistoryPanel.HistoryPanel(self)
		self.__history_panel.setObjectName("history_panel")
		self.addPanel(self.__history_panel)

		self.__google_translate_panel = GoogleTranslatePanel.GoogleTranslatePanel(self)
		self.__google_translate_panel.setObjectName("google_translate_panel")
		self.addPanel(self.__google_translate_panel)
		self.addSourceObject(self.__google_translate_panel)

		#####

		self.connect(self.__settings, Qt.SIGNAL("settingsChanged(const QString &)"), self.applySettingsTrayIcon)

		self.connect(self.__sl_search_panel, Qt.SIGNAL("wordChanged(const QString &)"), self.__history_panel.addWord)

		self.connect(self.__history_panel, Qt.SIGNAL("wordChanged(const QString &)"), self.__sl_search_panel.setWord)
		self.connect(self.__history_panel, Qt.SIGNAL("wordChanged(const QString &)"), self.__sl_search_panel.show)
		self.connect(self.__history_panel, Qt.SIGNAL("statusChanged(const QString &)"), self.__status_bar.showStatusMessage)

		self.connect(self.__tabbed_translate_browser, Qt.SIGNAL("uFindRequest(const QString &)"), self.__sl_search_panel.setWord)
		self.connect(self.__tabbed_translate_browser, Qt.SIGNAL("uFindRequest(const QString &)"), self.__sl_search_panel.uFind)
		self.connect(self.__tabbed_translate_browser, Qt.SIGNAL("uFindRequest(const QString &)"), self.__sl_search_panel.show)
		self.connect(self.__tabbed_translate_browser, Qt.SIGNAL("cFindRequest(const QString &)"), self.__sl_search_panel.setWord)
		self.connect(self.__tabbed_translate_browser, Qt.SIGNAL("cFindRequest(const QString &)"), self.__sl_search_panel.cFind)
		self.connect(self.__tabbed_translate_browser, Qt.SIGNAL("cFindRequest(const QString &)"), self.__sl_search_panel.show)
		self.connect(self.__tabbed_translate_browser, Qt.SIGNAL("statusChanged(const QString &)"), self.__status_bar.showStatusMessage)

		self.connect(self.__translate_window, Qt.SIGNAL("newTabRequest()"), self.addTab)
		self.connect(self.__translate_window, Qt.SIGNAL("uFindRequest(const QString &)"), self.__sl_search_panel.setWord)
		self.connect(self.__translate_window, Qt.SIGNAL("uFindRequest(const QString &)"), self.__sl_search_panel.uFind)
		self.connect(self.__translate_window, Qt.SIGNAL("uFindRequest(const QString &)"), self.__sl_search_panel.show)
		self.connect(self.__translate_window, Qt.SIGNAL("uFindRequest(const QString &)"), self.showUp)
		self.connect(self.__translate_window, Qt.SIGNAL("cFindRequest(const QString &)"), self.__sl_search_panel.setWord)
		self.connect(self.__translate_window, Qt.SIGNAL("cFindRequest(const QString &)"), self.__sl_search_panel.cFind)
		self.connect(self.__translate_window, Qt.SIGNAL("cFindRequest(const QString &)"), self.__sl_search_panel.show)
		self.connect(self.__translate_window, Qt.SIGNAL("cFindRequest(const QString &)"), self.showUp)

		self.connect(self.__dicts_manager_window, Qt.SIGNAL("dictsListChanged(const QStringList &)"), self.__sl_search_panel.setDictsList)
		self.connect(self.__dicts_manager_window, Qt.SIGNAL("dictsListChanged(const QStringList &)"), lambda : self.__sl_search_panel.lFind())

		self.connect(self.__spy, Qt.SIGNAL("selectionChanged(const QString &)"), self.spySelectionChanged)
		self.connect(self.__spy, Qt.SIGNAL("showTranslateWindowRequest()"), self.__translate_window.show)
		self.connect(self.__spy, Qt.SIGNAL("showTranslateWindowRequest()"), self.__translate_window.setFocus)

		self.connect(self.__tray_icon, Qt.SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.controlAct)

		if sys.modules.has_key("KeysGrabber") :
			self.connect(self.__keys_grabber, Qt.SIGNAL("keyPressed(const QString &)"), self.controlAct)


	### Public ###

	def save(self) :
		for panels_list_item in self.__panels_list :
			panels_list_item["panel"].saveSettings()

		self.__translate_window.saveSettings()
		self.__dicts_manager_window.saveSettings()
		self.__settings_window.saveSettings()
		self.__help_browser_window.saveSettings()

		self.saveSettings()

	def load(self) :
		for panels_list_item in self.__panels_list :
			panels_list_item["panel"].loadSettings()

		self.__translate_window.loadSettings()
		self.__dicts_manager_window.loadSettings()
		self.__settings_window.loadSettings()
		self.__help_browser_window.loadSettings()

		self.loadSettings()

		self.__sl_search_panel.setFocus()
		self.__sl_search_panel.raise_()

		self.__tray_icon.setVisible(self.__settings.value("application/misc/show_tray_icon_flag", Qt.QVariant(True)).toBool())

		self.translateUi()

		self.__tabbed_translate_browser.setCaption(0, tr("Welcome"))
		self.__tabbed_translate_browser.setText(0, tr("<br><br><hr><table border=\"0\" width=\"100%\"><tr>"
			"<td class=\"dict_header_background\" align=\"center\"><font class=\"dict_header_font\">"
			"Welcome to the %1 - the system of electronic dictionaries</font></td></tr></table><hr>").arg(Const.Package))

		self.__status_bar.showStatusMessage(tr("Ready"))

	###

	def visibleChange(self) :
		if not self.isVisible() or self.isMinimized() or not self.isActiveWindow() :
			self.close() # FIXME (Issue 58): Normal window move to top
			self.showNormal()
			self.activateFocus()
		else :
			self.close()

	def showUp(self) :
		if self.isVisible() :
			self.visibleChange()
		self.visibleChange()

	###

	def focusChanged(self) :
		new_flags_list = [ item["panel"].hasInternalFocus() for item in self.__panels_list ]
		if True in new_flags_list :
			for count in xrange(len(new_flags_list)) :
				self.__panels_list[count]["focus_flag"] = new_flags_list[count]

	def activateFocus(self) :
		for panels_list_item in self.__panels_list :
			if panels_list_item["focus_flag"] :
				panels_list_item["panel"].setFocus()

	###

	def exit(self) :
		self.save()
		Qt.QApplication.exit(0)


	### Private ###

	def translateUi(self) :
		self.__pages_menu.setTitle(tr("&Pages"))
		self.__save_action.setText(tr("Save current page"))
		self.__print_action.setText(tr("Print current page"))
		self.__clear_action.setText(tr("Clear current page"))
		self.__clear_all_action.setText(tr("Clear all"))
		self.__find_action.setText(tr("Search in translations"))
		self.__new_tab_action.setText(tr("New tab"))
		self.__close_tab_action.setText(tr("Close tab"))
		self.__exit_action.setText(tr("Quit"))

		self.__panels_menu.setTitle(tr("Pane&ls"))
		for panels_list_item in self.__panels_list :
			panels_list_item["action"].setText(tr(panels_list_item["title"]))

		self.__spy_menu.setTitle(tr("Sp&y"))
		self.__start_spy_action.setText(tr("Start Spy"))
		self.__stop_spy_action.setText(tr("Stop Spy"))
		self.__spy_methods_action.setText(tr("Translate methods"))
		for spy_methods_dict_key in self.__spy_methods_dict :
			spy_methods_dict_key.setText(tr(self.__spy_methods_dict[spy_methods_dict_key]["title"]))

		self.__view_menu.setTitle(tr("&View"))
		self.__zoom_in_action.setText(tr("Zoom in"))
		self.__zoom_out_action.setText(tr("Zoom out"))
		self.__zoom_normal_action.setText(tr("Zoom normal"))

		self.__tools_menu.setTitle(tr("&Tools"))
		self.__dicts_manager_action.setText(tr("Dicts management"))
		self.__settings_action.setText(tr("Settings"))

		self.__help_menu.setTitle(tr("&Help"))
		self.__help_action.setText(tr("%1 manual").arg(Const.Package))
		self.__links_action.setText(tr("Internet links"))
		self.__about_action.setText(tr("About %1").arg(Const.MyName))
		self.__about_qt_action.setText(tr("About Qt4"))

		if self.__spy.isRunning() :
			self.__tray_icon.setToolTip(tr("%1 - graphical interface for SL\nSpy is stopped").arg(Const.MyName))
		else :
			self.__tray_icon.setToolTip(tr("%1 - graphical interface for SL\nSpy is running").arg(Const.MyName))

	###

	def addPanel(self, panel) :
		requisites = dict(panel.requisites())
		self.__panels_list.append({ "panel" : panel, "title" : requisites["title"], "focus_flag" : False,
			"action" : self.__panels_menu.addAction(requisites["icon"], tr(requisites["title"]), panel.show, requisites["hotkey"]) })

		self.addDockWidget(requisites["area"], panel)
		if len(self.__panels_list) > 1 :
			self.tabifyDockWidget(self.__panels_list[-2]["panel"], self.__panels_list[-1]["panel"])

	def addSourceObject(self, source_object) :
		self.__source_objects_list.append({ "object" : source_object, "index" : -1, "spy_method_actions" : {} })

		index = len(self.__source_objects_list) - 1

		self.connect(source_object, Qt.SIGNAL("processStarted()"), ( lambda n = index : self.registrateStream(n) ))
		self.connect(source_object, Qt.SIGNAL("processStarted()"), self.__status_bar.startWaitMovie)
		self.connect(source_object, Qt.SIGNAL("processFinished()"), ( lambda n = index : self.releaseStream(n) ))
		self.connect(source_object, Qt.SIGNAL("processFinished()"), self.__status_bar.stopWaitMovie)
		self.connect(source_object, Qt.SIGNAL("clearRequest()"), ( lambda n = index : self.clearTab(n) ))
		self.connect(source_object, Qt.SIGNAL("wordChanged(const QString &)"), ( lambda word, n = index : self.setTabCaption(n, word) ))
		self.connect(source_object, Qt.SIGNAL("wordChanged(const QString &)"), self.__translate_window.setCaption)
		self.connect(source_object, Qt.SIGNAL("textChanged(const QString &)"), ( lambda text, n = index : self.setTabText(n, text) ))
		self.connect(source_object, Qt.SIGNAL("textChanged(const QString &)"), self.__translate_window.setText)
		self.connect(source_object, Qt.SIGNAL("newTabRequest()"), self.addTab)
		self.connect(source_object, Qt.SIGNAL("statusChanged(const QString &)"), self.__status_bar.showStatusMessage)

		for translate_methods_list_item in source_object.translateMethods() :
			action = self.__spy_methods_menu.addRadioButton(translate_methods_list_item["title"],
				translate_methods_list_item["object_name"]+"__"+translate_methods_list_item["method_name"])
			self.__spy_methods_dict[action] = dict(translate_methods_list_item)
			self.__spy_methods_dict[action]["source_object"] = source_object

	###

	def registrateStream(self, source_object_index) :
		self.__tabbed_translate_browser.setShredLock(True)
		tabbed_translate_browser_index = self.__tabbed_translate_browser.currentIndex()

		for source_objects_list_item in self.__source_objects_list :
			if source_objects_list_item["index"] == tabbed_translate_browser_index :
				self.__tabbed_translate_browser.addTab()
				tabbed_translate_browser_index = self.__tabbed_translate_browser.currentIndex()
				break

		self.__source_objects_list[source_object_index]["index"] = tabbed_translate_browser_index

	def releaseStream(self, source_object_index) :
		self.__tabbed_translate_browser.setShredLock(False)
		self.__source_objects_list[source_object_index]["index"] = -1

	def checkBusyStreams(self) :
		for source_objects_list_item in self.__source_objects_list :
			if source_objects_list_item["index"] != -1 :
				return True
		return False

	###

	def clearTab(self, source_object_index) :
		self.__tabbed_translate_browser.clear(self.__source_objects_list[source_object_index]["index"])

	def setTabCaption(self, source_object_index, word) :
		self.__tabbed_translate_browser.setCaption(self.__source_objects_list[source_object_index]["index"], word)

	def setTabText(self, source_object_index, text) :
		self.__tabbed_translate_browser.setText(self.__source_objects_list[source_object_index]["index"], text)

	def addTab(self) :
		self.__tabbed_translate_browser.addTab()

	def removeTab(self) :
		if self.checkBusyStreams() :
			return
		self.__tabbed_translate_browser.removeTab()

	###

	def saveCurrentPage(self) :
		if self.checkBusyStreams() :
			return

		index = self.__tabbed_translate_browser.currentIndex()
		file_path = Qt.QFileDialog.getSaveFileName(self,
			tr("Save page \"%1\"").arg(self.__tabbed_translate_browser.caption(index)),
			Qt.QDir.homePath(), "*.html *.htm")
		if file_path.simplified().isEmpty() :
			return

		page_file = Qt.QFile(file_path)
		if not page_file.open(Qt.QIODevice.WriteOnly|Qt.QIODevice.Text) :
			Qt.QMessageBox.warning(self, Const.MyName, tr("This file cannot by open for saving"))
			return

		file_stream = Qt.QTextStream(page_file)
		file_stream << self.__tabbed_translate_browser.document(index).toHtml("utf-8")

		page_file.close()

		self.__status_bar.showStatusMessage(tr("Saved"))

	def printCurrentPage(self) :
		if self.checkBusyStreams() :
			return

		printer = Qt.QPrinter()
		print_dialog = Qt.QPrintDialog(printer)
		print_dialog.setWindowTitle(tr("Print page"))

		if print_dialog.exec_() != Qt.QDialog.Accepted :
			return

		index = self.__tabbed_translate_browser.currentIndex()
		text_document = self.__tabbed_translate_browser.document(index)
		text_document.print_(printer)

		self.__status_bar.showStatusMessage(tr("Printing..."))

	def clearAllPages(self) :
		if self.checkBusyStreams() :
			return

		for panels_list_item in self.__panels_list :
			panels_list_item["panel"].clear()

		self.__tabbed_translate_browser.clearAll()

		self.activateFocus()

	def clearCurrentPage(self) :
		if self.checkBusyStreams() :
			return
		self.__tabbed_translate_browser.clearPage()

		self.activateFocus()

	###

	def startSpy(self) :
		self.__spy.start()
		self.__start_spy_action.setEnabled(False)
		self.__stop_spy_action.setEnabled(True)
		self.__tray_icon.setIcon(IconsLoader.icon("xsl+spy_22"))
		self.__tray_icon.setToolTip(tr("%1 - graphical interface for SL\nSpy is running").arg(Const.MyName))
		self.__status_bar.showMessage(tr("Spy is running"))

	def stopSpy(self) :
		self.__spy.stop()
		self.__start_spy_action.setEnabled(True)
		self.__stop_spy_action.setEnabled(False)
		self.__tray_icon.setIcon(IconsLoader.icon("xsl_22"))
		self.__tray_icon.setToolTip(tr("%1 - graphical interface for SL\nSpy is stopped").arg(Const.MyName))
		self.__status_bar.showMessage(tr("Spy is stopped"))

	def spySelectionChanged(self, text) :
		action = self.__spy_methods_menu.currentAction()
		self.__spy_methods_dict[action]["method"](text)
		self.__spy_methods_dict[action]["source_object"].show()

	###

	def applySettingsTrayIcon(self, key) :
		if key == "application/misc/show_tray_icon_flag" :
			self.__tray_icon.setVisible(self.__settings.value("application/misc/show_tray_icon_flag").toBool())

	###

	def controlAct(self, reason) :
		if sys.modules.has_key("KeysGrabber") and reason == self.__main_window_hotkey :
			self.visibleChange()
		elif reason == Qt.QSystemTrayIcon.Trigger :
			self.visibleChange()
		elif reason == Qt.QSystemTrayIcon.Context :
			menu = EntitledMenu.EntitledMenu(IconsLoader.icon("xsl"), Const.Package+" "+Const.MyName)
			menu.addAction(self.__start_spy_action)
			menu.addAction(self.__stop_spy_action)
			menu.addSeparator()
			menu.addAction(tr("Dictionary window")+( "\tWin+L" if sys.modules.has_key("KeysGrabber") else "" ), self.visibleChange)
			menu.addSeparator()
			menu.addAction(self.__exit_action)
			menu.exec_(Qt.QCursor.pos())

	###

	def saveSettings(self) :
		self.__settings.setValue(Qt.QString("%1/size").arg(self.objectName()), Qt.QVariant(self.size()))
		self.__settings.setValue(Qt.QString("%1/position").arg(self.objectName()), Qt.QVariant(self.pos()))
		self.__settings.setValue(Qt.QString("%1/is_visible_flag").arg(self.objectName()), Qt.QVariant(self.isVisible()))
		self.__settings.setValue(Qt.QString("%1/state").arg(self.objectName()), Qt.QVariant(self.saveState()))

		self.__settings.setValue(Qt.QString("%1/spy_method_index").arg(self.objectName()), Qt.QVariant(self.__spy_methods_menu.currentIndex()))
		self.__settings.setValue(Qt.QString("%1/spy_status").arg(self.objectName()), Qt.QVariant(self.__spy.isRunning()))

	def loadSettings(self) :
		self.resize(self.__settings.value(Qt.QString("%1/size").arg(self.objectName()), Qt.QVariant(Qt.QSize(800, 500))).toSize())
		self.move(self.__settings.value(Qt.QString("%1/position").arg(self.objectName())).toPoint())
		self.setVisible(self.__settings.value(Qt.QString("%1/is_visible_flag").arg(self.objectName()), Qt.QVariant(True)).toBool())
		self.restoreState(self.__settings.value(Qt.QString("%1/state").arg(self.objectName())).toByteArray())

		spy_method_index = self.__settings.value(Qt.QString("%1/spy_method_index").arg(self.objectName()), Qt.QVariant(-1)).toInt()[0]
		if spy_method_index > 0 :
			self.__spy_methods_menu.setCurrentIndex(spy_method_index)
		elif self.__spy_methods_menu.count() > 0 :
			self.__spy_methods_menu.setCurrentIndex(0)
		if self.__settings.value(Qt.QString("%1/spy_status").arg(self.objectName())).toBool() :
			self.startSpy()

	### Handlers ###

	def changeEvent(self, event) :
		if event.type() == Qt.QEvent.LanguageChange :
			self.translateUi()
		else :
			Qt.QMainWindow.changeEvent(self, event)

	def closeEvent(self, event) :
		if not self.__settings.value("application/misc/show_tray_icon_flag", Qt.QVariant(True)).toBool() :
			self.exit()
		else :
			Qt.QMainWindow.closeEvent(self, event)

