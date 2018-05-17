#!/usr/bin/env python
# -*- coding: utf-8 -*-

# standard modules
import json

# user modules
from pahoawsiot import PahoAwsIot
from speaker import Speaker

class PahoSpeaker(PahoAwsIot, object):

	def __init__(self, config, param):
		super(PahoSpeaker, self).__init__(config['Paho'], param)
		self.speaker = Speaker(config['Aws'], param)

		self.logging = param['logging']

	def _on_message(self, mosq, obj, msg):
		"""
		Define on_message event function. 
		This function will be invoked every time,
		a new message arrives for the subscribed topic 

		:param dict msg: dictionary converted from json
		 str  topic : raspberrypi/{action}
		 int  qos :
		 json payload : {"param1": "...", "param2": "..."}

		  action :
		   speak -- payload : {"text": "...", "voice": "..."}
			:str text: 再生するテキスト
			:str voice: "Takumi" or "Mizuki"
		"""
		try:
			self.logging.info("Topic: " + str(msg.topic))
			self.logging.info("QoS: " + str(msg.qos))
			self.logging.info("Payload: " + str(msg.payload))

			# topic 確認
			topics_pub = msg.topic.split('/', 2)
			topics_sub = self.topic.split('/')
			if topics_pub[0] != topics_sub[0]:
				raise Exception("invalid topic.")

			if len(topics_pub) < 2 :
				raise Exception("can't find action.")
			action = topics_pub[1]

			# 一応下位を取得している
			subtopics = None
			if len(topics_pub) > 2 :
				subtopics = topics_pub[2].split('/')

			# パラメータをjsonデコード
			param = json.loads(msg.payload)

			# action毎の処理
			if action == 'speak':
				self.speaker.play(param)

			# 処理終了
			self.logging.info('end')

		except Exception as e:
			self.logging.error(e)

	def run(self):
		self._loop_forever()
