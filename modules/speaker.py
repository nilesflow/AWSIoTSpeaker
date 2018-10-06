#!/usr/bin/env python
# -*- coding: utf-8 -*-

# standard modules
import os
import time
import threading
from contextlib import closing
import boto3

# クラウドサーバ等の存在しないケース
try:
	import pygame
	import pygame.mixer
except ImportError:
	pass

class Speaker:
	"""
	音声再生クラス
	"""

	# 出力音声ファイル名
	file_voice = 'polly.mp3'

	# 終了イベント
	EVENT_PLAYEND = pygame.USEREVENT + 1

	def __init__(self, **kargs):
		self.logger = kargs['logging'].getLogger(__name__)

		# 出力音声ファイルパス
		path = os.path.dirname(os.path.abspath(__file__)) + '/../tmp/'
		
		# ディレクトリ存在チェック
		if not os.path.isdir(path):
			os.mkdir(path)

		self.path_voice = path + Speaker.file_voice

		## AWS Client生成
		self.client = boto3.client(
			'polly',
			region_name = 'ap-northeast-1',
			aws_access_key_id = kargs['key'],
			aws_secret_access_key = kargs['secret'],
		)

		# コールバック関数登録
		self.on_speak = kargs['on_speak']

	def threadWaitPlay(self):
		"""
		再生待ち処理
		"""

		# "error: video system not initialized" 対策
		# https://www.raspberrypi.org/forums/viewtopic.php?t=46096
		os.environ["SDL_VIDEODRIVER"] = "dummy"
		pygame.init()

		self.logger.info("PLAY START WAIT")

		# 再生終了待ち
		loop = True
		while loop:
			for event in pygame.event.get():
				if event.type == self.EVENT_PLAYEND:
					loop = False
					break
				time.sleep(0.1)
		self.logger.info("PLAY END")

		# 再生終了をコールバック
		self.on_speak()

	def _play(self):
		"""
		音声ファイル再生
		"""

		# モジュール読み込みチェック（EC2等はデフォルト無し）
		if not pygame.mixer:
			return

		# mixerモジュールの初期化
		pygame.mixer.init()

		# 終了イベントを登録
		pygame.mixer.music.set_endevent(self.EVENT_PLAYEND)

		# 音声再生ファイルの読み込み
		pygame.mixer.music.load(self.path_voice)

		# 再生待ち処理を非デーモン（終了待ちスレッド）として起動
		thread = threading.Thread(target = self.threadWaitPlay)
		thread.start()

		# 音声再生
		pygame.mixer.music.play()

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
		self.logger.info(param)

		## 再生するテキスト
		if 'text' not in param:
			raise Exception('textが指定されていません')
		text = param['text'].encode('utf-8')
		self.logger.info(text)

		## 男女を切り替え
		voice = "Takumi"
		if 'voice' in param:
			voice = param['voice']
		self.logger.info(voice)

		# 生成＆再生
		self._create(text, voice)
		self._play()
