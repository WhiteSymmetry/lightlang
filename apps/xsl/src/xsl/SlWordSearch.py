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


##### Private constants #####
UsuallySearchOption = "-u"
WordCombinationsSearchOption = "-c"
ListSearchOption = "-l"
IllDefinedSearchOption = "-i"


##### Public classes #####
class SlWordSearch(Qt.QObject) :
	def __init__(self, parent = None) :
		Qt.QObject.__init__(self, parent)

		#####

		self.__proc = Qt.QProcess(self)
		self.__proc.setReadChannelMode(Qt.QProcess.MergedChannels)
		self.__proc.setReadChannel(Qt.QProcess.StandardOutput)

		self.__proc_block_flag = False
		self.__proc_kill_flag = False

		self.__proc_args = Qt.QStringList()

		self.__proc_output = Qt.QByteArray()

		self.__dicts_list = Qt.QStringList()

		###

		self.__info_item_regexp = Qt.QRegExp("<font class=\"info_font\">(.*)</font>")
		self.__info_item_regexp.setMinimal(True)

		self.__caption_item_regexp = Qt.QRegExp("<font class=\"dict_header_font\">(.*)</font>")
		self.__caption_item_regexp.setMinimal(True)

		self.__word_item_regexp = Qt.QRegExp("<a href=.*>(.*)</a>")
		self.__word_item_regexp.setMinimal(True)

		#####

		self.connect(self.__proc, Qt.SIGNAL("error(QProcess::ProcessError)"), self.processError)
		self.connect(self.__proc, Qt.SIGNAL("finished(int, QProcess::ExitStatus)"), self.processFinished)
		self.connect(self.__proc, Qt.SIGNAL("stateChanged(QProcess::ProcessState)"), self.processStateChenged)
		self.connect(self.__proc, Qt.SIGNAL("readyReadStandardOutput()"), self.setText)


	### Public ###

	def uFind(self, word) :
		self.find(word, UsuallySearchOption)

	def cFind(self, word) :
		self.find(word, WordCombinationsSearchOption)

	def lFind(self, word) :
		self.find(word, ListSearchOption)

	def iFind(self, word) :
		self.find(word, IllDefinedSearchOption)

	def setDictsList(self, dicts_list) :
		self.__dicts_list = dicts_list


	### Private ###

	def find(self, word, option) :
		word = word.simplified().toLower()
		if word.isEmpty() :
			return

		if self.__proc.state() in (Qt.QProcess.Starting, Qt.QProcess.Running) :
			self.setText()
			self.__proc_kill_flag = True
			self.__proc.kill()

		self.processStartedSignal()

		self.clearRequestSignal()

		self.__proc_output.clear()

		self.__proc_args.clear()
		self.__proc_args << "--output-format=html" << "--use-css=no" << "--use-list="+self.__dicts_list.join("|") << option << word

		while self.__proc_block_flag :
			self.__proc.waitForFinished()
		self.__proc_kill_flag = False
		self.__proc.start(Const.SlBin, self.__proc_args)

	###

	def processError(self, error_code) :
		if error_code == Qt.QProcess.FailedToStart and not self.__proc_kill_flag :
			Qt.QMessageBox.warning(None, Const.MyName, tr("An error occured when creating the search process"))
		elif error_code == Qt.QProcess.Crashed and not self.__proc_kill_flag :
			Qt.QMessageBox.warning(None, Const.MyName, tr("Error of the search process"))
		elif error_code == Qt.QProcess.Timedout and not self.__proc_kill_flag :
			Qt.QMessageBox.warning(None, Const.MyName, tr("Connection lost with search process"))
		elif error_code == Qt.QProcess.WriteError and not self.__proc_kill_flag :
			Qt.QMessageBox.warning(None, Const.MyName, tr("Error while writing data into the search process"))
		elif error_code == Qt.QProcess.ReadError and not self.__proc_kill_flag :
			Qt.QMessageBox.warning(None, Const.MyName, tr("Error while reading data from the search process"))
		elif not self.__proc_kill_flag :
			Qt.QMessageBox.warning(None, Const.MyName, tr("Unknown error occured while executing the search process"))

	def processFinished(self, exit_code) :
		if exit_code and not self.__proc_kill_flag :
			Qt.QMessageBox.warning(None, Const.MyName, tr("Error of the search process"))
		self.processFinishedSignal()

	def processStateChenged(self, state) :
		self.__proc_block_flag = ( state in (Qt.QProcess.Starting, Qt.QProcess.Running) )

	def setText(self) :
		self.__proc_output.append(self.__proc.readAllStandardOutput())

		text = Qt.QString.fromLocal8Bit(str(self.__proc_output))
		for replaces_list_item in (
			("<font class=\"info_font\">This word is not found</font>", tr("<font class=\"info_font\">This word is not found</font>"))
			("<font class=\"info_font\">No dict is connected</font>", tr("<font class=\"info_font\">No dict is connected</font>")) ) :

			text.replace(replaces_list_item[0], replaces_list_item[1])

		#####

		if self.__proc_args[3] in (UsuallySearchOption, WordCombinationsSearchOption) :
			self.textChangedSignal(text)
		else :
			text_list = Qt.QStringList()
			parts_list = text.split("<table border=\"0\" width=\"100%\">")

			#####

			if parts_list.count() == 1 :
				info_item_pos = self.__info_item_regexp.indexIn(text, 0)
				while info_item_pos != -1 :
					text_list << "{{"+self.__info_item_regexp.cap(1)+"}}"
					info_item_pos = self.__info_item_regexp.indexIn(text, info_item_pos +
						self.__info_item_regexp.matchedLength())

				if text_list.count() == 0 :
					text_list << "{{"+text+"}}"

			###

			for parts_list_count in xrange(1, parts_list.count()) :
				if self.__caption_item_regexp.indexIn(parts_list[parts_list_count]) < 0 :
					continue

				text_list << "[["+self.__caption_item_regexp.cap(1)+"]]"

				word_item_pos = self.__word_item_regexp.indexIn(parts_list[parts_list_count], 0)
				while word_item_pos != -1 :
					text_list << self.__word_item_regexp.cap(1)
					word_item_pos = self.__word_item_regexp.indexIn(parts_list[parts_list_count], word_item_pos +
						self.__word_item_regexp.matchedLength())

			#####

			self.listChangedSignal(text_list)


	### Signals ###

	def processStartedSignal(self) :
		self.emit(Qt.SIGNAL("processStarted()"))

	def processFinishedSignal(self) :
		self.emit(Qt.SIGNAL("processFinished()"))

	def clearRequestSignal(self) :
		self.emit(Qt.SIGNAL("clearRequest()"))

	def textChangedSignal(self, text) :
		self.emit(Qt.SIGNAL("textChanged(const QString &)"), text)

	def listChangedSignal(self, text_list) :
		self.emit(Qt.SIGNAL("listChanged(const QStringList &)"), text_list)

