#!/usr/bin/python
from mqtt_ros_bridge.msg import ImuPackage
from mqtt_ros_bridge.msg import Vector3Time
import bridge
import rospy
import signal

class imu_bridge_recordings(bridge.bridge):

    def msg_process(self, msg):
        msg_list = msg.split(";")
        
        pkgSizeAcc = int(msg_list[0])
        moduleSizeAcc = 4*pkgSizeAcc+2
        acc_msg = msg_list[2:moduleSizeAcc]

        pkgSizeGyro = int(msg_list[moduleSizeAcc])
        moduleSizeGyro = 4*pkgSizeGyro+2
        gyro_msg = msg_list[moduleSizeAcc+2:moduleSizeAcc+moduleSizeGyro]

        imu_data = ImuPackage()

        for i in range(0,pkgSizeAcc):
            acceleration = Vector3Time()
            acceleration.vector.x = float(acc_msg[3*i].replace(',','.'))
            acceleration.vector.y = float(acc_msg[3*i+1].replace(',','.'))
            acceleration.vector.z = float(acc_msg[3*i+2].replace(',','.'))

            acceleration.time.data = long(acc_msg[3*pkgSizeAcc+i])
            imu_data.linear_acceleration.append(acceleration)

        for i in range(0,pkgSizeGyro):
            velocity = Vector3Time()
            velocity.vector.x = float(gyro_msg[3*i].replace(',','.'))
            velocity.vector.y = float(gyro_msg[3*i+1].replace(',','.'))
            velocity.vector.z = float(gyro_msg[3*i+2].replace(',','.'))

            velocity.time.data = long(gyro_msg[3*pkgSizeGyro+i])
            imu_data.angular_velocity.append(velocity)

        return imu_data


def main():
    rospy.init_node('imu_bridge_recordings', anonymous=True)
    device = rospy.get_param('~device_name','sensors')
    mqtt_topic = device + '/imu'
    print mqtt_topic
    imu_publisher = rospy.Publisher('/imu_data', ImuPackage, queue_size=1)
    imu_sub = imu_bridge_recordings(imu_publisher, mqtt_topic, 'bridge_imu_'+ device)
    rospy.on_shutdown(imu_sub.hook)

    


    while not rospy.is_shutdown():
        imu_sub.looping()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
