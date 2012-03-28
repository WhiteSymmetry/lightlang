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
import shutil
import errno

import const
import cli


#####
def fetchResources(types_list = ["dicts", "sounds"]) :
	cli.printLine("\nProcessing local repository for %s..." % (str(types_list)))

	resources_dict = dict(map(( lambda item : (item, {}) ), types_list))

	for resource_type in resources_dict.keys() :
		count = 0
		for file_name in os.listdir(os.path.join(const.SL_SHARES_DIR, resource_type)) :
			if file_name.startswith(".") :
				continue

			file_path = os.path.join(const.SL_SHARES_DIR, resource_type, file_name)

			try :
				if resource_type == "dicts" :
					file_size = os.stat(file_path).st_size
				elif resource_type == "sounds" :
					file_size = 0
					for root_dir_path, dirs_list, files_list in os.walk(file_path) :
						for files_list_item in dirs_list + files_list :
							file_size += os.stat(os.path.join(root_dir_path, files_list_item)).st_size

				if file_size <= 0 :
					cli.printLine("--- file \"%s\" :: warning, non-positive size" % (file_path))
					continue
			except Exception, err :
				cli.printLine("--- file \"%s\" :: warning, error while getsize: %s" % (file_path, str(err)))
				continue

			resources_dict[resource_type][file_name] = {
				"file_path" : file_path,
				"file_size" : file_size
			}
			count += 1

		cli.printLine("--- local :: %d %s" % (count, resource_type))

	cli.printLine()

	return resources_dict

def removeResource(resource_name, resource_type) :
	cli.printLine("--- resource \"%s\" :: begin to remove..." % (resource_name), short_flag=True)

	file_path = os.path.join(const.SL_SHARES_DIR, resource_type, resource_name)
	try :
		if resource_type == "dicts" :
			os.remove(file_path)
		elif resource_type == "sounds" :
			shutil.rmtree(file_path)
	except Exception, err :
		cli.printLine("--- resource \"%s\" :: removal failure: %s" % (resource_name, str(err)), short_flag=( err.errno == errno.ENOENT ))
		if err.errno != errno.ENOENT :
			raise

	cli.printLine("--- resource \"%s\" :: removal complete" % (resource_name))

