#!/usr/bin/env python

import rospy
from bottle import route, run, template, request
from std_msgs.msg import Int8
from geometry_msgs.msg import Twist
from std_msgs.msg import Int8

import time
import sys
import os


IP_ADDRESS = '127.0.1.1' # my Pi

rospy.init_node('proj_zumo_web', anonymous=True)
pub = rospy.Publisher('/zumo/1/cmd_vel', Twist, queue_size=10)

def move_forward(msg):
    vel_msg = Twist()
    vel_msg.linear.x = 0
    vel_msg.linear.y = 0                    #forward
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0
    vel_msg.linear.x = 1
    pub.publish(vel_msg)
    time.sleep(0.1)


def stop():
    vel_msg = Twist()
    vel_msg.linear.x = 0
    vel_msg.linear.y = 0                    #stop
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0
    vel_msg.linear.x = 0
    pub.publish(vel_msg)



def right():
    vel_msg = Twist()
    vel_msg.linear.x = 0
    vel_msg.linear.y = -1            #right
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0
    vel_msg.linear.x = 0
    pub.publish(vel_msg)


def left():
    vel_msg = Twist()
    vel_msg.linear.x = 0
    vel_msg.linear.y = 1            #left
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0
    vel_msg.linear.x = 0
    pub.publish(vel_msg)


def reverse():
    vel_msg = Twist()
    vel_msg.linear.x = 0
    vel_msg.linear.y = 0            #reverse
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0
    vel_msg.linear.x = -1
    pub.publish(vel_msg)


def index():
        cmd = request.GET.get('command', '')
        if cmd == 'f':
            rospy.Subscriber('/zumo/line_left', Int8, move_forward)
        elif cmd == 'l':
            rospy.Subscriber('/zumo/line_left', Int8, left)
        elif cmd == 's':
            rospy.Subscriber('/zumo/line_left', Int8, stop)
        elif cmd == 'r':
            rospy.Subscriber('/zumo/line_left', Int8, right)
        elif cmd == 'b':
            rospy.Subscriber('/zumo/line_left', Int8, reverse)
        return template('home.tpl')

# Start the webserver running on port 80
try:
    run(host=IP_ADDRESS, port=80)
finally:
    rr.cleanup()
