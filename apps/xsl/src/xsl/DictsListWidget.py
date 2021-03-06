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
import DictsListWidgetItem


##### Public classes #####
class DictsListWidget(Qt.QTableWidget) :
	def __init__(self, parent = None) :
		Qt.QTableWidget.__init__(self, parent)

		self.setColumnCount(1)
		self.setRowCount(0)

		self.horizontalHeader().hide()
		self.horizontalHeader().setStretchLastSection(True)
		self.verticalHeader().setResizeMode(Qt.QHeaderView.Fixed)
		self.setHorizontalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOff)

		self.setMouseTracking(True)
		self.setSelectionBehavior(Qt.QAbstractItemView.SelectRows)
		self.setSelectionMode(Qt.QAbstractItemView.SingleSelection)
		self.setDragEnabled(True)
		self.setDragDropMode(Qt.QAbstractItemView.InternalMove)
		self.setAcceptDrops(True)
		self.setDropIndicatorShown(True)

		self.setAlternatingRowColors(True)

		#####

		self.__start_drag_point = Qt.QPoint()
		self.__pressed_drag_index = -1
		self.__last_drag_move_y = -1

		self.__scroll_timer = Qt.QTimer()
		self.__scroll_timer.setInterval(200)

		#####

		self.connect(self, Qt.SIGNAL("cellActivated(int, int)"), self.invertDictState)
		self.connect(self, Qt.SIGNAL("currentCellChanged(int, int, int, int)"), self.currentRowChanged)

		self.connect(self.__scroll_timer, Qt.SIGNAL("timeout()"), self.dragMoveScroll)

		self.connect(self.verticalHeader(), Qt.SIGNAL("sectionClicked(int)"), self.setCurrentRow)


	### Public ###

	def setItemsList(self, items_list) :
		self.setRowCount(0)

		item_code_regexp = Qt.QRegExp("\\{(\\d)\\}\\{(.+)\\}")
		for items_list_item in items_list :
			Qt.QCoreApplication.processEvents(Qt.QEventLoop.ExcludeUserInputEvents)
			if not item_code_regexp.exactMatch(items_list_item) :
				continue
			dict_state_flag = bool(item_code_regexp.cap(1).toInt()[0])
			dict_name = item_code_regexp.cap(2)
			self.insertDictItem(DictsListWidgetItem.DictsListWidgetItem(dict_state_flag, dict_name))

		if items_list.count() > 0 :
			self.setCurrentCell(0, 0)
			self.currentRowChangedSignal(0)

		self.dictsListChangedSignal()

	def itemsList(self) :
		items_list = Qt.QStringList()

		for count in xrange(self.rowCount()) :
			Qt.QCoreApplication.processEvents(Qt.QEventLoop.ExcludeUserInputEvents)
			items_list << Qt.QString("{%1}{%2}").arg(self.cellWidget(count, 0).dictState()).arg(self.cellWidget(count, 0).dictName())

		return items_list

	###

	def dictsList(self) :
		dicts_list = Qt.QStringList()

		for count in xrange(self.rowCount()) :
			Qt.QCoreApplication.processEvents(Qt.QEventLoop.ExcludeUserInputEvents)
			if self.cellWidget(count, 0).dictState() :
				dicts_list << self.cellWidget(count, 0).dictName()

		return dicts_list

	###

	def up(self) :
		index = self.currentRow()
		if self.isUpAvailable(index) :
			self.insertDictItem(self.takeDictItem(index), index - 1)
			self.setCurrentCell(index - 1, 0)
			self.dictsListChangedSignal()

	def down(self) :
		index = self.currentRow()
		if self.isDownAvailable(index) :
			self.insertDictItem(self.takeDictItem(index), index + 1)
			self.setCurrentCell(index + 1, 0)
			self.dictsListChangedSignal()

	###

	def setFilter(self, str) :
		for count in xrange(self.rowCount()) :
			dict_name = self.cellWidget(count, 0).dictName().replace(Qt.QRegExp("[\\._]"), " ")
			if not dict_name.contains(str, Qt.Qt.CaseInsensitive) :
				self.hideRow(count)
			else :
				self.showRow(count)


	### Private ###

	def insertDictItem(self, item, index = -1) :
		if index < 0 or index > self.rowCount() :
			self.insertRow(self.rowCount())
			index = self.rowCount() - 1
		else :
			self.insertRow(index)

		self.setRowHeight(index, item.height())
		self.setCellWidget(index, 0, item)

		self.connect(item, Qt.SIGNAL("stateChanged(int)"), self.dictsListChangedSignal)

	def takeDictItem(self, index) :
		if index < 0 or index >= self.rowCount() :
			return None

		dict_state = self.cellWidget(index, 0).dictState()
		dict_name = self.cellWidget(index, 0).dictName()

		self.removeRow(index)

		return DictsListWidgetItem.DictsListWidgetItem(dict_state, dict_name)

	###

	def setCurrentRow(self, index) :
		self.setCurrentCell(index, 0)

	###

	def isUpAvailable(self, index) :
		return ( 0 < index < self.rowCount() )

	def isDownAvailable(self, index) :
		return ( 0 <= index < self.rowCount() - 1 )

	###

	def currentRowChanged(self, index) :
		self.setCurrentCell(index, 0)
		self.currentRowChangedSignal(index)

		self.upAvailableSignal(self.isUpAvailable(index))
		self.downAvailableSignal(self.isDownAvailable(index))

	###

	def invertDictState(self, index) :
		self.cellWidget(index, 0).invertDictState()

	###

	def dragMoveScroll(self) :
		if self.__last_drag_move_y < self.height() / 10 :
			self.verticalScrollBar().setValue(self.verticalScrollBar().value() - 1)
		elif self.height() - self.__last_drag_move_y < self.height() / 10 :
			self.verticalScrollBar().setValue(self.verticalScrollBar().value() + 1)


	### Signals ###

	def currentRowChangedSignal(self, index) :
		self.emit(Qt.SIGNAL("currentRowChanged(int)"), index)

	def dictsListChangedSignal(self) :
		self.emit(Qt.SIGNAL("dictsListChanged(const QStringList &)"), self.dictsList())

	def upAvailableSignal(self, up_available_flag) :
		self.emit(Qt.SIGNAL("upAvailable(bool)"), up_available_flag)

	def downAvailableSignal(self, down_available_flag) :
		self.emit(Qt.SIGNAL("downAvailable(bool)"), down_available_flag)


	### Events ###

	def keyPressEvent(self, event) :
		if event.modifiers() == Qt.Qt.ControlModifier :
			if event.key() == Qt.Qt.Key_Up :
				self.up()
			elif event.key() == Qt.Qt.Key_Down :
				self.down()
		else :
			Qt.QTableWidget.keyPressEvent(self, event)

	###

	def mousePressEvent(self, event) :
		if event.button() == Qt.Qt.LeftButton and self.indexAt(event.pos()).row() > -1 :
			self.__start_drag_point = event.pos()
		Qt.QTableWidget.mousePressEvent(self, event)

	def mouseMoveEvent(self, event) :
		if not ((event.buttons() & Qt.Qt.LeftButton) and self.indexAt(event.pos()).row() > -1) :
			return
		if (event.pos() - self.__start_drag_point).manhattanLength() < Qt.QApplication.startDragDistance() :
			return

		self.__pressed_drag_index = self.indexAt(event.pos()).row()

		mime_data = Qt.QMimeData()
		mime_data.setData("application/x-dictslistwidgetitem", Qt.QByteArray())

		drag = Qt.QDrag(self)
		drag.setMimeData(mime_data)
		drag.setPixmap(Qt.QPixmap.grabWidget(self.cellWidget(self.__pressed_drag_index, 0), 0, 0))
		drag.exec_(Qt.Qt.MoveAction)

	def dragEnterEvent(self, event) :
		if event.mimeData().hasFormat("application/x-dictslistwidgetitem") :
			if event.source() == self :
				event.setDropAction(Qt.Qt.MoveAction)
				event.accept()
			else :
				event.acceptProposedAction()
		else :
			event.ignore()

	def dragMoveEvent(self, event) :
		if event.mimeData().hasFormat("application/x-dictslistwidgetitem") :
			if event.source() == self :
				event.setDropAction(Qt.Qt.MoveAction)
				event.accept()
			else :
				event.acceptProposedAction()
		else :
			event.ignore()

		if event.pos().y() < self.height() / 10 or self.height() - event.pos().y() < self.height() / 10 :
			self.__last_drag_move_y = event.pos().y()
			if not self.__scroll_timer.isActive() :
				self.__scroll_timer.start()
		else :
			if self.__scroll_timer.isActive() :
				self.__scroll_timer.stop()

	def dropEvent(self, event) :
		if event.mimeData().hasFormat("application/x-dictslistwidgetitem") :
			current_drop_index = self.indexAt(event.pos()).row()

			if self.__pressed_drag_index != current_drop_index :
				self.insertDictItem(self.takeDictItem(self.__pressed_drag_index), current_drop_index)
				self.setCurrentCell(current_drop_index, 0)

			if event.source() == self :
				event.setDropAction(Qt.Qt.MoveAction)
				event.accept()
			else :
				event.acceptProposedAction()
		else :
			event.ignore()

		if self.__scroll_timer.isActive() :
			self.__scroll_timer.stop()

