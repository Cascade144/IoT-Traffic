"""
File: carDriver.py
"""

# IMPORTS ###
import RPi.GPIO as GPIO
import motor
import car_dir
import signal
import paho.mqtt.client as mqtt
from carMQTT import on_subscribe, on_message, on_connect
import sys

# GLOBALS ###
busnum = 1
light_topic = 'intersection/light0'


class GracefulShutdown:
    shutdown = False

    def __init__(self):
        signal.signal(signal.SIGTERM, self.end_program)
        signal.signal(signal.SIGINT, self.end_program)

    def end_program(self):
        self.shutdown = True


def setup():
    global offset_x, offset_y, offset, forward0, forward1
    offset_x = 0
    offset_y = 0
    offset = 0
    forward0 = 'True'
    forward1 = 'False'
    try:
        for line in open('config'):
            if line[0:8] == 'offset_x':
                offset_x = int(line[11:-1])
                print
                'offset_x =', offset_x
            if line[0:8] == 'offset_y':
                offset_y = int(line[11:-1])
                print
                'offset_y =', offset_y
            if line[0:8] == 'offset =':
                offset = int(line[9:-1])
                print
                'offset =', offset
            if line[0:8] == "forward0":
                forward0 = line[11:-1]
                print
                'turning0 =', forward0
            if line[0:8] == "forward1":
                forward1 = line[11:-1]
                print
                'turning1 =', forward1
    except:
        print('no config file, set config to original')
        raise
    car_dir.setup(busnum=busnum)
    motor.setup(busnum=busnum)
    car_dir.calibrate(offset)


def main():
    try:
        setup()
    except KeyboardInterrupt:
        exit()
    killer = GracefulShutdown()
    client_name = 'car0'
    # Begin MQTT connection
    print("Creating MQTT client data...")
    client = mqtt.Client(client_id=client_name, clean_session=True, userdata=None, protocol=mqtt.MQTTv31,
                         transport='tcp')
    client.on_connect = on_connect
    client.on_message = on_message
    print('Connecting to host...')
    client.connect('192.168.1.155', 1883)
    print('Connected...')
    client.subscribe(light_topic)
    motor.setSpeed(50)
    motor.motor0(forward1)
    motor.motor1(forward1)
    print('Moving forward...')
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
