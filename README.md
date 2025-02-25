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
- remo2mqtt.service ファイル中の [Service]セクションのの値を修正
- remo2mqtt.service ファイルを/etc/systemd/system/ にコピー

### 有効化
```
$ sudo systemctl daemon-reload
$ sudo systemctl enable remo2matt
$ sudo systemctl start remo2matt
```

## Home Assistantと統合

MQTT統合を利用する。

### センサーの追加

configuration.yamlを編集し、mqttのセンサ-を構成する。
以下温度センサ-の設定例:
```
mqtt:
  sensor:
    - name: "Remo XXXX Temperature"
      state_topic: "remo2mqtt/XX:XX:XX:XX:XX:XX/info"
      value_template: "{{ value_json.temperature }}"
      unique_id: "remo-xxxxxxxxxxxx-temperature"
      state_class: "measurement"
      device_class: "temperature"
      unit_of_measurement: "℃"
      device:
        name: "Nature Remo"
        identifiers: ["remo-xxxxxxxxxxxx"]
        manufacturer: "Nature Inc."
        model: "Nature Remo"
        serial_number: "YYYYYYYYYYYYYY"
```

Remo Eを利用している場合、電力、電力量をセンサーとして設定できる。
以下電力量センサーの設定例:
```
    - name: "RemoE XXXX Energy"
      state_topic: "remo2mqtt/XX:XX:XX:XX:XX:XX/info"
      value_template: "{{ value_json.normal_direction_cumulative_electric_energy }}"
      unique_id: "remoe-xxxxxxxxxxxx-energy"
      state_class: "total_increasing"
      device_class: "energy"
      unit_of_measurement: "kWh"
      device:
        name: "Nature Remo E lite"
        identifiers: [ "remoe-xxxxxxxxxxxx" ]
        manufacturer: "Nature Inc."
        model: "Nature Remo E lite"
        serial_number: "YYYYYYYYYYYYYY"
```
deviceクラスとして "energy" を設定する。

### エネルギー設定

1. Home Assistantのダッシュボードに　エネルギーを追加する。
2. エネルギーを表示し、右上のハンバーガーメニューをクリックし、エネルギーの設定メニューを選択する。
3. 電力網パネルから、電力網の追加をクリックする。
4. 電力量センサーを追加する。
