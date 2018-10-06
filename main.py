#!/usr/bin/env python3
import os
import logging
import uuid
import json

import logzero
from logzero import logger

from Common.Events import PeriodicEvents
from EdgeAgent import EdgeAgent
from gui import TkinterGUI
from Topics import mqttTopics

# Set a minimum log level
logzero.loglevel(logging.DEBUG)

# Set a logfile (all future log messages are also saved there)
# logzero.logfile("/tmp/logfile.log")

# Set a custom formatter
formatter = logging.Formatter('%(asctime)-15s - %(levelname)s: %(message)s');
# logzero.formatter(formatter)


# Set up the MQTT related options
config = {}
config['MQTT_CLIENT_ID'] = 'EdgeAgent_{}'.format(uuid.uuid4())
config['MQTT_BROKER_URL'] = 'iot.eclipse.org'
config['MQTT_BROKER_PORT'] = 1883
config['MQTT_USERNAME'] = ''
config['MQTT_PASSWORD'] = ''
config['MQTT_KEEPALIVE'] = 60
config['MQTT_TLS_ENABLED'] = False

# Construct the EdgeAgent with name, events, and GUI instances
# namespace {app.events, app.gui} are available after this line
app = EdgeAgent(config, PeriodicEvents(), TkinterGUI())

# Register topics to app (this can be done at any time before the on_connect() is called)
app.topics['my topic'] = mqttTopics.myTopic('UniqueID')

# Configure the GUI general settings
app.gui.config['TITLE'] = 'MQTT Controler'

# Only critical GUI events manages here to call other functions and gracefully shutdown
@app.gui.on_exit()
def exit_button():
    app.stop()
    logger.info('Good Bye')
    os._exit(0)

# UI related events use general signal handler with name
@app.gui.on_event('btn_hit')
def btn_click():
    logger.info('Clicked')

# Periodic events of the core running engine/application
@app.events.Heartbeat(interval = 0.5)
def foo():
    logger.debug("Heart is Beating!!")

@app.events.DataRecover(interval = 1.5)
def foo2():
    logger.debug("Recover!!")

# MQTT handlers are named directly with its common name, i.e. on_message
# The callback for when the client receives a CONNACK response from the server.
@app.on_message()
def handle_message(client, userdata, msg):
    print('{} {}'.format(msg.topic, str(msg.payload)))

# The callback for when a PUBLISH message is received from the server.
@app.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# Run main function if this file is the entry file
if __name__ == '__main__':
    app.run()
