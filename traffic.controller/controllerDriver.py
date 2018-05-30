"""
File: controllerDriver.py
By: Gustavo Chavez
"""


# IMPORTS ###
from trafficMQTT import on_message, on_connect
import signal
import sys
import paho.mqtt.client as mqtt
import time
from multiprocessing import Process

# GLOBALS ###
GPIO_set1 = [13, 19, 26]
GPIO_set2 = [21, 20, 16]
light0_topic = 'intersection/light0'
light1_topic = 'intersection/light1'
light2_topic = 'intersection/light2'
topic_list = [light0_topic, light1_topic, light2_topic]
boolWarning = False
boolDisabled = False
boolDefault = False
colors = ['DEFAULT', 'RED', 'AMBER', 'GREEN']


class GracefulShutdown:
    shutdown = False

    def __init__(self):
        signal.signal(signal.SIGTERM, self.end_program)
        signal.signal(signal.SIGINT, self.end_program)

    def end_program(self):
        self.shutdown = True


def main():
    global boolWarning, boolDisabled, boolDefault
    if len(sys.argv) != 2:
        print('Please enter traffic mode...')
        print('Usage: controllerDriver.py [warning|default|disabled]')
        sys.exit()
    if sys.argv[1] == 'warning':
        boolWarning = True
    elif sys.argv[1] == 'default':
        boolDefault = True
    elif sys.argv[1] == 'disabled':
        boolDisabled = True
    else:
        print('Incorrect parameter')
        sys.exit()
    killer = GracefulShutdown()
    print('Beginning traffic controller')
    # Begin MQTT connection
    print("Creating MQTT client data...")
    client = mqtt.Client(client_id='lightcontroller', clean_session=True, userdata=None, protocol=mqtt.MQTTv31, transport='tcp')
    client.on_connect = on_connect
    client.on_message = on_message
    print('Connecting to host...')
    client.connect('192.168.1.155', 1883)
    print('Connected...')
    rc = 0
    while rc == 0:
        if killer.shutdown:
            client.disconnect()
            client.loop_stop()
            break
        if boolWarning:
            print('WARNING, BROKEN SIGNALS')
            for topic in topic_list:
                client.publish(topic, 'AMBER')
                client.publish(topic, 'AMBER')
            time.sleep(3)
            for topic in topic_list:
                client.publish(topic, 'DEFAULT')
                client.publish(topic, 'DEFAULT')
            time.sleep(3)
        elif boolDisabled:
            killer.shutdown = True
            for topic in topic_list:
                client.publish(topic, 'DEFAULT')
        elif boolDefault:
            for topic in topic_list:
                client.publish(topic, 'GREEN')
        rc = client.loop()
    print('Shutting down...')
    sys.exit()


if __name__ == '__main__':
    main()
