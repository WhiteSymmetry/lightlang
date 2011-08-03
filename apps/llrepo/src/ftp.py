# -*- coding: utf-8 -*-
#
# LLRepo - LightLang repository manager
# Copyright (C) 2007-2016 Devaev Maxim
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


import os
import ftplib

import cli


##### Public methods #####
def connectServer(host, port, user = "", passwd = "", short_flag = False) :
	server = None
	try :
		server = ftplib.FTP()
		cli.printLine("--- server \"%s\" -> %s" % (host, server.connect(host, port)), short_flag=short_flag)
		cli.printLine("--- server \"%s\" -> %s" % (host, server.login(user, passwd)), short_flag=short_flag)
	except Exception, err :
		cli.printLine("Cannot connect to \"%s:%d\": %s" % (host, port, str(err)))
		closeServer(server, short_flag=short_flag)
		raise
	return server

def closeServer(server, short_flag = False) :
	try :
		( server != None and cli.printLine("--- server \"%s\" -> %s" % (server.host, server.quit()), short_flag=short_flag) )
	except : pass


###
def downloadFile(server, remote_file_path, local_file_path) :
	local_file = open(local_file_path, "wb")
	try :
		server.retrbinary("RETR %s" % (remote_file_path), makeDownloadHandler(local_file, server.size(remote_file_path)))
	except :
		local_file.close()
		try :
			os.remove(local_file_path)
		except : pass
		raise
	local_file.close()


##### Private methods #####
def makeDownloadHandler(local_file, size) :
	def download_handler(block, static = [size, 0, cli.formatSize(size)]) :
		local_file.write(block)
		static[1] += len(block)

		percent = (100.0 * static[1]) / static[0]
		cli.printLine("--- retr :: [%s] %3.1f%%   %s of %s" % ( ("=" * int(percent / 2.5)) + (" " * int(40 - percent / 2.5)),
			percent, cli.formatSize(static[1]), static[2] ), short_flag=True)

	return download_handler

