#!/usr/bin/env python3
import os
import logging
import logzero
from logzero import logger

from Common.Events import PeriodicEvents
from EdgeAgent import EdgeAgent
from gui import TkinterGUI

# Set a minimum log level
logzero.loglevel(logging.DEBUG)

# Set a logfile (all future log messages are also saved there)
# logzero.logfile("/tmp/logfile.log")

# Set a custom formatter
formatter = logging.Formatter('%(asctime)-15s - %(levelname)s: %(message)s');
# logzero.formatter(formatter)



app = EdgeAgent('AgentH')
app.config['MQTT_BROKER_URL'] = 'iot.eclipse.org'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TLS_ENABLED'] = False

# Construct the instance of periodic events
app.events = PeriodicEvents()

# Construct the instance of GUI interface
app.gui = TkinterGUI()
app.gui.config['TITLE'] = 'MQTT Controler'

# Only critical GUI events manages here to call other functions and gracefully shutdown
@app.gui.on_exit()
def exit_button():
    logger.info('Good Bye')
    os._exit(0)

@app.gui.on_event('btn_hit')
def btn_click():
    logger.info('Clicked')

@app.events.Heartbeat(interval = 0.1)
def foo():
    logger.debug("Heart is Beating!!")

@app.events.DataRecover(interval = 0.5)
def foo2():
    logger.debug("Recover!!")

# The callback for when the client receives a CONNACK response from the server.
@app.on_message()
def handle_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

# The callback for when a PUBLISH message is received from the server.
@app.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

if __name__ == '__main__':
    app.run()
