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
import IconsLoader


##### Public classes #####
class InternetLinksMenu(Qt.QMenu) :
	def __init__(self, title, parent = None) :
		Qt.QMenu.__init__(self, title, parent)

		#####

		self.translateUi()


	### Private ###

	def translateUi(self) :
		self.clear()

		self.addMailLink(IconsLoader.icon("mail-send"), tr("Developer e-mail"), Const.DeveloperMail, Const.Package)
		self.addMailLink(IconsLoader.icon("mail-send"), tr("Offers e-mail"), Const.OffersMail, Const.Package)
		self.addMailLink(IconsLoader.icon("mail-send"), tr("Bugtrack e-mail"), Const.BugtrackMail, Const.Package)
		self.addSeparator()
		self.addLink(IconsLoader.icon("applications-internet"), tr("Home page"), Const.HomePageAddress)
		self.addSeparator()

		self.addMailLink(IconsLoader.icon("mail-send"), tr("Register %1").arg(Const.Package), Const.UserCountMail,
			"&body="+tr("Count me, please :-)\nRegistration date/time: %1\nPackage version: %2")
				.arg(Qt.QDateTime().currentDateTime().toString()).arg(Const.PackageVersion))

	###

	def addLink(self, icon, title, link) :
		self.addAction(icon, title, lambda : Qt.QDesktopServices.openUrl(Qt.QUrl(link)))

	def addMailLink(self, icon, title, mailto, subject) :
		self.addLink(icon, title, Qt.QString("mailto:%1?subject=%2").arg(mailto).arg(subject))


	### Handlers ###

	def changeEvent(self, event) :
		if event.type() == Qt.QEvent.LanguageChange :
			self.translateUi()
		else :
			Qt.QMenu.changeEvent(self, event)

