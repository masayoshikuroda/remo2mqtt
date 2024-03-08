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
        return self.get(self.baseurl + '/1/devices')
    
    def get_appliances(self):
        logging.info("Retrieving appliances...")
        return self.get(self.baseurl + '/1/appliances')
    
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
                info['temperature'] = newest_events['te']['val']
                info['temperature_at'] = newest_events['te']['created_at']
                info['humidity'] = newest_events['hu']['val']
                info['humidity_at'] = newest_events['hu']['created_at']
                info['illuminance'] = newest_events['il']['val']
                info['illuminance_at'] = newest_events['il']['created_at']
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

