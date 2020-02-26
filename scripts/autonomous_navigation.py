#!/usr/bin/env python3
import rospy
import numpy as np
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


global object_loc
global distance_value
distance_value = None
object_loc = None

def laserCallback(data):
	global distance_value
	global object_loc
	ranges = np.array(data.ranges)
	distance_value = min(ranges)
	distance_place = np.where(ranges==distance_value)
	if distance_place[0] >150 and distance_place[0] <=550 and distance_value < 2.0:
		object_loc = True
	else:
		object_loc = False

def Navigate(object_loc, pub):
	twist = Twist()  
	if object_loc == True:
		twist.linear.x = 0.0
		twist.angular.z = 2.0
		print("Obstacle Found, turning away")

	elif object_loc == False:
		twist.linear.x = 0.3
		twist.angular.z = 0.0
		print("No Obstacle Found, Moving Forward")

	else:
		twist.linear.x = 0.0
		twist.angular.z = 0.0

	pub.publish(twist)

if __name__ == "__main__":
	rospy.init_node("obstacle_avoidance")
	pub = rospy.Publisher('cmd_vel', Twist, queue_size=20)
	sub = rospy.Subscriber('scan',LaserScan,laserCallback)
	while not rospy.is_shutdown():
		Navigate(object_loc,pub)
	rospy.spin()

