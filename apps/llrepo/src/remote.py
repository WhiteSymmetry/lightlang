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
import tarfile
import bz2

import const
import cli
import ftp
import repos


#####
def fetchResources(types_list = ["dicts", "sounds"]) :
	resources_dict = dict(map(( lambda item : (item, {}) ), types_list))

	for repos_list_item in repos.ReposList :
		host = repos_list_item["host"]
		port = repos_list_item["port"]
		user = repos_list_item["user"]
		passwd = repos_list_item["passwd"]

		cli.printLine("Processing remote repository \"%s\" for %s..." % (host, str(types_list)))

		try :
			server = ftp.connectServer(host, port, user, passwd)
		except :
			continue

		for resource_type in resources_dict.keys() :
			count = 0
			for file_path in server.nlst(os.path.join(repos_list_item["root"], resource_type)) :
				if file_path.startswith(".") :
					continue

				try :
					file_size = server.size(file_path)
					if file_size <= 0 :
						cli.printLine("--- file \"%s\" :: warning, non-positive size" % (file_path))
						continue
				except Exception, err :
					cli.printLine("--- file \"%s\" :: warning, error while getsize: %s" % (file_path, str(err)))
					continue

				resource_name = os.path.basename(file_path).replace({
					"dicts" : ".bz2", "sounds" : ".tar.bz2"}[resource_type], "")

				item_dict = {
					"host" : host,
					"port" : port,
					"user" : user,
					"passwd" : passwd,
					"file_path" : file_path,
					"file_size" : file_size
				}

				if not resources_dict[resource_type].has_key(resource_name) :
					resources_dict[resource_type][resource_name] = [item_dict]
				else :
					resources_dict[resource_type][resource_name].append(item_dict)
				count += 1

			cli.printLine("--- server \"%s\" :: %d %s" % (host, count, resource_type))

		ftp.closeServer(server)

	cli.printLine()

	return resources_dict

def installResource(resource_name, resource_type, resources_dict) :
	for resource in resources_dict[resource_type][resource_name] :
		local_file_name = "."+os.path.basename(resource["file_path"])
		local_file_path = os.path.join(const.SL_SHARES_DIR, resource_type, local_file_name)

		try :
			server = ftp.connectServer(resource["host"], resource["port"], resource["user"], resource["passwd"], True)
			ftp.downloadFile(server, resource["file_path"], local_file_path)
			cli.printLine("--- file \"%s\" :: download complete" % (local_file_path), short_flag=True)
		except Exception, err :
			cli.printLine("--- file \"%s\" :: download error: %s" % (local_file_path, str(err)))
			continue

		if resource_type == "dicts" :
			try :
				dict_bz2 = bz2.BZ2File(local_file_path)
				dict_file = open(os.path.join(os.path.join(const.SL_SHARES_DIR, resource_type, resource_name)), "w")
				while True :
					line = dict_bz2.readline()
					if len(line) == 0 :
						break
					dict_file.write(line)
				dict_bz2.close()
				dict_file.close()
			except Exception, err :
				try :
					dict_bz2.close()
				except : pass
				try :
					dict_file.close()
				except : pass
				try :
					os.remove(local_file_path)
				except : pass
				cli.printLine("--- file \"%s\" :: bunzip2 error: %s" % (local_file_path, str(err)))
				continue

		elif resource_type == "sounds" :
			try :
				sound_tar = tarfile.open(local_file_path)
				sound_tar.extractall(os.path.join(const.SL_SHARES_DIR, resource_type))
				sound_tar.close()
			except Exception, err :
				try :
					sound_tar.close()
				except : pass
				try :
					os.remove(local_file_path)
				except : pass
				cli.printLine("--- file \"%s\" :: untar error: %s" % (local_file_path, str(err)))
				continue

		try :
			os.remove(local_file_path)
		except : pass

		cli.printLine("--- resource \"%s\" :: installation complete" % (resource_name))
		return

	cli.printLine("--- resource \"%s\" :: installation failure :-(" % (resource_name))

