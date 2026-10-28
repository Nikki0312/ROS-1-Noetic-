#!/usr/bin/env python3
import math
import time

import rospy
from std_msgs.msg import Float32


def main():
    rospy.init_node("telemetry_monitor")
    timeout_sec = float(rospy.get_param("~timeout_sec", 3.0))
    last_received = time.monotonic()
    timeout_reported = False

    def voltage_callback(message):
        nonlocal last_received, timeout_reported

        if not math.isfinite(message.data) or message.data < 0:
            rospy.logwarn(
                "Invalid simulated voltage: %s", message.data
            )
            return

        if timeout_reported:
            rospy.loginfo("Simulated voltage reception resumed.")

        last_received = time.monotonic()
        timeout_reported = False
        rospy.loginfo(
            "Received simulated voltage: %.2f V", message.data
        )

    subscriber = rospy.Subscriber(
        "/bf_ros_telemetry/sim/voltage",
        Float32,
        voltage_callback,
        queue_size=10
    )

    rospy.loginfo("Waiting for simulated voltage...")

    while not rospy.is_shutdown():
        if last_received is not None:
            if time.monotonic() - last_received > timeout_sec:
                if not timeout_reported:
                    rospy.logwarn(
                        "No valid simulated voltage received for over %.1f seconds.",
                        timeout_sec
                    )
                    timeout_reported = True

        time.sleep(0.1)


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
