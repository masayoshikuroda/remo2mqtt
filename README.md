# remo2mqtt

# 設定

```
$ export REMO_URL=https://api.nature.global
$ export REMO_TOKEN=XXX
$ export MQTT_HOST=localhost
$ export MQTT_PORT=1883
$ export POLLING_INTERVAL=60
```

# 実行
```
$ python remo2mqtt.py
```

# 確認

```
$ mosquitto_sub -h localhost -p 1883 -t 'remo2mqtt/#'
```

## サービスとして実行

### 設定ファイルの配置

- remo2mqtt ファイル中の REMO_TOKEN の値を設定
- remo2qtt ファイルを/etc/default/ にコピー
- remo2mqtt ファイル中の [Service]セクションのの値を修正
- remo2mqtt.service ファイルを/etc/systemd/system/ にコピー

### 有効化
```
$ sudo systemctl daemon-reload
$ sudo systemctl enable remo2matt
$ sudo systemctl start remo2matt
```
