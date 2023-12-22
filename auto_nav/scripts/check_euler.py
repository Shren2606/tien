#!/usr/bin/env python3
import rospy
import tf
from tf.transformations import euler_from_quaternion

if __name__ == '__main__':
    rospy.init_node('transform_lookup_example')
    listener = tf.TransformListener()
    rospy.sleep(1.0)

    source_frame = "base_link"
    target_frame = "map"

    try:
        (trans, rot) = listener.lookupTransform(target_frame, source_frame, rospy.Time(0))

        # Chuyển đổi từ quaternion sang Euler
        euler_angles = euler_from_quaternion(rot)

        # In thông tin về tịnh tiến và xoay dưới dạng Euler
        print(f"Transform from {source_frame} to {target_frame}")
        print(f"Translation: {trans}")
        print(f"Euler Angles (Yaw, Pitch, Roll): {euler_angles}")

    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        rospy.logerr("Failed to lookup transform")

    rospy.spin()



