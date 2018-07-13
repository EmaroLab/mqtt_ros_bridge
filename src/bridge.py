#!/usr/bin/python
import paho.mqtt.client as mqtt
import rospy
import time

class bridge:

    def __init__(self, publisher, mqtt_topic, client_id = "bridge",user_id = "",password = "", host = "localhost", port = "1883", keepalive = 60):
        self.mqtt_topic = mqtt_topic
        self.client_id = client_id
        self.user_id = user_id
        self.password = password
        self.host = host
        self.port = port
        self.keepalive = keepalive

        self.disconnect_flag = False
        self.rc = 1
        self.timeout = 0

        self.client = mqtt.Client(self.client_id, clean_session=True)
        self.client.username_pw_set(self.user_id, self.password)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.client.on_unsubscribe = self.on_unsubscribe
        self.client.on_subscribe = self.on_subscribe

        self.connect()
        self.publisher = publisher

    def connect(self):
        while self.rc != 0:
            try:
                self.rc = self.client.connect(self.host, self.port, self.keepalive)
            except:
                print "connection failed"
            time.sleep(2)
            self.timeout = self.timeout + 2

    def msg_process(self, msg):
        pass

    def looping(self, loop_timeout = .1):
        self.client.loop(loop_timeout)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.client.subscribe(self.mqtt_topic)
        self.timeout = 0

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            if not self.disconnect_flag:
                print "Unexpected disconnection."
                print "Trying reconnection"
                self.rc = rc
                self.connect()

    def on_message(self, client, userdata, msg):
        ros_msgs = self.msg_process(msg.payload)
        try:
            for ros_msg in ros_msgs:
                self.publisher.publish(ros_msg)
                time.sleep(.01)
        except TypeError:
            self.publisher.publish(ros_msgs)

    def unsubscribe(self):
        print " unsubscribing"
        self.client.unsubscribe(self.mqtt_topic)

    def disconnect(self):
        print " disconnecting"
        self.disconnect_flag = True
        self.client.disconnect()

    def on_unsubscribe(self, client, userdata, mid):
        print "Unsubscribed to " + self.mqtt_topic

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print "Subscribed to " + self.mqtt_topic

    def hook(self):
        self.unsubscribe()
        self.disconnect()
        print " shutting down"

    def get_timeout(self):
        return self.timeout