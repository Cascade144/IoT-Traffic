"""
File: carMQTT.py
By: Gustavo Chavez
"""
import motor

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
    if color_str == 'GREEN':
        motor.setSpeed(50)
        motor.start()




def on_subscribe(client, userdata, mid, granted_qos):
    print('Client subscribed')