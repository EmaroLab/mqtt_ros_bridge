#!/usr/bin/python
import paho.mqtt.client as mqtt
import rospy

class bridge:

    def __init__(self, publisher, mqtt_topic, client_id = "bridge",user_id = "",password = "", host = "localhost", port = "1883", keepalive = 60):
        self.mqtt_topic = mqtt_topic
        self.client_id = client_id
        self.user_id = user_id
        self.password = password
        self.host = host
        self.port = port
        self.keepalive = keepalive

        self.client = mqtt.Client(self.client_id, clean_session=True)
        self.client.username_pw_set(self.user_id, self.password)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.client.on_unsubscribe = self.on_unsubscribe
        self.client.on_subscribe = self.on_subscribe

        self.client.connect(self.host, self.port, self.keepalive)
        self.publisher = publisher

    def msg_process(self, msg):
        pass

    def looping(self):
        self.client.loop(.1)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.client.subscribe(self.mqtt_topic)

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print "Unexpected disconnection."

    def on_message(self, client, userdata, msg):
        self.publisher.publish(self.msg_process(msg.payload))

    def unsubscribe(self):
        print " unsubscribing"
        self.client.unsubscribe(self.mqtt_topic)

    def disconnect(self):
        print " disconnecting"
        self.client.disconnect()

    def on_unsubscribe(self, client, userdata, mid):
        print "Unsubscribed to " + self.mqtt_topic

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print "Subscribed to " + self.mqtt_topic

    def hook(self):
        self.unsubscribe()
        self.disconnect()
        print " shutting down"