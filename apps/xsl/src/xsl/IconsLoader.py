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
import Config
import Utils


##### Private constants #####
ImagePostfix = ".png"
GifPostfix = ".gif"

IconsDir = Utils.joinPath(Config.DataRootDir, "xsl/icons")
PicturesDir = Utils.joinPath(Config.DataRootDir, "xsl/pictures")
GifsDir = Utils.joinPath(Config.DataRootDir, "xsl/pictures")


##### Public methods #####
def icon(name, fallback_name = None) :
	fallback_icon = Qt.QIcon(Utils.joinPath(IconsDir, name+ImagePostfix))
	if fallback_name != None :
		fallback_icon = Qt.QIcon.fromTheme(fallback_name, fallback_icon)
	return Qt.QIcon.fromTheme(name, fallback_icon)

def iconPath(name) :
	return Qt.QString(Utils.joinPath(IconsDir, name+ImagePostfix))

###

def pixmap(name) :
	return Qt.QPixmap(Utils.joinPath(PicturesDir, name+ImagePostfix))

def gifMovie(name) :
	return Qt.QMovie(Utils.joinPath(GifsDir, name+GifPostfix))

