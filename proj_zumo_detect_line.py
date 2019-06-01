#!/usr/bin/env python

import rospy
from std_msgs.msg import Int8
from geometry_msgs.msg import Twist
from std_msgs.msg import Int8

import time
import sys
import os

rospy.init_node('proj_zumo_detect_line', anonymous=True)
pub = rospy.Publisher('/zumo/2/cmd_vel', Twist, queue_size=10)
current_topic = 0
new_topic = 1

def right():
    vel_msg = Twist()
    vel_msg.linear.x = 0
    vel_msg.linear.y = -0.5
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0
    #vel_msg.linear.x = 0
    pub.publish(vel_msg)

def left():
    vel_msg = Twist()
    vel_msg.linear.x = 0
    vel_msg.linear.y = 0.5
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0
    #vel_msg.linear.x = 0
    pub.publish(vel_msg)

def stop():
    vel_msg = Twist()
    vel_msg.linear.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0
    vel_msg.linear.x = 0
    pub.publish(vel_msg)

def handle_zumo_line_sensor_right(line_msg):


        # if the line is on the right turn left

    global current_topic

    if(line_msg.data > 7):
        new_topic = 2
        left()
    else:
        new_topic = 1

    if(current_topic ==1 and new_topic == 2):
        os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/2/cmd_vel")
        current_topic = 2
    if(current_topic ==2 and new_topic == 1):
        os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/1/cmd_vel")
        current_topic = 1

def handle_zumo_line_sensor_left(line_msg):



    # if the line is on the left turn right

    global current_topic

    if(line_msg.data > 7):
        new_topic = 2
        right()
    else:
        new_topic = 1

    if(current_topic ==1 and new_topic == 2):
        os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/2/cmd_vel")
        current_topic = 2
    if(current_topic ==2 and new_topic == 1):
        os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/1/cmd_vel")
        current_topic = 1


rospy.Subscriber('/zumo/line_left', Int8, handle_zumo_line_sensor_right)            #left line turn right
rospy.Subscriber('/zumo/line_right', Int8, handle_zumo_line_sensor_left)            #right line turn left

#take over
os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/1/cmd_vel")
current_topic = 1
rospy.spin()



