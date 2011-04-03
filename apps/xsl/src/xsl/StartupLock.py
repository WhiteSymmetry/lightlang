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
import os

import Qt
import Const


##### Public methods #####
def test(without_options_list = []) :
	proc_name = os.path.basename(sys.argv[0])
	try :
		uid = os.getuid()
		pid = os.getpid()
	except :
		return

	proc_pids_list = []
	for proc_list_item in os.listdir("/proc") :
		try :
			proc_pid = int(proc_list_item)
		except :
			continue
		if proc_pid == pid :
			continue

		cmdline_file_path = os.path.join("/proc", proc_list_item, "cmdline")
		try :
			if os.stat(cmdline_file_path).st_uid != uid :
				continue
		except :
			continue

		try :
			cmdline_file = open(cmdline_file_path)
			cmdline_list = cmdline_file.read().split("\0")
		except : pass
		try :
			cmdline_file.close()
		except : pass

		if len(cmdline_list) >= 2 and "python" in cmdline_list[0] and os.path.basename(cmdline_list[1]) == proc_name :
			ignore_flag = False
			for without_options_list_item in without_options_list :
				if without_options_list_item in cmdline_list :
					ignore_flag = True
					break
			if not ignore_flag :
				proc_pids_list.append(proc_pid)

	if len(proc_pids_list) != 0 and not Qt.QApplication.instance().isSessionRestored() :
		Qt.QMessageBox.warning(None, Const.MyName, tr("Oops, %1 process is already running, "
			"kill old process and try again.\n").arg(Const.MyName))
		sys.exit(1)

