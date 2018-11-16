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
payload = { "value": 0, "deviceId": hostname, "label": "Hydrogen Sulfide" }

behavior = "FLAT"

def post_message():
    tmp = payload.copy()      
    tmp['value'] = get_random_number() ## change this
    tmp['behavior'] = behavior
    iotData.publish(topic='SaLaunch/DataGenerationHandler', payload=json.dumps(tmp))

scale = [0, 49]
def get_random_number():    
    if behavior == "RISING":
        return random.random()
    if behavior == "FALLING":
        return random.random()
    return 0

def change_behavior_handler(event, context):
    logger.info("CHANGE BEHAVIOR HANDLER {}".format(event))
    behavior = event["behavior"]
    logger.info("behavior is now" + behavior)

def pinned_handler(event, context):
    """
    Mock function for pinned/long-lived Lambda
    """         
    pass

while True:
    logger.info("running post_message with behavior: " + behavior)
    post_message()
    logger.info("sleeping...")
    time.sleep(5)