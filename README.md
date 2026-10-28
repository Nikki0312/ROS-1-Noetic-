# ROS 模拟遥测项目

本项目只生成、接收、记录和显示模拟数据，不连接真实飞控。

## 启动模拟与监听节点

打开终端执行：

source ~/catkin_ws/devel/setup.bash
roslaunch bf_ros_telemetry simulation.launch

roslaunch 会在需要时自动启动 ROS 主程序。

停止：在运行 roslaunch 的终端按 Ctrl+C。

## 模拟话题

- /bf_ros_telemetry/sim/status：模拟状态
- /bf_ros_telemetry/sim/voltage：电压，单位 V
- /bf_ros_telemetry/sim/attitude_rpy：姿态，单位弧度
  x 为横滚，y 为俯仰，z 为偏航

## 监听节点

收到电压时显示数值。
收到过数据后，连续超过 3 秒未收到电压时提示一次。
数据恢复后显示恢复提示。

## 回放已有数据

先停止模拟与监听节点，再分别启动：

终端一：
source ~/catkin_ws/devel/setup.bash
rosrun bf_ros_telemetry telemetry_monitor.py

终端二：
source ~/catkin_ws/devel/setup.bash
rosbag play ~/catkin_ws/bags/sim_telemetry_01.bag

回放需要有 roscore 运行，可在另一个终端启动。

## 已有录制文件

~/catkin_ws/bags/sim_telemetry_01.bag
## 电压检查与超时提示

- 拒绝负数、NaN 和无穷大。
- 异常值不会重置有效数据的等待时间。
- 启动后一直没有有效数据，也会触发超时提示。
- 每次中断只提示一次，收到有效数据后提示恢复。
- 默认超时时间为 3 秒。

统一启动，并设置超时时间为 5 秒：

source ~/catkin_ws/devel/setup.bash
roslaunch bf_ros_telemetry simulation.launch timeout_sec:=5.0

单独启动监听节点，并设置超时时间为 5 秒：

source ~/catkin_ws/devel/setup.bash
rosrun bf_ros_telemetry telemetry_monitor.py _timeout_sec:=5.0

已验证：正常接收、负数拒绝、启动无数据超时、
数据中断、有效数据恢复及启动参数设置。
