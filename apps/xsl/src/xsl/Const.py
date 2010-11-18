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
import Utils


##### Public constants #####

Package = Qt.QString("LightLang")
PackageVersion = Qt.QString("0.8.6")
MyName = Qt.QString("XSL")
Version = Qt.QString("6.6")

DeveloperMail = Qt.QString("mdevaev@gmail.com")
OffersMail = Qt.QString("developers@lightlang.org.ru")
BugtrackMail = Qt.QString("bugtrack@lightlang.org.ru")
UserCountMail = Qt.QString("usercount@lightlang.org.ru")
HomePageAddress = Qt.QString("http://lightlang.org.ru")


#PrefixDirPath = Qt.QString("@prefix@")
#ExecPrefixDirPath = Qt.QString("@exec_prefix@")
BinsDirPath = Qt.QString("/usr/bin")#Qt.QString("@bindir@")
LibsDirPath = Qt.QString("/usr/lib64")#Qt.QString("@libdir@")
DataRootDirPath = Qt.QString("/usr/share")#Qt.QString("@datarootdir@")
#MansDirPath = Qt.QString("@mandir@")
DocsDirPath = Qt.QString("/usr/share/doc")#Qt.QString("@docdir@")
HtmlDocsDirPath = Utils.joinPath(DocsDirPath, "lightlang/html")

TrDirPath = Utils.joinPath(DataRootDirPath, "xsl/tr")

AllDictsDirPath = Utils.joinPath(DataRootDirPath, "sl/dicts")
AllSoundsDirPath = Utils.joinPath(DataRootDirPath, "sl/sounds")

SlBin = Utils.joinPath(BinsDirPath, "sl")

