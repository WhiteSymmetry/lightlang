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


##### Private constants #####
AudioPostfix = ".ogg"

SoundSearchOption = "-s"


##### Public classes #####
class SlSoundSearch(Qt.QObject) :
	def __init__(self, parent = None) :
		Qt.QObject.__init__(self, parent)

		#####

		self.__proc = Qt.QProcess(self)

		self.__proc_block_flag = False
		self.__proc_kill_flag = False

		self.__proc_args = Qt.QStringList()

		self.__all_sounds_dir = Qt.QDir(Const.AllSoundsDirPath)

		#####

		self.connect(self.__proc, Qt.SIGNAL("error(QProcess::ProcessError)"), self.processError)
		self.connect(self.__proc, Qt.SIGNAL("finished(int, QProcess::ExitStatus)"), self.processFinished)
		self.connect(self.__proc, Qt.SIGNAL("stateChanged(QProcess::ProcessState)"), self.processStateChenged)


	### Public ###

	def find(self, word) :
		word = word.simplified().toLower()
		if word.isEmpty() :
			return

		if self.__proc.state() in (Qt.QProcess.Starting, Qt.QProcess.Running) :
			self.__proc_kill_flag = True
			self.__proc.kill()

		self.__proc_args.clear()
		self.__proc_args << SoundSearchOption << word

		while self.__proc_block_flag :
			self.__proc.waitForFinished()
		self.__proc_kill_flag = False
		self.__proc.start(Const.SlBin, self.__proc_args)

	def checkWord(self, lang, word) :
		word = word.simplified().toLower()
		if word.isEmpty() :
			return False
		return Qt.QFile.exists(Utils.joinPath(Const.AllSoundsDirPath, lang, word[0], word+AudioPostfix))


	### Private ###

	def processError(self, error_code) :
		if error_code == Qt.QProcess.FailedToStart and not self.__proc_kill_flag :
			Qt.QMessageBox.warning(None, Const.MyName, tr("An error occured when creating the search process"))
		elif error_code == Qt.QProcess.Crashed and not self.__proc_kill_flag :
			Qt.QMessageBox.warning(None, Const.MyName, tr("Error of the search process"))
		elif error_code == Qt.QProcess.Timedout and not self.__proc_kill_flag :
			Qt.QMessageBox.warning(None, Const.MyName, tr("Connection lost with search process"))
		elif not self.__proc_kill_flag :
			Qt.QMessageBox.warning(None, Const.MyName, tr("Unknown error occured while executing the search process"))

	def processFinished(self, exit_code) :
		if exit_code and not self.__proc_kill_flag :
			Qt.QMessageBox.warning(None, Const.MyName, tr("Error of the search process"))

	def processStateChenged(self, state) :
		self.__proc_block_flag = ( state in (Qt.QProcess.Starting, Qt.QProcess.Running) )

