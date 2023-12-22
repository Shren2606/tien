#!/usr/bin/env python3

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

# Callbacks definition

def active_cb(extra):
    rospy.loginfo("Value of 'extra': {}".format(extra))
    rospy.loginfo("Goal pose being processed")

def feedback_cb(feedback):
    rospy.loginfo("Current location: "+str(feedback))

def done_cb(status, result):
    if status == 3:
        rospy.loginfo("da toi vi tri 1, dung lai trong 5 giay truoc khi chuyen den vi tri 2")
        rospy.sleep(5.0)
        send_next_goal()
        
    if status == 2 or status == 8:
        rospy.loginfo("Goal cancelled")
    if status == 4:
        rospy.loginfo("Goal aborted")

def send_next_goal():
    next_goal = MoveBaseGoal()
    next_goal.target_pose.header.frame_id = "map"
    next_goal.target_pose.header.stamp = rospy.Time.now()
    next_goal.target_pose.pose.position.x = -1.880993
    next_goal.target_pose.pose.position.y = 0.339186
    next_goal.target_pose.pose.position.z = 0.010025
    next_goal.target_pose.pose.orientation.x = 0.0
    next_goal.target_pose.pose.orientation.y = 0.0
    next_goal.target_pose.pose.orientation.z = 0.898858
    next_goal.target_pose.pose.orientation.w = 0.00013
    
    rospy.loginfo("da toi vi tri 2")
    navclient.send_goal(next_goal, done_cb, active_cb, feedback_cb)   

rospy.init_node('goal_pose')

navclient = actionlib.SimpleActionClient('move_base', MoveBaseAction)
navclient.wait_for_server()

# Example of navigation goal
goal = MoveBaseGoal()
goal.target_pose.header.frame_id = "map"
goal.target_pose.header.stamp = rospy.Time.now()

goal.target_pose.pose.position.x = 2.16
goal.target_pose.pose.position.y = 0.764
goal.target_pose.pose.position.z = 0.0
goal.target_pose.pose.orientation.x = 0.0
goal.target_pose.pose.orientation.y = 0.0
goal.target_pose.pose.orientation.z = 0.662
goal.target_pose.pose.orientation.w = 0.750

navclient.send_goal(goal, done_cb, active_cb, feedback_cb)
navclient.wait_for_result()

rospy.spin()  # Keep the script running

