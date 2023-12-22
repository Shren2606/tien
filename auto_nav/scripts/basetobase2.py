#!/usr/bin/env python3

import rospy
import tf

if __name__ == '__main__':
    rospy.init_node('odom_to_base_footprint_tf_broadcaster')

    listener = tf.TransformListener()
    broadcaster = tf.TransformBroadcaster()

    rate = rospy.Rate(10.0)

    while not rospy.is_shutdown():
        try:
            # Lắng nghe transform từ "odom" tới "base_footprint"
            (trans, rot) = listener.lookupTransform('/odom', '/base_footprint', rospy.Time(0))
            
            # Phát sóng transform này với frame_id là "odom" và child_frame_id là "base_footprint"
            broadcaster.sendTransform(trans, rot, rospy.Time.now(), '/base_footprint', '/odom')

        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        rate.sleep()

