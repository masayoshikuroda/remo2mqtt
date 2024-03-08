import os
import sys
import time
import logging
import json
from urllib.parse import urlencode
from urllib.request import urlopen, Request, URLError, HTTPError
import asyncio
from remo_scanner import RemoScanner
from mqtt_publisher import MQTTPublisher

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

REMO_URL = os.environ.get('REMO_URL', 'https://api.nature.global')
REMO_TOKEN = os.environ.get('REMO_TOKEN', 'token')
MQTT_HOST = os.environ.get('MQTT_HOST', 'localhost')
MQTT_PORT = int(os.environ.get('MQTT_PORT', '1883'))
POLLING_INTERVAL = int(os.environ.get('POLLING_INTERVAL', '60'))

remo = RemoScanner(REMO_URL, REMO_TOKEN)
mqtt = MQTTPublisher(MQTT_HOST, MQTT_PORT, 'remo2mqtt')

def detection_callback(info):
    mqtt.publish(info['mac_address'], info['id'], info)

def scan():
    remo.scan(detection_callback)

def main():
   while True:
        scan()
        time.sleep(POLLING_INTERVAL)

main()