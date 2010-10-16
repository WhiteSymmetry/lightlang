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
import IconsLoader
import LangsList


##### Private constants #####
CaptionTag = "Caption"
DirectionTag = "Direction"
GroupTag = "Group"
VersionTag = "Version"
WordCountTag = "WordCount"
FileSizeTag = "FileSize"
AuthorTag = "Author"
UrlTag = "Url"
LicenseTag = "License"
CopyrightTag = "Copyright"
MiscTag = "Misc"

AllTagsList = [
	CaptionTag, DirectionTag, GroupTag, VersionTag,
	WordCountTag, FileSizeTag, AuthorTag, UrlTag,
	LicenseTag, CopyrightTag, MiscTag
]


##### Private objects #####
InfoDictObject = {}


##### Public methods #####
def info(tag, dict_name) :
	tag = str(tag)
	dict_name = str(dict_name)

	if not InfoDictObject.has_key(dict_name) :
		loadInfo(dict_name)

	if InfoDictObject.has_key(dict_name) and InfoDictObject[dict_name].has_key(tag) :
		return Qt.QString(InfoDictObject[dict_name][tag])
	return tr("Unavailable")

def clearInfo(dict_name = None) :
	global InfoDictObject

	if dict_name == None :
		InfoDictObject = {}
	else :
		if InfoDictObject.has_key(str(dict_name)) :
			InfoDictObject.pop(str(dict_name))


##### Private methods #####
def loadInfo(dict_name) :
	dict_name = str(dict_name)

	global InfoDictObject

	dict_file = Qt.QFile(Utils.joinPath(Const.AllDictsDir, dict_name))
	dict_file_stream = Qt.QTextStream(dict_file)
	if not dict_file.open(Qt.QIODevice.ReadOnly) :
		return

	InfoDictObject[dict_name] = {}
	for all_tags_list_item in AllTagsList :
		InfoDictObject[dict_name][all_tags_list_item] = Qt.QString()

	while not dict_file_stream.atEnd() :
		Qt.QCoreApplication.processEvents(Qt.QEventLoop.ExcludeUserInputEvents)
		line = dict_file_stream.readLine()

		if line.isEmpty() :
			continue
		if line[0] != "#" and line.contains("  ") :
			break

		if line[0] == "#" :
			line.remove(0, 1)
			line = line.trimmed()

			key = MiscTag
			for key_item in InfoDictObject[dict_name].keys() :
				tag = Qt.QString(key_item+":")
				if line.startsWith(tag) :
					line = line.remove(0, tag.length()).simplified()
					key = str(key_item)
					break

			if not InfoDictObject[dict_name][key].isEmpty() :
				InfoDictObject[dict_name][key].append("<br>")
			InfoDictObject[dict_name][key].append(line)

	dict_file.close()

	###

	InfoDictObject[dict_name][FileSizeTag] = Qt.QString().setNum(dict_file.size() / 1024)

	direction_regexp = Qt.QRegExp("((..)-(..))")
	if direction_regexp.exactMatch(InfoDictObject[dict_name][DirectionTag]) :
		icon_width = icon_height = Qt.QApplication.style().pixelMetric(Qt.QStyle.PM_SmallIconSize)
		InfoDictObject[dict_name][DirectionTag] = (
			Qt.QString("<img src=\"%3\" width=\"%1\" height=\"%2\"> &#187; <img src=\"%4\" width=\"%1\" height=\"%2\">"
				"&nbsp;&nbsp;&nbsp;%5 &#187; %6 (%7)").arg(icon_width).arg(icon_height)
					.arg(IconsLoader.iconPath(Utils.joinPath("flags", direction_regexp.cap(2))))
					.arg(IconsLoader.iconPath(Utils.joinPath("flags", direction_regexp.cap(3))))
					.arg(LangsList.langName(direction_regexp.cap(2))).arg(LangsList.langName(direction_regexp.cap(3)))
					.arg(direction_regexp.cap(1)) )
		
	for key_item in InfoDictObject[dict_name].keys() :
		if InfoDictObject[dict_name][key_item].isEmpty() :
			InfoDictObject[dict_name][key_item] = tr("Unavailable")

