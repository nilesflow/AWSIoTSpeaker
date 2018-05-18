#!/usr/bin/env python
# -*- coding: utf-8 -*-

# standard modules
import os
from contextlib import closing
import boto3

try:
	import pygamea.mixer
except ImportError:
	pass

class Speaker:
	"""
	音声再生クラス
	"""

	# 出力音声ファイル名
	file_voice = 'polly.mp3'

	def __init__(self, config, param):
		# 出力音声ファイルパス
		path = os.path.dirname(os.path.abspath(__file__)) + '/../tmp/'
		
		# ディレクトリ存在チェック
		if not os.path.isdir(path):
			os.mkdir(path)

		self.path_voice = path + Speaker.file_voice

		## AWS Client生成
		self.client = boto3.client(
			'polly',
			region_name='ap-northeast-1',
			aws_access_key_id = config['ACCESS_KEY'],
			aws_secret_access_key = config['SECRET_KEY'],
		)

		self.logging = param['logging']

	def _play(self):
		"""
		音声ファイル再生
		"""

		# モジュール読み込みチェック（EC2等はデフォルト無し）
		if not pygame.mixer :
			return

		# mixerモジュールの初期化
		pygame.mixer.init()

		# 音声再生ファイルの読み込み
		pygame.mixer.music.load(self.path_voice)

		# 音声再生、および再生回数の設定(-1はループ再生)
		pygame.mixer.music.play(1)

	def _create(self, text, voice):
		"""
		指定文字列の音声ファイル生成
		Amazon Pollyでmp3生成
		
		:param str text: 再生するテキスト
		:param str voice: "Takumi" or "Mizuki"
		"""

		## ファイルが存在した場合は削除
		if os.path.isfile(self.path_voice):
		  os.remove (self.path_voice)

		## 音声データを作成
		response = self.client.synthesize_speech(
			Text = text,
			OutputFormat = 'mp3',
			VoiceId = voice
		)

		## ファイルに追加書き込み
		if 'AudioStream' in response:
			with closing(response['AudioStream']) as stream:
				data = stream.read()
				fw = open(self.path_voice, 'a+')
				fw.write(data)
				fw.close()

	def play(self, param):
		"""
		音声ファイル生成＆再生
		"""
		self.logging.info(param)

		## 再生するテキスト
		if 'text' not in param:
			raise Exception('textが指定されていません')
		text = param['text'].encode('utf-8')
		self.logging.info(text)

		## 男女を切り替え
		voice = "Takumi"
		if 'voice' in param:
			voice = param['voice']
		self.logging.info(voice)

		# 生成＆再生
		self._create(text, voice)
		self._play()
