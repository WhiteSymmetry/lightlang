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


##### Private constants #####
ResizeDirectionNone = 0
ResizeDirectionTop = 1
ResizeDirectionBottom = 2
ResizeDirectionLeft = 3
ResizeDirectionRight = 4
# TopLeft - move
ResizeDirectionTopRight = 5
ResizeDirectionBottomLeft = 6
ResizeDirectionBottomRight = 7


##### Public classes #####
class PopupWindow(Qt.QFrame) :
	def __init__(self, parent = None) :
		Qt.QFrame.__init__(self, parent)

		self.setWindowFlags(Qt.Qt.Popup)

		self.setMouseTracking(True)

		self.setFrameStyle(Qt.QFrame.Box)
		self.setFrameShadow(Qt.QFrame.Raised)

		self.setLineWidth(1)
		self.setMidLineWidth(2)

		####

		self._resize_timer = Qt.QTimer(self)
		self._resize_timer.setInterval(10)

		self._resize_direction = ResizeDirectionNone

		self._move_timer = Qt.QTimer(self)
		self._move_timer.setInterval(10)

		#####

		self.connect(self._resize_timer, Qt.SIGNAL("timeout()"), self.doResize)
		self.connect(self._move_timer, Qt.SIGNAL("timeout()"), self.doMove)


	### Private ###

	def startResize(self) :
		self._resize_timer.start()

	def stopResize(self) :
		self._resize_timer.stop()
		self._resize_direction = ResizeDirectionNone

	def doResize(self) :
		if Qt.QApplication.mouseButtons() == Qt.Qt.NoButton :
			self.stopResize()
			return

		if self._resize_direction == ResizeDirectionNone :
			return

		new_geometry = self.frameGeometry()

		if self._resize_direction == ResizeDirectionTop :
			new_geometry.setTop(Qt.QCursor.pos().y())
		elif self._resize_direction == ResizeDirectionBottom :
			new_geometry.setBottom(Qt.QCursor.pos().y())
		elif self._resize_direction == ResizeDirectionLeft :
			new_geometry.setLeft(Qt.QCursor.pos().x())
		elif self._resize_direction == ResizeDirectionRight :
			new_geometry.setRight(Qt.QCursor.pos().x())
		elif self._resize_direction == ResizeDirectionTopRight :
			new_geometry.setTopRight(Qt.QCursor.pos())
		elif self._resize_direction == ResizeDirectionBottomLeft :
			new_geometry.setBottomLeft(Qt.QCursor.pos())
		elif self._resize_direction == ResizeDirectionBottomRight :
			new_geometry.setBottomRight(Qt.QCursor.pos())

		if new_geometry.width() < self.size().width() / 2 :
			new_geometry.setWidth(self.size().width() / 2)
			new_geometry.moveLeft(self.frameGeometry().left())
		if new_geometry.height() < self.size().height() / 2 :
			new_geometry.setHeight(self.size().height() / 2)
			new_geometry.moveTop(self.frameGeometry().top())

		if new_geometry != self.frameGeometry() :
			self.setGeometry(new_geometry)

	###

	def startMove(self) :
		self._move_timer.start()

	def stopMove(self) :
		self._move_timer.stop()

	def doMove(self) :
		if Qt.QApplication.mouseButtons() == Qt.Qt.NoButton :
			self.stopMove()
			return
		self.move(Qt.QCursor.pos())


	### Handlers ###

	def showEvent(self, event) :
		cursor_position = Qt.QCursor.pos() + Qt.QPoint(15, 15)
		if cursor_position.x() < 0 :
			cursor_position.setX(0)
		if cursor_position.y() < 0 :
			cursor_position.setY(0)

		if cursor_position.x() + self.width() > Qt.QApplication.desktop().width() :
			x_window_position = cursor_position.x() - self.width() - 20
			if x_window_position < 0 :
				x_window_position = Qt.QApplication.desktop().width() - self.width() - 20
		else :
			x_window_position = cursor_position.x()

		if cursor_position.y() + self.height() > Qt.QApplication.desktop().height() :
			y_window_position = cursor_position.y() - self.height() - 20
			if y_window_position < 0 :
				y_window_position = Qt.QApplication.desktop().height() - self.height() - 20
		else :
			y_window_position = cursor_position.y()

		self.move(Qt.QPoint(x_window_position, y_window_position))
		Qt.QWidget.showEvent(self, event)

	###

	def mousePressEvent(self, event) :
		if not self.frameGeometry().contains(event.globalPos()) :
			self.stopResize()
			self.stopMove()
			self.close()
			return

		x = event.x()
		y = event.y()
		w = self.width()
		h = self.height()
		f = self.frameWidth()
		c = 10

		if x < c and y < c : # TopLeft
			self.stopResize()
			self.startMove()
			return

		if x >= w - c and y < c :
			self._resize_direction = ResizeDirectionTopRight
		elif x < c and y >= h - c :
			self._resize_direction = ResizeDirectionBottomLeft
		elif x >= w - c and y >= h - c :
			self._resize_direction = ResizeDirectionBottomRight
		elif x < f :
			self._resize_direction = ResizeDirectionLeft
		elif x >= w - f :
			self._resize_direction = ResizeDirectionRight
		elif y < f :
			self._resize_direction = ResizeDirectionTop
		elif y >= h - f :
			self._resize_direction = ResizeDirectionBottom
		else :
			self._resize_direction = ResizeDirectionNone

		if self._resize_direction != ResizeDirectionNone :
			self.stopMove()
			self.startResize()

	def mouseReleaseEvent(self, event) :
		self.stopResize()
		self.stopMove()

	def mouseMoveEvent(self, event) :
		x = event.x()
		y = event.y()
		w = self.width()
		h = self.height()
		f = self.frameWidth()
		c = 10

		if 0 <= x < c and 0 <= y < c :
			cursor_shape = Qt.Qt.SizeAllCursor
		elif w - c <= x < w and h - c <= y < h :
			cursor_shape = Qt.Qt.SizeFDiagCursor
		elif (w - c <= x < w and 0 <= y < c) or (0 <= x < c and h - c <= y < h) :
			cursor_shape = Qt.Qt.SizeBDiagCursor
		elif 0 <= x <= w and (0 <= y < f or h - f <= y < h) :
			cursor_shape = Qt.Qt.SizeVerCursor
		elif 0 <= y <= h and (0 <= x < f or w - f <= x < w) :
			cursor_shape = Qt.Qt.SizeHorCursor
		else :
			cursor_shape = Qt.Qt.ArrowCursor

		if self.cursor().shape() != cursor_shape :
			self.setCursor(cursor_shape)

