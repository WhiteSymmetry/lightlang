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


##### Public classes #####
class StatusBar(Qt.QStatusBar) :
	def __init__(self, parent = None) :
		Qt.QStatusBar.__init__(self, parent)

		#####

		self.__activation_semaphore = 0

		self.__timer = Qt.QTimer(self)

		#####

		icon_width = icon_height = label_height = self.style().pixelMetric(Qt.QStyle.PM_SmallIconSize)

		self.__message_label = Qt.QLabel(self)
		self.__message_label.setTextFormat(Qt.Qt.PlainText)
		self.__message_label.setMaximumHeight(label_height)
		self.addWidget(self.__message_label, 1)

		self.__wait_picture_movie = IconsLoader.gifMovie("circular")
		self.__wait_picture_movie.setScaledSize(Qt.QSize(icon_width, icon_height))
		self.__wait_picture_movie.jumpToFrame(0)
		self.__wait_picture_movie_label = Qt.QLabel(self)
		self.__wait_picture_movie_label.setMovie(self.__wait_picture_movie)
		self.__wait_picture_movie_label.hide()
		self.addWidget(self.__wait_picture_movie_label)

		#####

		self.connect(self.__timer, Qt.SIGNAL("timeout()"), self.clearStatusMessage)


	### Public ###

	def startWaitMovie(self) :
		if self.__activation_semaphore != 0 :
			self.__activation_semaphore += 1
			return

		self.__wait_picture_movie_label.show()
		self.__wait_picture_movie.start()

	def stopWaitMovie(self) :
		if self.__activation_semaphore > 1 :
			return
		if self.__activation_semaphore > 0 :
			self.__activation_semaphore -= 1

		self.__wait_picture_movie_label.hide()
		self.__wait_picture_movie.stop()
		self.__wait_picture_movie.jumpToFrame(0)

	###

	def showStatusMessage(self, message, timeout = 2000) :
		self.__message_label.setText(message)
		if timeout != 0 :
			self.__timer.start(timeout)

	def clearStatusMessage(self) :
		self.__message_label.clear()

