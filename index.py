#!/usr/bin/env python
# -*- coding: utf-8 -*-

# standard modules
import sys, os

# 実行ディレクトリ＆モジュールパス設定
dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir)
sys.path.append(dir + '/modules')

# user modules
from awsiotspeaker import AwsIoTSpeaker

def run(is_daemon = False):
	param = {
		'is_daemon' : is_daemon
	}
	AwsIoTSpeaker('config.ini', param).run()

def daemonize():
	pid = os.fork()
	if pid > 0:
		f = open('/var/run/aws-iot-speakerd.pid', 'w')
		f.write(str(pid) + "\n")
		f.close()
		sys.exit()

	elif pid == 0:
		run(True)

if __name__== '__main__':
	# コマンドライン引数を判定
	if '-D' in sys.argv:
		# デーモン起動
		daemonize()
	else:
		# 通常起動
		run(False)
