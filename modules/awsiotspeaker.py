#!/usr/bin/env python
# -*- coding: utf-8 -*-

# user modules
from base import Base
from pahospeaker import PahoSpeaker

class AwsIoTSpeaker(Base, object):

	def __init__(self, file_config, param):
		# コンフィグ生成等
		super(AwsIoTSpeaker, self).__init__(file_config, param)

	def run(self):
		"""
		メッセージ受信＆再生処理
		"""
		param = {
			'logging' : self.logging
		}
		PahoSpeaker(self.config, param).run()
