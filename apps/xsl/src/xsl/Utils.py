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


##### Public methods #####
def joinPath(first, *others_list) :
	return Qt.QStringList((first,)+others_list).join(Qt.QDir.separator())

def pathName(path) :
	path = Qt.QString(path)
	index = path.lastIndexOf(Qt.QDir.separator())
	return ( path.left(index) if index >= 0 else Qt.QString() )

def baseName(path) :
	names_list = Qt.QString(path).split(Qt.QDir.separator())
	return names_list[names_list.count() -1]

###

def styledHtml(style, body) :
	return Qt.QString("<html><head><style>%1</style></head><body>%2</body></html>").arg(style).arg(body)

