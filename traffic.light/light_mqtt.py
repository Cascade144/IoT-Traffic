"""
File: trafficMQTT.py
By: Gustavo Chavez
"""


# Define a function for connection
def on_connect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))
    # When subscribing in on_connect function, if connection is lost and regained,
    # subscriptions will be renewed.
    # client.subscribe('$SYS/#')


# The function to use when publish is received from server
def on_message(client, userdata, msg):
    print('Msg received...')
    print(msg.topic+' '+str(msg.payload))
    print(msg.payload.decode())
    color_str = str(msg.payload.decode())
    print(userdata)
    if userdata is not None:
        print('Signal light is available')
        userdata.set_status(color_str.rstrip())
        userdata.enable()


def on_subscribe(client, userdata, mid, granted_qos):
    print('Client subscribed')

