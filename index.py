#!/usr/bin/env python
# -*- coding: utf-8 -*-

# standard modules
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/modules')

# user modules
import ConfigParser
from pahospeaker import PahoSpeaker

parser = ConfigParser.ConfigParser()
parser.optionxform = str # 大文字小文字の区別
parser.read('config.ini')

# 全て文字列型で読み込まれる
config = {}
config['Paho'] = dict(parser.items('Paho'))
config['Aws'] = dict(parser.items('Aws'))

# メッセージ受信＆再生
PahoSpeaker(config).run()
