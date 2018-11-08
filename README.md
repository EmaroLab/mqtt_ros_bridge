# MQTT ROS Bridge

This Bridge allows to subscribe to MQTT topics and publish contents of MQTT messages to ROS. It is not yet possible to pulish to MQTT from ROS.

## Installation

Clone the repository in the source folder of your catkin workspace.

```bash
git clone https://github.com/EmaroLab/mqtt_ros_bridge.git
```

## Dependencies

In order to succesfully run the code, you should have installed [paho-mqtt](https://pypi.python.org/pypi/paho-mqtt/1.1) and [ROS](http://wiki.ros.org/kinetic/Installation/Ubuntu).

## MQTT Broker

The suggested MQTT Broker is [Mosquitto](https://mosquitto.org/documentation/). In order to install Mosquitto on Ubuntu follow [this guide](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-the-mosquitto-mqtt-messaging-broker-on-ubuntu-16-04).

## Test

In order to test the code:

1. Check the Mosquitto broker status, if the broker is already active skip step 2.
    ```bash
    sudo service mosquitto status
    ```
1. Start the Mosquitto broker.
    ```bash
    mosquitto
    ```
1. In a new terminal tab launch the _imu_bridge_.
    ```bash
    roslaunch mqtt_ros_bridge imu_bridge.launch
    ```
1. In a new terminal tab check the ROS topip _/inertial_, nothing should appear.
    ```bash
    rostopic echo /inertial
    ```
1. In a new terminal tab publish a _sensors/imu_ message to the local Mosquitto broker.
    ```bash
    mosquitto_pub -h localhost -t "sensors/imu" -m "acc;9.8;-0.3;0.5;vel;0.1;0.12;-0.4"
    ```
    In the terminal open at step 4 should appear the message received by the ROS master.

## How to use _mqtt_ros_bridge_

The _imu_brdige_ node is an example of how to use the bridge, summing up:

1. Import _bridge.py_
1. Create a class _example_brigde_ that inherit from the bridge class.
    ```python
    class example_bridge(bridge.bridge):
    ```
1. Implement the _msg_process_ function to map MQTT message to ROS message.
1. Initialize the bridge and call the _loop_ function in a ROS while loop.

## Author

[Alessandro Carfì](https://github.com/ACarfi) e-mail: alessandro.carfi@dibris.unige.it