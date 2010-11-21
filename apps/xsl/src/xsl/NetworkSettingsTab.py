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
import Settings
import IconsLoader
import LineEdit


##### Public classes #####
class NetworkSettingsTab(Qt.QWidget) :
	def __init__(self, parent = None) :
		Qt.QWidget.__init__(self, parent)

		self.__main_layout = Qt.QVBoxLayout()
		self.setLayout(self.__main_layout)

		#####

		self.__settings = Settings.Settings()

		#####

		self.__use_proxy_checkbox = Qt.QCheckBox(self)
		self.__main_layout.addWidget(self.__use_proxy_checkbox)

		self.__proxy_settings_groupbox = Qt.QGroupBox(self)
		self.__proxy_settings_groupbox.setEnabled(False)
		self.__proxy_settings_groupbox_layout = Qt.QGridLayout()
		self.__proxy_settings_groupbox.setLayout(self.__proxy_settings_groupbox_layout)
		self.__main_layout.addWidget(self.__proxy_settings_groupbox)

		self.__main_layout.addStretch()

		###

		self.__proxy_server_label = Qt.QLabel(self)
		self.__proxy_settings_groupbox_layout.addWidget(self.__proxy_server_label, 0, 0)

		self.__proxy_server_line_edit = LineEdit.LineEdit(self)
		self.__proxy_settings_groupbox_layout.addWidget(self.__proxy_server_line_edit, 0, 1)

		self.__proxy_port_label = Qt.QLabel(self)
		self.__proxy_settings_groupbox_layout.addWidget(self.__proxy_port_label, 1, 0)

		self.__proxy_port_spin_box = Qt.QSpinBox(self)
		self.__proxy_port_spin_box.setRange(0, 50000)
		self.__proxy_settings_groupbox_layout.addWidget(self.__proxy_port_spin_box, 1, 1)

		self.__proxy_user_label = Qt.QLabel(self)
		self.__proxy_settings_groupbox_layout.addWidget(self.__proxy_user_label, 2, 0)

		self.__proxy_user_line_edit = LineEdit.LineEdit(self)
		self.__proxy_settings_groupbox_layout.addWidget(self.__proxy_user_line_edit, 2, 1)

		self.__proxy_passwd_label = Qt.QLabel(self)
		self.__proxy_settings_groupbox_layout.addWidget(self.__proxy_passwd_label, 3, 0)

		self.__proxy_passwd_line_edit = LineEdit.LineEdit(self)
		self.__proxy_passwd_line_edit.setEchoMode(Qt.QLineEdit.Password)
		self.__proxy_settings_groupbox_layout.addWidget(self.__proxy_passwd_line_edit, 3, 1)

		#####

		self.connect(self.__use_proxy_checkbox, Qt.SIGNAL("stateChanged(int)"), self.__proxy_settings_groupbox.setEnabled)

		#####

		self.translateUi()


	### Public ###

	def requisites(self) :
		return {
			"icon" : IconsLoader.icon("network-wired"),
			"title" : Qt.QT_TR_NOOP("Network"),
		}

	###

	def saveSettings(self) :
		self.__settings.setValue("application/network/use_proxy_flag", Qt.QVariant(self.__use_proxy_checkbox.isChecked()))
		self.__settings.setValue("application/network/proxy/host", Qt.QVariant(self.__proxy_server_line_edit.text()))
		self.__settings.setValue("application/network/proxy/port", Qt.QVariant(self.__proxy_port_spin_box.value()))
		self.__settings.setValue("application/network/proxy/user", Qt.QVariant(self.__proxy_user_line_edit.text()))
		self.__settings.setValue("application/network/proxy/passwd", Qt.QVariant(self.__proxy_passwd_line_edit.text()))

	def loadSettings(self) :
		self.__use_proxy_checkbox.setChecked(self.__settings.value("application/network/use_proxy_flag").toBool())
		self.__proxy_server_line_edit.setText(self.__settings.value("application/network/proxy/host").toString())
		self.__proxy_port_spin_box.setValue(self.__settings.value("application/network/proxy/port").toInt()[0])
		self.__proxy_user_line_edit.setText(self.__settings.value("application/network/proxy/user").toString())
		self.__proxy_passwd_line_edit.setText(self.__settings.value("application/network/proxy/passwd").toString())


	### Private ###

	def translateUi(self) :
		self.__use_proxy_checkbox.setText(tr("Use proxy server for internet connections"))
		self.__proxy_settings_groupbox.setTitle(tr("Proxy settings"))
		self.__proxy_server_label.setText(tr("Proxy server:"))
		self.__proxy_port_label.setText(tr("Proxy port:"))
		self.__proxy_user_label.setText(tr("Username:"))
		self.__proxy_passwd_label.setText(tr("Password:"))


	### Handlers ###

	def changeEvent(self, event) :
		if event.type() == Qt.QEvent.LanguageChange :
			self.translateUi()
		else :
			Qt.QWidget.changeEvent(self, event)

