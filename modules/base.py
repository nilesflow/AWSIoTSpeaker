#!/usr/bin/env python
# -*- coding: utf-8 -*-

# standard modules
import os
import logging
import ConfigParser

class Base:
	"""
	基底クラス
	コンフィグ読み込み等の基本処理
	"""

	def __init_config(self, file_config):
		parser = ConfigParser.ConfigParser()
		parser.optionxform = str # 大文字小文字の区別
		parser.read(file_config)

		# 全て文字列型で読み込まれる
		config = {}
		for section in parser.sections():
			config[section] = dict(parser.items(section))

		return config

	def __init_logging(self, config):
		if self.is_daemon:
			dir = '/var/log/'
		else:
			dir = os.getcwd() + '/logs/'

		# ディレクトリ存在チェック
		if not os.path.isdir(dir):
			os.mkdir(dir)

		path = dir + config['FILENAME']

		logging.basicConfig(
			filename = path,
			level = eval("logging." + config['LEVEL']),
			format = "%(asctime)s %(levelname)s %(message)s"
		)
		self.logging = logging

	def __init__(self, file_config, param):
		# コンフィグ読み込み
		self.config = self.__init_config(file_config)
		self.is_daemon = param['is_daemon']

		# ロギング設定
		self.__init_logging(self.config['Logging'])
