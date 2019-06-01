#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from std_msgs.msg import Int8

import time
import sys




class joy_receiver:
    def __init__(self):
        self.pub = rospy.Publisher('/zumo/1/cmd_vel', Twist, queue_size=10)
        rospy.Subscriber('joy', Joy, self.callback)
        rospy.init_node('joy_receiver')
        rospy.spin()

    def callback(self, data):
        twist = Twist()
        twist.linear.x = 4 * data.axes[1]
        twist.angular.z = 4 * data.axes[0]
        self.pub.publish(twist)


if __name__ == '__main__':
        try:
            joy_receiver()
        except rospy.ROSInterruptException:
            pass
        rospy.spin()