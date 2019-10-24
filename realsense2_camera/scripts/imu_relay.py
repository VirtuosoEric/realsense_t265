#!/usr/bin/python
import rospy
import tf
import time
import sys
import math
from nav_msgs.msg import *
from sensor_msgs.msg import *


def filter(data):
    if -0.01 < data < 0.01:
        return 0.0
    else:
        return data 

def imu_relay(msg):
    imu_pub = rospy.Publisher('cam_imu',Imu,queue_size= 10)
    new_imu = Imu()
    new_imu.header.stamp = msg.header.stamp
    new_imu.header.frame_id = 'cam_imu_link'
    new_imu.linear_acceleration.x = filter(msg.linear_acceleration.z)
    new_imu.linear_acceleration.y = filter(msg.linear_acceleration.x)
    new_imu.linear_acceleration.z = filter(msg.linear_acceleration.y)
    # new_imu.linear_acceleration.z = 9.8

    new_imu.angular_velocity.x = filter(msg.angular_velocity.z)
    new_imu.angular_velocity.y = filter(msg.angular_velocity.x)
    new_imu.angular_velocity.z = filter(msg.angular_velocity.y)
    
    imu_pub.publish(new_imu)


if __name__ == "__main__":

    rospy.init_node('imu_relay', anonymous=False)
    rospy.Subscriber('/camera/imu',Imu,imu_relay)
    rospy.spin()
