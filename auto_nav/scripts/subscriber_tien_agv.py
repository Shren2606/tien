#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Vector3Stamped

# Callback function
def callback(msg):
    print("Received message: {}".format(msg))

# Node and subscriber initialization
rospy.init_node("subscriber")
rospy.Subscriber("speed", Vector3Stamped, callback)

# Spinning
rospy.spin()

