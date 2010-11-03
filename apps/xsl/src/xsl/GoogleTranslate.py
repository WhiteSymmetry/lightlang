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


import json

import Qt
import Const
import Locale
import Settings
import LangsList
import Logger


##### Public classes #####
class GoogleTranslate(Qt.QObject) :
	def __init__(self, parent = None) :
		Qt.QObject.__init__(self, parent)

		#####

		self.__locale = Locale.Locale()
		self.__settings = Settings.Settings()

		self.__http = Qt.QHttp(self)
		self.__http_request_id = -1
		self.__http_abort_flag = False

		self.__http_output = Qt.QByteArray()

		self.__timer = Qt.QTimer(self)
		self.__timer.setInterval(30000)

		self.__sl = Qt.QString()
		self.__tl = Qt.QString()

		#####

		self.connect(self.__http, Qt.SIGNAL("stateChanged(int)"), self.setStatus)
		self.connect(self.__http, Qt.SIGNAL("requestFinished(int, bool)"), self.requestFinished)
		self.connect(self.__http, Qt.SIGNAL("readyRead(const QHttpResponseHeader &)"), self.setText)

		self.connect(self.__timer, Qt.SIGNAL("timeout()"), self.abort)


	### Public ###

	def translate(self, sl, tl, text) :
		self.__http_abort_flag = True
		self.__http.abort()
		self.__http_abort_flag = False

		self.processStartedSignal()

		self.clearRequestSignal()

		self.__http.clearPendingRequests()
		self.__http_output.clear()

		self.wordChangedSignal(tr("Google Translate"))
		self.textChangedSignal(tr("<font class=\"info_font\">Please wait...</font>"))

		text = text.trimmed()

		self.__sl = sl
		self.__tl = tl

		###

		if text.startsWith("http:", Qt.Qt.CaseInsensitive) :
			site = ( Qt.QString("http://translate.google.com/translate?js=y&prev=_t&hl=%1&ie=UTF-8&sl=%2&tl=%3&u=%4")
				.arg(self.__locale.mainLang()).arg(sl).arg(tl).arg(text) )
			Qt.QDesktopServices.openUrl(Qt.QUrl(site))
			self.textChangedSignal(tr("<font class=\"word_header_font\">Link of site \"%1\" translation "
				"was opened in your browser</font><hr><br><a href=\"%2\">%2</a>").arg(text).arg(site))
			self.processFinishedSignal()
			return

		###

		text = Qt.Qt.escape(text)
		text.replace("\"", "&quot;")
		text.replace("\n", "<br>")

		text = Qt.QString.fromLocal8Bit(str(Qt.QUrl.toPercentEncoding(text)))
		text = Qt.QByteArray().append("q="+text)

		http_request_header = Qt.QHttpRequestHeader("POST",
			Qt.QString("/ajax/services/language/translate?v=1.0&type=html&langpair=%1%7C%2").arg(sl).arg(tl), 1, 1)
		http_request_header.setValue("Host", "ajax.googleapis.com")
		http_request_header.setValue("User-Agent", "Mozilla/5.0")
		http_request_header.setValue("Accept", "*/*")
		http_request_header.setValue("Content-Type", "application/x-www-form-urlencoded")
		http_request_header.setContentLength(text.length())
		http_request_header.setValue("Connection", "close")

		if self.__settings.value("application/network/use_proxy_flag").toBool() :
			self.__http.setProxy(self.__settings.value("application/network/proxy/host").toString(),
				self.__settings.value("application/network/proxy/port").toInt()[0],
				self.__settings.value("application/network/proxy/user").toString(),
				self.__settings.value("application/network/proxy/passwd").toString())
		else :
			self.__http.setProxy(Qt.QString(), 0)

		self.__http.setHost("ajax.googleapis.com")
		self.__http_request_id = self.__http.request(http_request_header, text)

		self.__timer.start()

	def abort(self) :
		self.__http_abort_flag = True
		self.__http.abort()
		self.__http_abort_flag = False

		self.statusChangedSignal(Qt.QString())
		self.textChangedSignal(tr("<font class=\"info_font\">Aborted</font>"))


	### Private ###

	def setStatus(self, state) :
		if state == Qt.QHttp.Unconnected :
			self.statusChangedSignal(Qt.QString())
		elif state == Qt.QHttp.HostLookup :
			self.statusChangedSignal(tr("Looking up host..."))
		elif state == Qt.QHttp.Connecting :
			self.statusChangedSignal(tr("Connecting..."))
		elif state == Qt.QHttp.Sending :
			self.statusChangedSignal(tr("Sending request..."))
		elif state == Qt.QHttp.Reading :
			self.statusChangedSignal(tr("Reading data..."))
		elif state == Qt.QHttp.Connected :
			self.statusChangedSignal(tr("Connected"))
		elif state == Qt.QHttp.Closing :
			self.statusChangedSignal(tr("Closing connection..."))

	def setText(self) :
		self.__http_output.append(self.__http.readAll())

	def requestFinished(self, request_id, error_flag) :
		if request_id != self.__http_request_id :
			return

		if error_flag and not self.__http_abort_flag :
			Qt.QMessageBox.warning(None, Const.MyName, tr("HTTP error: %1\nPress \"Yes\" to ignore").arg(self.__http.errorString()))

		self.__timer.stop()

		###

		text = Qt.QTextCodec.codecForName("UTF-8").toUnicode(self.__http_output.data())

		###

		try :
			json_dict = json.loads(unicode(text).encode("utf-8"))
			if json_dict.has_key("responseData") and json_dict.has_key("responseStatus") and json_dict.has_key("responseDetails") :
				responce_data = json_dict["responseData"]
				responce_status = json_dict["responseStatus"]
				responce_details = json_dict["responseDetails"]

				if responce_data != None :
					lang_codes_dict = LangsList.langCodes()
					sl_name = ( tr("%1 (guessed)").arg(LangsList.langName(responce_data["detectedSourceLanguage"], lang_codes_dict))
						if responce_data.has_key("detectedSourceLanguage") else LangsList.langName(self.__sl, lang_codes_dict) )
					tl_name = LangsList.langName(self.__tl, lang_codes_dict)
					text = ( tr("<font class=\"word_header_font\">Translated: %1 &#187; %2</font><hr>%3")
						.arg(sl_name).arg(tl_name).arg(Qt.QString(responce_data["translatedText"])) )
				else :
					text = ( tr("<font class=\"word_header_font\">Invalid server responce</font><hr>Code: %1<br>Message: %2")
						.arg(responce_status).arg(responce_details) )
			else :
				text = ( tr("<font class=\"word_header_font\">Invalid server responce</font><hr>Raw JSON: %1")
					.arg(Qt.QString(unicode(json_dict).encode("utf-8"))) )
		except :
			Qt.QMessageBox.warning(None, Const.MyName, tr("JSON parser exception (see logs for more information).\nPress \"Yes\" to ignore"))
			Logger.warning("JSON parser exception")
			Logger.attachException(Logger.WarningMessage)

		###

		self.textChangedSignal(text)

		self.processFinishedSignal()


	### Signals ###
		
	def processStartedSignal(self) :
		self.emit(Qt.SIGNAL("processStarted()"))

	def processFinishedSignal(self) :
		self.emit(Qt.SIGNAL("processFinished()"))

	def clearRequestSignal(self) :
		self.emit(Qt.SIGNAL("clearRequest()"))

	def wordChangedSignal(self, word) :
		self.emit(Qt.SIGNAL("wordChanged(const QString &)"), word)

	def textChangedSignal(self, text) :
		self.emit(Qt.SIGNAL("textChanged(const QString &)"), text)

	def statusChangedSignal(self, status) :
		self.emit(Qt.SIGNAL("statusChanged(const QString &)"), status)

