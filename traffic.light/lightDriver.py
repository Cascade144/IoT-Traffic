"""
File: lightDriver.py
By: Gustavo Chavez
"""

# IMPORTS ###
import RPi.GPIO as GPIO
from TrafficLight import TrafficLight
from lightMQTT import on_connect, on_message
import signal
import sys
import paho.mqtt.client as mqtt

# GLOBALS ###
GPIO_set1 = (13, 19, 26)
GPIO_set2 = (21, 20, 16)
pinout_list = [GPIO_set1, GPIO_set2]
topic = 'intersection/light'
signal_light = None


class GracefulShutdown:
    shutdown = False

    def __init__(self):
        signal.signal(signal.SIGTERM, self.disable_lights)
        signal.signal(signal.SIGINT, self.disable_lights)

    def disable_lights(self):
        if isinstance(signal_light, TrafficLight):
            signal_light.disable_lights()
        GPIO.cleanup()
        self.shutdown = True


def main():
    global signal_light
    # Check user invocation
    if len(sys.argv) != 2:
        print('Please enter traffic ID...')
        print('Usage: lightDriver.py [ID]')
        sys.exit()
    light_id = int(sys.argv[1])
    client_name = 'light' + str(light_id)
    light_topic = topic + str(light_id)
    killer = GracefulShutdown()
    print('Beginning light controller with ID ' + str(light_id))
    # Setup pinouts
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # Setup light classes
    signal_light = TrafficLight(pinout_list[light_id][0], pinout_list[light_id][1], pinout_list[light_id][2])
    # Begin MQTT connection
    print("Creating MQTT client data...")
    client = mqtt.Client(client_id=client_name, clean_session=True, userdata=None, protocol=mqtt.MQTTv31, transport='tcp')
    client.on_connect = on_connect
    client.on_message = on_message
    client.user_data_set(signal_light)
    print('Connecting to host...')
    client.connect('192.168.1.155', 1883)
    print('Connected...')
    client.subscribe(light_topic)
    rc = 0
    while rc == 0:
        if killer.shutdown:
            client.disconnect()
            client.loop_stop()
            break

        rc = client.loop()
    print('Shutting down...')
    sys.exit()


if __name__ == '__main__':
    main()
