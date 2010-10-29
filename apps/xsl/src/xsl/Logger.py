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


import sys
import traceback
import inspect

import Qt
import Settings


##### Public constants #####
FatalMessage = (0, Qt.qFatal)
CriticalMessage = (1, Qt.qCritical)
WarningMessage = (2, Qt.qWarning)
DebugMessage = (3, Qt.qDebug)

AllMessagesList = (
	FatalMessage,
	CriticalMessage,
	WarningMessage,
	DebugMessage
)

AllMessagesTextsList = (
	(" Fatal  ", "\033[31m Fatal  \033[0m"),
	("Critical", "\033[31mCritical\033[0m"),
	("Warning ", "\033[33mWarning \033[0m"),
	(" Debug  ", " Debug  ")
)

ModuleCallerNameTag = "{mod}"
CurrentTimeTag = "{time}"


##### Private methods #####
def log(message_type, message) :
	if not message_type in AllMessagesList :
		log(WarningMessage, Qt.QString("Message type %1 not in valid range, caller: {mod}").arg(str(message_type)))
		return

	message = Qt.QString(message)

	if Settings.settings().value("application/logger/debug_mode_flag", Qt.QVariant(False)).toBool() :
		if message.contains(ModuleCallerNameTag) :
			try :
				message.replace(ModuleCallerNameTag, inspect.getmodule(inspect.currentframe().f_back.f_back).__name__)
			except : pass
		elif message.contains(CurrentTimeTag) :
			message.replace(CurrentTimeTag, Qt.QDateTime().currentDateTime().toString())

		colored_index = int(sys.stderr.isatty())
		for message_list_item in message.split("\n") :
			message_type[1](Qt.QString("[ %1 ] %2").arg(AllMessagesTextsList[message_type[0]][colored_index]).arg(message_list_item))


##### Public methods #####
def fatal(message) :
	log(FatalMessage, message)

def critical(message) :
	log(CriticalMessage, message)

def warning(message) :
	log(WarningMessage, message)

def debug(message) :
	log(DebugMessage, message)

###

def attachException(message_type = CriticalMessage) :
	for line in traceback.format_exc().splitlines() :
		log(message_type, line)

