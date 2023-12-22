#!/usr/bin/env python3
import rospy
import tf

if __name__ == '__main__':
    rospy.init_node('map_to_odom_tf_broadcaster')

    listener = tf.TransformListener()
    broadcaster = tf.TransformBroadcaster()

    rate = rospy.Rate(10.0)

    while not rospy.is_shutdown():
        try:
            # Lắng nghe transform từ "map" tới "odom"
            (trans, rot) = listener.lookupTransform('/map', '/odom', rospy.Time(0))
            
            # Phát sóng transform này với frame_id là "map" và child_frame_id là "odom"
            broadcaster.sendTransform(trans, rot, rospy.Time.now(), '/odom', '/map')

        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        rate.sleep()

