#!/usr/bin/env python3

import rospy
import tf

if __name__ == '__main__':
    rospy.init_node('base_footprint_to_base_link_tf_broadcaster')

    listener = tf.TransformListener()
    broadcaster = tf.TransformBroadcaster()

    rate = rospy.Rate(10.0)

    while not rospy.is_shutdown():
        try:
            # Lắng nghe transform từ "base_footprint" tới "base_link"
            (trans, rot) = listener.lookupTransform('/base_footprint', '/base_link', rospy.Time(0))
            
            # Phát sóng transform này với frame_id là "base_footprint" và child_frame_id là "base_link"
            broadcaster.sendTransform(trans, rot, rospy.Time.now(), '/base_link', '/base_footprint')

        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        rate.sleep()

