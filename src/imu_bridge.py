#!/usr/bin/python

from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3
import bridge
import rospy
import signal

class imu_bridge(bridge.bridge):

    def msg_process(self, msg):
        msg_list = msg.split(";")

        acceleration = Vector3()
        acceleration.x = float(msg_list[1].replace(',','.'))
        acceleration.y = float(msg_list[2].replace(',','.'))
        acceleration.z = float(msg_list[3].replace(',','.'))

        velocity = Vector3()
        velocity.x = float(msg_list[5].replace(',','.'))
        velocity.y = float(msg_list[6].replace(',','.'))
        velocity.z = float(msg_list[7].replace(',','.'))

        imu_message = Imu()
        now = rospy.get_rostime()
        imu_message.header.stamp.secs = now.secs
        imu_message.header.stamp.nsecs = now.nsecs
        imu_message.header.frame_id = "0"
        imu_message.linear_acceleration = acceleration
        imu_message.angular_velocity = velocity

        return imu_message


def main():
    rospy.init_node('imu_bridge', anonymous=True)
    device = rospy.get_param(rospy.get_name()+'/device_name','sensors')
    mqtt_topic = device + '/imu'
    print mqtt_topic
    imu_publisher = rospy.Publisher('/imu_data', Imu, queue_size=1)
    imu_sub = imu_bridge(imu_publisher, mqtt_topic, 'bridge_imu_'+ device)
    rospy.on_shutdown(imu_sub.hook)

    


    while not rospy.is_shutdown():
        imu_sub.looping()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
