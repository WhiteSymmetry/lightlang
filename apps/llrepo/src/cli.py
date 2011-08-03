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



import sys
import os
import struct
import fcntl
import termios


##### Public methods #####
def terminalWidth(output = sys.stdout) :
	winsize_struct_packed = struct.pack("HHHH", 0, 0, 0, 0)
	try :
		winsize_struct_packed = fcntl.ioctl(output.fileno(), termios.TIOCGWINSZ, winsize_struct_packed)
	except : pass
	winsize_struct_unpacked = struct.unpack("HHHH", winsize_struct_packed)
	return ( winsize_struct_unpacked[1] if winsize_struct_unpacked[1] > 80 else 80 )


###
def formatSize(size) :
	if size >= 1048576 :
		return "%.1f Mb" % (size / 1048576.0)
	elif size > 1024 :
		return "%.1f Kb" % (size / 1024.0)
	else :
		return "%d bytes" % (size)


###
def printLine(line = "", max_width = None, output = sys.stdout, short_flag = False, static = [""]) :
	if max_width == None :
		max_width = terminalWidth(output)

	if os.isatty(output.fileno()) :
		line = line[:max_width]

	if short_flag :
		old_static = static[0]
		static[0] = line
		line = " "*len(old_static) + "\r" + line + "\r"
	else :
		if len(static[0]) != 0 :
			line = " "*len(static[0]) + "\r" + line + "\n"
		else :
			line += "\n"
		static[0] = ""

	output.write(line)
	output.flush()

def printTable(rows_list, output = sys.stdout) :
	max_width = terminalWidth(output)

	sizes_list = [0] * len(rows_list[0])
	for rows_list_item in rows_list :
		for count in xrange(len(rows_list_item)) :
			item = ( str(rows_list_item[count]) if not type(rows_list_item[count]) in (str, unicode) else rows_list_item[count] )
			item_len = len(item)
			if item_len > sizes_list[count] :
				sizes_list[count] = item_len

	format_cell = ( lambda row, column : ("%-"+str(sizes_list[column])+"s") % (rows_list[row][column]) )
	format_row = ( lambda row : " | ".join(map(lambda column : format_cell(row, column), xrange(len(rows_list[row]))))  )

	print >> output
	printLine(format_row(0), max_width, output)
	printLine("-+-".join(map(lambda item_len : "-" * item_len, sizes_list)), max_width, output)
	for row in xrange(1, len(rows_list)) :
		printLine(format_row(row), max_width, output)
	print >> output

