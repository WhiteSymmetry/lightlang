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
import Logger


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

AllTagsList = (
	CaptionTag, DirectionTag, GroupTag, VersionTag,
	WordCountTag, FileSizeTag, AuthorTag, UrlTag,
	LicenseTag, CopyrightTag, MiscTag
)


##### Private classes #####
class SlDictsInfoMultiple(Qt.QObject) :
	def __init__(self, parent = None) :
		Qt.QObject.__init__(self, parent)

		#####

		self.__info_cache_dict = {}

		self.__langs_list = LangsList.LangsList()


	### Public ###

	def info(self, tag, dict_name) :
		tag = str(tag)
		dict_name = str(dict_name)

		if not self.__info_cache_dict.has_key(dict_name) :
			self.loadInfo(dict_name)

		if self.__info_cache_dict.has_key(dict_name) and self.__info_cache_dict[dict_name].has_key(tag) :
			return Qt.QString(self.__info_cache_dict[dict_name][tag])
		else :
			return tr("Unavailable")

	def clearInfo(self, dict_name = None) :
		if dict_name == None :
			self.__info_cache_dict = {}
		elif self.__info_cache_dict.has_key(str(dict_name)) :
			self.__info_cache_dict.pop(str(dict_name))


	### Private ###

	def loadInfo(self, dict_name) :
		dict_name = str(dict_name)

		dict_file_name = Utils.joinPath(Const.AllDictsDirPath, dict_name)
		dict_file = Qt.QFile(dict_file_name)
		dict_file_stream = Qt.QTextStream(dict_file)
		if not dict_file.open(Qt.QIODevice.ReadOnly) :
			Logger.warning(Qt.QString("Cannot open dict file \"%1\" for reading info").arg(dict_file_name))
			return

		self.__info_cache_dict[dict_name] = {}
		for all_tags_list_item in AllTagsList :
			self.__info_cache_dict[dict_name][all_tags_list_item] = Qt.QString()

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
				for key_item in self.__info_cache_dict[dict_name].keys() :
					tag = Qt.QString(key_item+":")
					if line.startsWith(tag) :
						line = line.remove(0, tag.length()).simplified()
						key = str(key_item)
						break
				if not self.__info_cache_dict[dict_name][key].isEmpty() :
					self.__info_cache_dict[dict_name][key].append("<br>")
				self.__info_cache_dict[dict_name][key].append(line)

		dict_file.close()

		###

		self.__info_cache_dict[dict_name][FileSizeTag] = Qt.QString().setNum(dict_file.size() / 1024)

		direction_regexp = Qt.QRegExp("((..)-(..))")
		if direction_regexp.exactMatch(self.__info_cache_dict[dict_name][DirectionTag]) :
			icon_width = icon_height = Qt.QApplication.style().pixelMetric(Qt.QStyle.PM_SmallIconSize)
			self.__info_cache_dict[dict_name][DirectionTag] = (
				Qt.QString("<img src=\"%3\" width=\"%1\" height=\"%2\"> &#187; <img src=\"%4\" width=\"%1\" height=\"%2\">"
					"&nbsp;&nbsp;&nbsp;%5 &#187; %6 (%7)").arg(icon_width).arg(icon_height)
						.arg(IconsLoader.iconPath(Utils.joinPath("flags", direction_regexp.cap(2))))
						.arg(IconsLoader.iconPath(Utils.joinPath("flags", direction_regexp.cap(3))))
						.arg(self.__langs_list.langName(direction_regexp.cap(2)))
						.arg(self.__langs_list.langName(direction_regexp.cap(3)))
						.arg(direction_regexp.cap(1)) )

		for tag_key in self.__info_cache_dict[dict_name].keys() :
			if self.__info_cache_dict[dict_name][tag_key].isEmpty() :
				self.__info_cache_dict[dict_name][tag_key] = tr("Unavailable")


##### Public classes #####
class SlDictsInfo(SlDictsInfoMultiple) :
	__sl_dicts_info_multiple_object = None

	def __new__(self, parent = None) :
		if self.__sl_dicts_info_multiple_object == None :
			self.__sl_dicts_info_multiple_object = SlDictsInfoMultiple.__new__(self, parent)
			SlDictsInfoMultiple.__init__(self.__sl_dicts_info_multiple_object, parent)
		return self.__sl_dicts_info_multiple_object

	def __init__(self, parent = None) :
		pass

