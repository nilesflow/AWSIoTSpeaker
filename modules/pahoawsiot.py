#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
see https://github.com/pradeesi/AWS-IoT-with-Python-Paho
"""

# standard modules
import paho.mqtt.client as mqtt
import ssl
import json

class PahoAwsIot:

	def __init__(self, config, param):
		self.topic = config['MQTT_TOPIC']

		# Initiate MQTT Client
		mqttc = mqtt.Client()

		# Assign event callbacks
		mqttc.on_message = self._on_message
		mqttc.on_connect = self._on_connect
		mqttc.on_subscribe = self._on_subscribe

		# Configure TLS Set
		mqttc.tls_set(
			config['CA_ROOT_CERT_FILE'],
			certfile = config['THING_CERT_FILE'],
			keyfile = config['THING_PRIVATE_KEY'],
			cert_reqs = ssl.CERT_REQUIRED,
			tls_version = ssl.PROTOCOL_TLSv1_2,
			ciphers = None
		)

		# Connect with MQTT Broker
		mqttc.connect(
			config['MQTT_HOST'],
			int(config['MQTT_PORT']),
			int(config['MQTT_KEEPALIVE_INTERVAL'])
		)

		self.mqttc = mqttc
		self.logging = param['logging']

	def _on_connect(self, client, userdata, flags, rc):
		"""
		Define on connect event function
		We shall subscribe to our Topic in this function
		"""
		self.mqttc.subscribe(self.topic, 0)

	def _on_message(self, mosq, obj, msg):
		"""
		Define on_message event function. 
		This function will be invoked every time,
		a new message arrives for the subscribed topic 
		"""
		pass

	def _on_subscribe(self, mosq, obj, mid, granted_qos):
		self.logging.info("Subscribed to Topic with QoS: " + str(granted_qos))

	def _loop_forever(self):
		# Continue monitoring the incoming messages for subscribed topic
		self.mqttc.loop_forever()
