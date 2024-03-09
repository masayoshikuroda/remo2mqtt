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
$ mosquitto_sub -h localhost -p 1883 -t remo2mqtt/#
```
