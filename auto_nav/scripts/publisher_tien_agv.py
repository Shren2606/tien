#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
rospy.init_node("publisher_node")
pub = rospy.Publisher("cmd_vel", Twist, queue_size=1)

# Looping
while not rospy.is_shutdown():
    # Create a Twist message
    twist_msg = Twist()

    # Set linear and angular values
    twist_msg.linear.x = 4000  # Replace 0.1 with your desired linear velocity
    twist_msg.angular.z = 0  # Replace 0.2 with your desired angular velocity

    # Publish the Twist message
    pub.publish(twist_msg)

    # Sleep for 1 second
    rospy.sleep(1)

