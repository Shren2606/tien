#!/usr/bin/env python3

import rospy
import yaml
from geometry_msgs.msg import Twist
import sys, select, os
if os.name == 'nt':
    import msvcrt
else:
    import tty, termios
    import tf
rospy.init_node('turtlebot3_teleop_keysave')

# Tạo một đối tượng của tf.TransformListener để lắng nghe và theo dõi biến đổi tọa độ
listener = tf.TransformListener()

# Chờ 1 giây để đảm bảo rằng tf listener đã được khởi tạo
rospy.sleep(1.0)

# Tên frame nguồn và frame đích
source_frame = "base_link"
target_frame = "map"

BURGER_MAX_LIN_VEL = 0.22
BURGER_MAX_ANG_VEL = 2.84

WAFFLE_MAX_LIN_VEL = 0.26
WAFFLE_MAX_ANG_VEL = 1.82

LIN_VEL_STEP_SIZE = 0.01
ANG_VEL_STEP_SIZE = 0.1

msg = """
Control Your TurtleBot3!
---------------------------
Moving around:
        w
   a    s    d
        x

w/x : increase/decrease linear velocity (Burger : ~ 0.22, Waffle and Waffle Pi : ~ 0.26)
a/d : increase/decrease angular velocity (Burger : ~ 2.84, Waffle and Waffle Pi : ~ 1.82)

space key, s : force stop

b : save current location

CTRL-C to quit
"""

e = """
Communications Failed
"""

def getKey():
    if os.name == 'nt':
        if sys.version_info[0] >= 3:
            return msvcrt.getch().decode()
        else:
            return msvcrt.getch()

    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def vels(target_linear_vel, target_angular_vel):
    return "currently:\tlinear vel %s\t angular vel %s " % (target_linear_vel, target_angular_vel)

def makeSimpleProfile(output, input, slop):
    if input > output:
        output = min(input, output + slop)
    elif input < output:
        output = max(input, output - slop)
    else:
        output = input

    return output

def constrain(input, low, high):
    if input < low:
        input = low
    elif input > high:
        input = high
    else:
        input = input

    return input

def checkLinearLimitVelocity(vel):
    if turtlebot3_model == "burger":
        vel = constrain(vel, -BURGER_MAX_LIN_VEL, BURGER_MAX_LIN_VEL)
    elif turtlebot3_model == "waffle" or turtlebot3_model == "waffle_pi":
        vel = constrain(vel, -WAFFLE_MAX_LIN_VEL, WAFFLE_MAX_LIN_VEL)
    else:
        vel = constrain(vel, -BURGER_MAX_LIN_VEL, BURGER_MAX_LIN_VEL)

    return vel

def checkAngularLimitVelocity(vel):
    if turtlebot3_model == "burger":
        vel = constrain(vel, -BURGER_MAX_ANG_VEL, BURGER_MAX_ANG_VEL)
    elif turtlebot3_model == "waffle" or turtlebot3_model == "waffle_pi":
        vel = constrain(vel, -WAFFLE_MAX_ANG_VEL, WAFFLE_MAX_ANG_VEL)
    else:
        vel = constrain(vel, -BURGER_MAX_ANG_VEL, BURGER_MAX_ANG_VEL)

    return vel

def get_location():
    try:
        (trans, rot) = listener.lookupTransform(target_frame, source_frame, rospy.Time(0))
        print(f"Transform from {source_frame} to {target_frame}")
        print(f"Translation: {trans}")
        print(f"Rotation: {rot}")
        return trans, rot
    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        rospy.logerr("Failed to lookup transform")
        return None, None

def save_location(waypoints, trans, rot):
    # Tự động tạo tên waypoint dựa trên số lượng waypoints đã có
    waypoint_name = f'waypoint{len(waypoints) + 1}'

    # Làm tròn giá trị tọa độ với 6 số sau dấu thập phân, và chuyển về kiểu float
    rounded_trans = [float(f"{coord:.4f}") for coord in trans]
    rounded_rot = [float(f"{coord:.4f}") for coord in rot]

    waypoints.append({
        'name': waypoint_name,
        'position': {'x': rounded_trans[0], 'y': rounded_trans[1], 'z': rounded_trans[2]},
        'orientation': {'w': rounded_rot[3], 'x': rounded_rot[0], 'y': rounded_rot[1], 'z': rounded_rot[2]}
    })

    # Tạo từ điển mới với khóa 'waypoints'
    yaml_data = {'waypoints': waypoints}

    with open('/home/vm/catkin_ws/src/auto_nav/scripts/waypoints.yaml', 'w') as file:
        yaml.dump(yaml_data, file, default_flow_style=False)  # Ghi từ điển mới

    print(f"Location saved as {waypoint_name}!")



if __name__=="__main__":
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

    turtlebot3_model = rospy.get_param("model", "burger")

    status = 0
    target_linear_vel = 0.0
    target_angular_vel = 0.0
    control_linear_vel = 0.0
    control_angular_vel = 0.0

    waypoints = []  # Danh sách lưu trữ waypoints

    try:
        print(msg)
        while(1):
            key = getKey()
            if key == 'w':
                target_linear_vel = checkLinearLimitVelocity(target_linear_vel + LIN_VEL_STEP_SIZE)
                status = status + 1
                print(vels(target_linear_vel, target_angular_vel))
            elif key == 'x':
                target_linear_vel = checkLinearLimitVelocity(target_linear_vel - LIN_VEL_STEP_SIZE)
                status = status + 1
                print(vels(target_linear_vel, target_angular_vel))
            elif key == 'a':
                target_angular_vel = checkAngularLimitVelocity(target_angular_vel + ANG_VEL_STEP_SIZE)
                status = status + 1
                print(vels(target_linear_vel, target_angular_vel))
            elif key == 'd':
                target_angular_vel = checkAngularLimitVelocity(target_angular_vel - ANG_VEL_STEP_SIZE)
                status = status + 1
                print(vels(target_linear_vel, target_angular_vel))
            elif key == ' ' or key == 's':
                target_linear_vel = 0.0
                control_linear_vel = 0.0
                target_angular_vel = 0.0
                control_angular_vel = 0.0
                print(vels(target_linear_vel, target_angular_vel))
            elif key == 'b':
                trans, rot = get_location()
                if trans is not None and rot is not None:
                    save_location(waypoints, trans, rot)
            else:
                if key == '\x03':
                    break

            if status == 20:
                print(msg)
                status = 0

            twist = Twist()

            control_linear_vel = makeSimpleProfile(control_linear_vel, target_linear_vel, (LIN_VEL_STEP_SIZE / 2.0))
            twist.linear.x = control_linear_vel; twist.linear.y = 0.0; twist.linear.z = 0.0

            control_angular_vel = makeSimpleProfile(control_angular_vel, target_angular_vel, (ANG_VEL_STEP_SIZE / 2.0))
            twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = control_angular_vel

            pub.publish(twist)

    except Exception as ex:
        print(ex)

    finally:
        twist = Twist()
        twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        pub.publish(twist)

    if os.name != 'nt':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

