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
import Settings
import IconsLoader
import LineEdit
import DictsListWidget


##### Public classes #####
class DictsManagerWindow(Qt.QDialog) :
	def __init__(self, parent = None) :
		Qt.QDialog.__init__(self, parent)

		self.setWindowIcon(IconsLoader.icon("xsl"))

		#####

		left_margin = self.style().pixelMetric(Qt.QStyle.PM_LayoutLeftMargin)
		top_margin = self.style().pixelMetric(Qt.QStyle.PM_LayoutTopMargin)
		right_margin = self.style().pixelMetric(Qt.QStyle.PM_LayoutRightMargin)
		bottom_margin = self.style().pixelMetric(Qt.QStyle.PM_LayoutBottomMargin)
		vertical_spacing = self.style().pixelMetric(Qt.QStyle.PM_LayoutVerticalSpacing)

		self.__main_layout = Qt.QVBoxLayout()
		self.__main_layout.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self.__main_layout)

		self.__line_edit_layout = Qt.QHBoxLayout()
		self.__line_edit_layout.setContentsMargins(left_margin, top_margin, right_margin, vertical_spacing)
		self.__main_layout.addLayout(self.__line_edit_layout)

		self.__dicts_browser_stacked_layout = Qt.QStackedLayout()
		self.__main_layout.addLayout(self.__dicts_browser_stacked_layout)

		self.__control_buttons_layout = Qt.QHBoxLayout()
		self.__control_buttons_layout.setContentsMargins(left_margin, vertical_spacing, right_margin, bottom_margin)
		self.__main_layout.addLayout(self.__control_buttons_layout)

		self.__message_labels_stacked_widget = Qt.QStackedWidget()
		self.__control_buttons_layout.addWidget(self.__message_labels_stacked_widget)

		#####

		self.__settings = Settings.Settings(self)

		self.__all_dicts_dir_watcher = Qt.QFileSystemWatcher(Qt.QStringList() << Const.AllDictsDirPath, self)
		self.__all_dicts_dir_watcher_timer = Qt.QTimer(self)
		self.__all_dicts_dir_watcher_timer.setInterval(5000)
		self.__all_dicts_dir_watcher_timer.setSingleShot(True)

		#####

		self.__filter_label = Qt.QLabel(self)
		self.__line_edit_layout.addWidget(self.__filter_label)

		self.__line_edit = LineEdit.LineEdit(self)
		self.__filter_label.setBuddy(self.__line_edit)
		self.__line_edit_layout.addWidget(self.__line_edit)

		self.__dicts_browser = DictsListWidget.DictsListWidget(self)
		self.__dicts_browser_stacked_layout.addWidget(self.__dicts_browser)

		self.__wait_picture_movie = IconsLoader.gifMovie("circular")
		self.__wait_picture_movie.setScaledSize(Qt.QSize(32, 32))
		self.__wait_picture_movie.jumpToFrame(0)
		self.__wait_picture_movie_label = Qt.QLabel(self)
		self.__wait_picture_movie_label.setAlignment(Qt.Qt.AlignHCenter|Qt.Qt.AlignVCenter)
		self.__wait_picture_movie_label.setMovie(self.__wait_picture_movie)
		self.__dicts_browser_stacked_layout.addWidget(self.__wait_picture_movie_label)

		self.__install_dicts_label = Qt.QLabel(self)
		self.__install_dicts_label.setOpenExternalLinks(True)
		self.__install_dicts_label.setTextFormat(Qt.Qt.RichText)
		self.__message_labels_stacked_widget.addWidget(self.__install_dicts_label)

		self.__wait_message_label = Qt.QLabel(self)
		self.__message_labels_stacked_widget.addWidget(self.__wait_message_label)

		self.__control_buttons_layout.addStretch()

		self.__update_dicts_button = Qt.QPushButton(self)
		self.__update_dicts_button.setIcon(IconsLoader.icon("view-refresh"))
		self.__update_dicts_button.setAutoDefault(False)
		self.__update_dicts_button.setDefault(False)
		self.__control_buttons_layout.addWidget(self.__update_dicts_button)

		self.__ok_button = Qt.QPushButton(self)
		self.__ok_button.setIcon(IconsLoader.icon("dialog-ok-apply"))
		self.__ok_button.setAutoDefault(False)
		self.__ok_button.setDefault(False)
		self.__control_buttons_layout.addWidget(self.__ok_button)

		self.__message_labels_stacked_widget.setMaximumHeight(self.__control_buttons_layout.minimumSize().height())

		#####

		self.connect(self.__all_dicts_dir_watcher, Qt.SIGNAL("directoryChanged(const QString &)"), self.planToUpdateDicts)
		self.connect(self.__all_dicts_dir_watcher_timer, Qt.SIGNAL("timeout()"), self.updateDicts)

		self.connect(self.__line_edit, Qt.SIGNAL("textChanged(const QString &)"), self.__dicts_browser.setFilter)

		self.connect(self.__dicts_browser, Qt.SIGNAL("dictsListChanged(const QStringList &)"), self.dictsListChangedSignal)

		self.connect(self.__update_dicts_button, Qt.SIGNAL("clicked()"), self.updateDicts)
		self.connect(self.__ok_button, Qt.SIGNAL("clicked()"), self.accept)

		#####

		self.__dicts_browser_stacked_layout.setCurrentIndex(0)
		self.__message_labels_stacked_widget.setCurrentIndex(0)

		self.translateUi()


	### Public ###

	def updateDicts(self) :
		self.__all_dicts_dir_watcher.blockSignals(True)
		self.__all_dicts_dir_watcher_timer.stop()
		self.__update_dicts_button.blockSignals(True)
		self.__update_dicts_button.setEnabled(False)

		self.__line_edit.clear()
		self.__line_edit.setEnabled(False)

		self.__message_labels_stacked_widget.setCurrentIndex(1)
		self.__dicts_browser_stacked_layout.setCurrentIndex(1)
		self.__wait_picture_movie.start()

		###

		self.__dicts_browser.setItemsList(self.allAndLocalDicts(self.__dicts_browser.itemsList()))

		###

		self.__message_labels_stacked_widget.setCurrentIndex(0)
		self.__dicts_browser_stacked_layout.setCurrentIndex(0)
		self.__wait_picture_movie.stop()
		self.__wait_picture_movie.jumpToFrame(0)

		self.__line_edit.setEnabled(True)

		self.__update_dicts_button.setEnabled(True)
		self.__update_dicts_button.blockSignals(False)
		self.__all_dicts_dir_watcher.blockSignals(False)

		#####

		self.__dicts_browser.setFocus(Qt.Qt.OtherFocusReason)

	###

	def saveSettings(self) :
		self.__settings.setValue(Qt.QString("%1/size").arg(self.objectName()), Qt.QVariant(self.size()))
		self.__settings.setValue(Qt.QString("%1/items_list").arg(self.objectName()), Qt.QVariant(self.__dicts_browser.itemsList()))

	def loadSettings(self) :
		self.__all_dicts_dir_watcher.blockSignals(True)
		self.__all_dicts_dir_watcher_timer.stop()
		self.__update_dicts_button.blockSignals(True)
		self.__update_dicts_button.setEnabled(False)

		###

		self.resize(self.__settings.value(Qt.QString("%1/size").arg(self.objectName()), Qt.QVariant(Qt.QSize(400, 550))).toSize())

		local_items_list = self.__settings.value(Qt.QString("%1/items_list").arg(self.objectName())).toStringList()
		self.__dicts_browser.setItemsList(self.allAndLocalDicts(local_items_list))

		###

		self.__update_dicts_button.setEnabled(True)
		self.__update_dicts_button.blockSignals(False)
		self.__all_dicts_dir_watcher.blockSignals(False)


	### Private ###

	def translateUi(self) :
		self.setWindowTitle(tr("Dicts Manager"))

		self.__filter_label.setText(tr("&Filter:"))
		self.__install_dicts_label.setText(tr("<a href=\"xslhelp://llrepo_usage.html\">How to install a new dictionary?</a>"))
		self.__wait_message_label.setText(tr("Please wait..."))

		self.__update_dicts_button.setText(tr("&Update"))
		self.__ok_button.setText(tr("&OK"))

	###

	def planToUpdateDicts(self) :
		if self.__all_dicts_dir_watcher_timer.isActive() :
			self.__all_dicts_dir_watcher_timer.stop()
		self.__all_dicts_dir_watcher_timer.start()

	###

	def allAndLocalDicts(self, local_items_list) :
		local_items_list = Qt.QStringList(local_items_list)

		all_dicts_file_name_filters = Qt.QStringList()
		all_dicts_file_name_filters << "*.??-??"

		all_dicts_dir = Qt.QDir(Const.AllDictsDirPath)
		all_dicts_dir.setNameFilters(all_dicts_file_name_filters)
		all_dicts_dir.setFilter(Qt.QDir.Files)
		all_dicts_dir.setSorting(Qt.QDir.Name)
		all_dicts_dir_entry_list = all_dicts_dir.entryList()

		###

		item_code_regexp = Qt.QRegExp("\\{(\\d)\\}\\{(.+)\\}")

		for count in xrange(local_items_list.count()) :
			Qt.QCoreApplication.processEvents(Qt.QEventLoop.ExcludeUserInputEvents)

			if not item_code_regexp.exactMatch(local_items_list[count]) :
				local_items_list.removeAt(count)
				continue

			if not all_dicts_dir_entry_list.contains(item_code_regexp.cap(2)) :
				local_items_list.removeAt(count)
				continue

		###

		tmp_list = Qt.QStringList(local_items_list)
		tmp_list.replaceInStrings(item_code_regexp, "\\2")

		###

		for count in xrange(all_dicts_dir_entry_list.count()) :
			Qt.QCoreApplication.processEvents(Qt.QEventLoop.ExcludeUserInputEvents)
			if not tmp_list.contains(all_dicts_dir_entry_list[count]) :
				local_items_list << Qt.QString("{0}{%1}").arg(all_dicts_dir_entry_list[count])

		return local_items_list


	### Signals ###

	def dictsListChangedSignal(self, dicts_list) :
		self.emit(Qt.SIGNAL("dictsListChanged(const QStringList &)"), dicts_list)


	### Handlers ###

	def changeEvent(self, event) :
		if event.type() == Qt.QEvent.LanguageChange :
			self.translateUi()
		else :
			Qt.QDialog.changeEvent(self, event)

	###

	def showEvent(self, event) :
		Qt.QDialog.showEvent(self, event)
		self.raise_()
		self.activateWindow()
		self.__dicts_browser.setFocus(Qt.Qt.OtherFocusReason)

