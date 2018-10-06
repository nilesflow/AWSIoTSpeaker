#!/usr/bin/env python
# -*- coding: utf-8 -*-

# standard modules
import json

# user modules
from pyfw import util
from pyfw.pahoawsiot import PahoAwsIot
from pyfw.error.error import Error, ParamError

from speaker import Speaker

class PahoSpeaker(PahoAwsIot, object):

	def __init__(self, config, **kargs):
		super(PahoSpeaker, self).__init__(
			topic_sub = config['Paho']['MQTT_TOPIC_SUB'],
			ca = config['Paho']['CA_ROOT_CERT_FILE'],
			cert = config['Paho']['THING_CERT_FILE'],
			key = config['Paho']['THING_PRIVATE_KEY'],
			host = config['Paho']['MQTT_HOST'],
			port = config['Paho']['MQTT_PORT'],
			keepalive = config['Paho']['MQTT_KEEPALIVE_INTERVAL'],
			logging = kargs['logging']
		)
		self.speaker = Speaker(
			key = config['Aws']['ACCESS_KEY'],
			secret = config['Aws']['SECRET_KEY'],
			logging = kargs['logging'],
			on_speak = self._on_speak
		)

		self.topic_pub = config['Paho']['MQTT_TOPIC_PUB']

	def _on_message(self, mosq, obj, msg):
		"""
		:param dict msg: dictionary converted from json
		 str  topic : raspberrypi/request/{action}
		 int  qos :
		 json payload : {"param1": "...", "param2": "..."}

		  action :
		   speak -- payload : {"text": "...", "voice": "..."}
			:str text: 再生するテキスト
			:str voice: "Takumi" or "Mizuki"
		"""
		try:
			self.logger.info("Topic: " + str(msg.topic))
			self.logger.info("QoS: " + str(msg.qos))
			self.logger.info("Payload: " + str(msg.payload))

			ack = {}

			# topic 確認
			# Level1:既定文字列のチェック
			levels_pub = msg.topic.split('/', 2)
			levels_sub = self.topic_sub.split('/')
			if levels_pub[0] != levels_sub[0]:
				raise ParamError("invalid topic.")

			# Level2：typeのチェック
			if levels_pub[1] != levels_sub[1]:
				raise ParamError("invalid type.")

			# Level3：actionのチェックと取得
			if len(levels_pub) < 3 :
				raise ParamError("can't find action.")
			action = levels_pub[2]

			# レスポンス
			ack['action'] = action

			"""
			# 一応下位を取得している
			subtopics = None
			if len(topics_pub) > 2 :
				subtopics = topics_pub[2].split('/')
			"""

			# パラメータをjsonデコード
			param = json.loads(msg.payload)

			# リクエストIDをチェック、ACKに設定
			if not param['request_id']:
				raise ParamError("can't find request_id.")
			ack['request_id'] = param['request_id']

			# action毎の処理
			if action == 'speak':
				self.speaker.play(param)
				ack['result'] = '指定されたテキストを読み上げました。'
			else :
				ack['result'] = '対応するactionが見つかりませんでした。'

			# 処理終了
			self.logger.info('success')

		except Error as e:
			self.logger.error(e.description)
			ack['error'] = e.error
			ack['error_description'] = e.description

		except Exception as e:
			self.logger.critical(e)
			self.logger.critical(util.trace())

			ack['error'] = 'internal_error'
			ack['error_description'] = str(e)

		# ACK返却
		json_ack = json.dumps(ack)
		self.mqttc.publish(self.topic_pub, json_ack)
		self.logger.info(self.topic_pub)
		self.logger.info(json_ack)

	def _on_speak(self):
		"""
		音声再生のコールバック
		再生終了を処理
		"""

		# 録音を起動
		self.mqttc.publish('raspberrypi/request/listen', json.dumps({'request_id' : 1}))
		self.logger.info('publish: raspberrypi/request/listen')

