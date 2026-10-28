#!/usr/bin/env python3
import math
import time

import rospy
from geometry_msgs.msg import Vector3
from std_msgs.msg import Float32, String


def main():
    rospy.init_node("sim_telemetry", anonymous=False)

    status_pub = rospy.Publisher(
        "/bf_ros_telemetry/sim/status", String, queue_size=10
    )
    voltage_pub = rospy.Publisher(
        "/bf_ros_telemetry/sim/voltage", Float32, queue_size=10
    )
    attitude_pub = rospy.Publisher(
        "/bf_ros_telemetry/sim/attitude_rpy", Vector3, queue_size=10
    )

    rate = rospy.Rate(1)
    start = time.monotonic()

    while not rospy.is_shutdown():
        elapsed = time.monotonic() - start
        voltage = 15.2 + 0.1 * math.sin(elapsed)

        attitude = Vector3()
        attitude.x = 0.1 * math.sin(elapsed)
        attitude.y = 0.05 * math.cos(elapsed)
        attitude.z = 0.0

        status_pub.publish(
            "SIMULATION ONLY: armed=false, link=simulated"
        )
        voltage_pub.publish(Float32(data=voltage))
        attitude_pub.publish(attitude)

        rospy.loginfo(
            "SIM: %.2f V, roll=%.3f pitch=%.3f yaw=%.3f rad",
            voltage, attitude.x, attitude.y, attitude.z
        )
        rate.sleep()


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
