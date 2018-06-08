"""
File: traffic_mqtt.py
By: Gustavo Chavez
"""

import paho.mqtt.client as mqtt


# Define a function for connection
def on_connect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))
    # When subscribing in on_connect function, if connection is lost and regained,
    # subscriptions will be renewed.
    # client.subscribe('$SYS/#')


# The function to use when publish is received from server
def on_message(client, userdata, msg):
    print(msg.topic+' '+str(msg.payload))


