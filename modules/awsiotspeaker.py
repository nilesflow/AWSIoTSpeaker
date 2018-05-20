#!/usr/bin/env python
# -*- coding: utf-8 -*-

# user modules
from pyfw.appbase import AppBase
from pahospeaker import PahoSpeaker

class AwsIoTSpeaker(AppBase, object):

	def __init__(self, **kargs):
		# コンフィグ生成等
		super(AwsIoTSpeaker, self).__init__(**kargs)

		# 待ち受けモジュール
		self.speaker = PahoSpeaker(
			self.config,
			logging = self.logging
		)

	def run(self):
		"""
		メッセージ受信＆再生処理
		"""
		self.speaker.loop_forever()
