# AwsIoTSpeaker
on RaspberryPi  
AWS IoT MQTTのpublish messageをAmazon Pollyして再生

# 動作環境
Python 2.7.13 で確認

# 準備
RasperrryPIにスピーカーを接続

証明書を配置

```vi config.ini
# AWS IoTのHost、証明書情報を入力
# AWS Pollyへのアクセス情報を入力
```

# セットアップ
```
# pip install paho-mqtt  
# pip install boto3
# pip install pygame
```

※シェル実行のみなら
```
$ pip install paho-mqtt  
$ pip install boto3
$ pip install pygame
```

# 起動方法
## シェル実行
```
python index.py
```
```
python index.py &
```

## デーモン起動
```
python index.py -D
```

## サービス起動
```
vi aws-iot-speakerd.service
# 下記パスを修正
ExecStart=/usr/bin/env python /path/to/AwsIoTSpeaker/index.py -D
```
```
sudo cp aws-iot-speakerd.service /usr/lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start aws-iot-speakerd
sudo systemctl enable aws-iot-speakerd
```

# トラブルシューティング
音が鳴らない場合は、出力をヘッドホン固定に。  
```amixer cset numid=3 1```
