#!/usr/bin/env python

## Simple talker demo that published std_msgs/Strings messages
## to the 'chatter' topic

import rospy
from manager.msg import GeneralPurposeCmd

def talker():
    pub = rospy.Publisher('chatter', GeneralPurposeCmd, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    while 1:
        generalPurposeCmd = GeneralPurposeCmd()
        generalPurposeCmd.Person = raw_input("Person? ")
        instruction = raw_input("Instruction? ")
        generalPurposeCmd.Instruction = instruction
        location = raw_input("Location? ")
        generalPurposeCmd.Location = location
        type1 = raw_input("Type? ")
        generalPurposeCmd.Type = type1
        time = raw_input("Time? ")
        generalPurposeCmd.Time = time
        pub = rospy.Publisher('publication', GeneralPurposeCmd, queue_size=10)
        pub.publish(generalPurposeCmd)

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
