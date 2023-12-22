#!/usr/bin/env python3
import rospy
import tf

if __name__ == '__main__':
    # Khởi tạo node ROS với tên 'transform_lookup_example'
    rospy.init_node('transform_lookup_example')

    # Tạo một đối tượng của tf.TransformListener để lắng nghe và theo dõi biến đổi tọa độ
    listener = tf.TransformListener()

    # Chờ 1 giây để đảm bảo rằng tf listener đã được khởi tạo
    rospy.sleep(1.0)

    # Tên frame nguồn và frame đích
    source_frame = "base_link"
    target_frame = "map"

    try:
        # Sử dụng lookupTransform để lấy thông tin biến đổi giữa frame 'target_frame' và 'source_frame'
        # Thời điểm sử dụng rospy.Time(0) để lấy thông tin gần nhất có sẵn
        (trans, rot) = listener.lookupTransform(target_frame, source_frame, rospy.Time(0))

        # In thông tin về tịnh tiến và xoay
        print(f"Transform from {source_frame} to {target_frame}")
        print(f"Translation: {trans}")
        print(f"Rotation: {rot}")

    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        # Xử lý các ngoại lệ có thể xảy ra khi lấy thông tin biến đổi
        rospy.logerr("Failed to lookup transform")

    # Tiếp tục chạy node ROS
    rospy.spin()

