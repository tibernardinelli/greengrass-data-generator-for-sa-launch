import time
import sys
import os
import logging
import json
import socket
import urllib2
import random

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'vendored/'))

import greengrasssdk

logger = logging.getLogger()
logger.setLevel(logging.INFO)

iotData = greengrasssdk.client('iot-data')

hostname = urllib2.urlopen('http://169.254.169.254/latest/meta-data/instance-id').read()
payload = { "value": 0, "deviceId": hostname, "label": "temp" }

def post_message():
    tmp = payload.copy()    
    tmp['value'] = random.random()
    iotData.publish(topic='SaLaunch/DataGenerationHandler', payload=json.dumps(tmp))

scale = [0, 49]
def get_random_number():
    
    pass

def pinned_handler(event, context):
    """
    Mock function for pinned/long-lived Lambda
    """         
    pass

while True:
    post_message()
    time.sleep(5)