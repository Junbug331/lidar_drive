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
    

def drive_stop():
    global motor_msg, pub
    motor_msg.speed = 0
    motor_msg.angle = 0
    pub.publish(motor_msg)

rospy.init_node('lidar_driver')
rospy.Subscriber('/scan', LaserScan, callback, queue_size=1)
pub = rospy.Publisher('xycar_motor', xycar_motor, queue_size=1)

time.sleep(3)

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
            print('stop')
            drive_stop()

    if ok <= 3:
        print('drive')
        #drive_go()
        drive_stop()
    time.sleep(1)