import os
import sys
import logging
import json
from urllib.parse import urlencode
from urllib.request import urlopen, Request, URLError, HTTPError

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

class RemoScanner:
    def __init__(self, baseurl, token):
        self.baseurl = baseurl
        self.token = token
    
    def get(self, url):
        headers = { "Authorization" : "Bearer " + self.token }
        req = Request(url, data=None, headers=headers)
        try:
            res = urlopen(req)
            body = res.read().decode()
            return json.loads(body)
        except HTTPError as e:
            logger.exception('Error code: ', e.getcode())
        except URLError as e:
            logger.exception('Reason: ', e.reason)

    def get_devices(self):
        logging.info("Retrieving devices...")
        devices = self.get(self.baseurl + '/1/devices')
        logger.debug(json.dumps(devices, ensure_ascii=False, indent=2))
        return devices
    
    def get_appliances(self):
        logging.info("Retrieving appliances...")
        appliances = self.get(self.baseurl + '/1/appliances')
        logger.debug(json.dumps(appliances, ensure_ascii=False, indent=2))
        return appliances
 
    def scan(self, detection_callback):
        logger.info("Scanning Remo information...")
        devices = self.get_devices()
        for i, device in enumerate(devices):
            if 'newest_events' in device and 'te' in device['newest_events']:
                info = {}
                info['id'] = device['id']
                info['name'] = device['name']
                info['type'] = device['firmware_version'].split('/')[0]
                info['mac_address'] = device['mac_address']
                info['serial_number'] = device['serial_number']

                newest_events = device['newest_events']
                if 'te' in newest_events:
                    info['temperature'] = newest_events['te']['val']
                    info['temperature_at'] = newest_events['te']['created_at']
                if 'hu' in newest_events:
                    info['humidity'] = newest_events['hu']['val']
                    info['humidity_at'] = newest_events['hu']['created_at']
                if 'il' in newest_events:
                    info['illuminance'] = newest_events['il']['val']
                    info['illuminance_at'] = newest_events['il']['created_at']
                if 'mo' in newest_events:
                    info['movement'] = newest_events['mo']['val']
                    info['movement_at'] = newest_events['mo']['created_at']

                detection_callback(info)

        appliances = self.get_appliances()
        for i, appliance in enumerate(appliances):
            if 'smart_meter' in appliance:
                info = {}
                device = appliance['device']
                info['id'] = device['id']
                info['name'] = device['name']
                info['type'] = device['firmware_version'].split('/')[0]
                info['mac_address'] = device['mac_address']
                info['serial_number'] = device['serial_number']

                smart_meter = appliance['smart_meter']
                props = smart_meter['echonetlite_properties']
                for i, prop in enumerate(props):
                    key = prop['name']
                    val = prop['val']
                    info[key] = val
                    info[key + '_at'] = prop['updated_at']

                detection_callback(info)

    def get_homeassitatnt_config(topic, data):
        config = {}
        config['name'] = f"{data['name']} {data['mac_address']} Temperature"
        config['state_topic'] = f"{topic}/{data['address']}/info"
        config['device_class'] = 'temperature'
        config['device'] = {}
        config['device']['manufacturer'] = 'Nature Inc.'
        config['device']['model'] = data['name']
        config['device']['serial_number'] = data['serial_number']
        config['value_template'] = '{{ value_json.temperature }}'
        config['suggested_display_precision'] = 1
        config['unit_of_measurement']  = '°C'
        return config

def _detection_callback(info):
    print('====== detection callback ======')
    print(json.dumps(info, ensure_ascii=True, indent=2))

if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    REMO_URL = os.environ.get('REMO_URL', 'https://api.nature.global')
    REMO_TOKEN = os.environ.get('REMO_TOKEN', 'token')
    remo = RemoScanner(REMO_URL, REMO_TOKEN)
    remo.scan(_detection_callback)
