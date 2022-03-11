#!/usr/bin/env python
import rospy, time
from sensor_msgs.msg import LaserScan
from xycar_msgs.msg import xycar_motor

motor_msg = xycar_motor()
distance = []

def callback(data):
    global distance, motor_msg
    distance = data.ranges


def drive_go():
    global motor_msg, pub
    motor_msg.speed = 5
    motor_msg.angle = 0
    pub.publish(motor_msg)

def drive_back():
    global motor_msg, pub
    motor_msg.speed = -5
    motor_msg.angle = 0
    pub.publish(motor_msg)

def drive_right():
    global motor_msg, pub
    xycar_motor = 5 
    motor_msg.angle = 30
    

def drive_stop():
    global motor_msg, pub
    motor_msg.speed = 0
    motor_msg.angle = 0
    pub.publish(motor_msg)

rospy.init_node('lidar_driver')
rospy.Subscriber('/scan', LaserScan, callback, queue_size=1)
pub = rospy.Publisher('xycar_motor', xycar_motor, queue_size=1)

time.sleep(3)
detected = False

while not rospy.is_shutdown():
    # obstacle in front
    # front angle is 90 degree
    ok = 0
    distance = distance[:42] + distance[403:]
    print(distance)
    for dis in distance:
        if  dis > 0.0 and dis <= 0.3:
            ok += 1 

    if ok > 3:
        detected = True
        for _ in range(20):
            drive_back()
            time.sleep(0.1)

    if detected and ok <= 3:
        detected = False
        for _ in range(20):
            drive_right()
            time.sleep(0.1)

    if not detected and ok <= 3:
        drive_go()
        #drive_stop()