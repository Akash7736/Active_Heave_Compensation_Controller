#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3

# Define constants
KP = 0.5 # Proportional gain
KD = 0.1 # Derivative gain

# Initialize global variables
heave_setpoint = 0.0
heave_error = 0.0
heave_error_prev = 0.0

# Define the callback function for the heave measurement message
def imu_callback(data):
    # Extract the heave measurement from the IMU message
    heave = data.linear_acceleration.z

    # Calculate the heave error
    global heave_error
    global heave_error_prev
    heave_error_prev = heave_error
    heave_error = heave_setpoint - heave

    # Calculate the PD controller output
    p = KP * heave_error
    d = KD * (heave_error - heave_error_prev)
    output = p + d

    # Publish the output as a motor command
    motor_command = Float32()
    motor_command.data = output
    motor_pub.publish(motor_command)

# Define the callback function for the heave setpoint message
def heave_callback(data):
    # Update the heave setpoint
    global heave_setpoint
    heave_setpoint = data.data

# Initialize the ROS node
rospy.init_node('active_heave_controller')

# Subscribe to the IMU topic
imu_sub = rospy.Subscriber('/imu/data', Imu, imu_callback)

# Subscribe to the heave setpoint topic
heave_sub = rospy.Subscriber('heave_setpoint', Float32, heave_callback)

# Publish the motor command topic
motor_pub = rospy.Publisher('motor_command', Float32, queue_size=1)

# Run the ROS node
rospy.spin()
