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

		self._main_layout = Qt.QVBoxLayout()
		self.setLayout(self._main_layout)

		#####

		self._use_proxy_checkbox = Qt.QCheckBox(tr("Use proxy server for internet connections"), self)
		self._main_layout.addWidget(self._use_proxy_checkbox)

		self._proxy_settings_group_box = Qt.QGroupBox(tr("Proxy settings"), self)
		self._proxy_settings_group_box.setEnabled(False)
		self._proxy_settings_group_box_layout = Qt.QGridLayout()
		self._proxy_settings_group_box.setLayout(self._proxy_settings_group_box_layout)
		self._main_layout.addWidget(self._proxy_settings_group_box)

		self._main_layout.addStretch()

		###

		self._proxy_server_label = Qt.QLabel(tr("Proxy server:"), self)
		self._proxy_settings_group_box_layout.addWidget(self._proxy_server_label, 0, 0)

		self._proxy_server_line_edit = LineEdit.LineEdit(self)
		self._proxy_settings_group_box_layout.addWidget(self._proxy_server_line_edit, 0, 1)

		self._proxy_port_label = Qt.QLabel(tr("Proxy port:"), self)
		self._proxy_settings_group_box_layout.addWidget(self._proxy_port_label, 1, 0)

		self._proxy_port_spin_box = Qt.QSpinBox(self)
		self._proxy_port_spin_box.setRange(0, 50000)
		self._proxy_settings_group_box_layout.addWidget(self._proxy_port_spin_box, 1, 1)

		self._proxy_user_label = Qt.QLabel(tr("Username:"), self)
		self._proxy_settings_group_box_layout.addWidget(self._proxy_user_label, 2, 0)

		self._proxy_user_line_edit = LineEdit.LineEdit(self)
		self._proxy_settings_group_box_layout.addWidget(self._proxy_user_line_edit, 2, 1)

		self._proxy_passwd_label = Qt.QLabel(tr("Password:"), self)
		self._proxy_settings_group_box_layout.addWidget(self._proxy_passwd_label, 3, 0)

		self._proxy_passwd_line_edit = LineEdit.LineEdit(self)
		self._proxy_passwd_line_edit.setEchoMode(Qt.QLineEdit.Password)
		self._proxy_settings_group_box_layout.addWidget(self._proxy_passwd_line_edit, 3, 1)

		#####

		self.connect(self._use_proxy_checkbox, Qt.SIGNAL("stateChanged(int)"), self._proxy_settings_group_box.setEnabled)


	### Public ###

	def requisites(self) :
		return {
			"icon" : IconsLoader.icon("network-wired"),
			"title" : tr("Network"),
		}

	###

	def saveSettings(self) :
		settings = Settings.settings()
		settings.setValue("application/network/use_proxy_flag", Qt.QVariant(self._use_proxy_checkbox.isChecked()))
		settings.setValue("application/network/proxy/host", Qt.QVariant(self._proxy_server_line_edit.text()))
		settings.setValue("application/network/proxy/port", Qt.QVariant(self._proxy_port_spin_box.value()))
		settings.setValue("application/network/proxy/user", Qt.QVariant(self._proxy_user_line_edit.text()))
		settings.setValue("application/network/proxy/passwd", Qt.QVariant(self._proxy_passwd_line_edit.text()))

	def loadSettings(self) :
		settings = Settings.settings()
		self._use_proxy_checkbox.setChecked(settings.value("application/network/use_proxy_flag", Qt.QVariant(False)).toBool())
		self._proxy_server_line_edit.setText(settings.value("application/network/proxy/host").toString())
		self._proxy_port_spin_box.setValue(settings.value("application/network/proxy/port").toInt()[0])
		self._proxy_user_line_edit.setText(settings.value("application/network/proxy/user").toString())
		self._proxy_passwd_line_edit.setText(settings.value("application/network/proxy/passwd").toString())

