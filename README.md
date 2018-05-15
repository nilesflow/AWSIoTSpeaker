# AWSIoTSpeaker
on RaspberryPi　AWS IoT MQTTのpublish messageをAmazon Pollyして再生

# 準備
RasperrryPIにスピーカーを接続

# セットアップ
pip install paho-mqtt
pip install boto3

vi config.ini
* AWS IoTのHost、証明書情報を入力
* AWS Pollyへのアクセス情報を入力

証明書を配置

# 起動方法
python index.py
