# Name: Daniel Hawbaker
# Last Edited: 29 FEB 2024
# Project: Milestone 1
# Class: ECE 2774
#can create a counter. Every time you create this class increment the counter by 1.
#can make it in the program so you cannot put in a negative number (For example, negative resistance input from user)

class bus:
    numbus = 0
    def __init__(self, name, voltage, bus_type, voltmag, angle):
        self.name = name
        self.voltage = voltage
        self.bus_type = bus_type
        self.voltmag = voltmag
        self.angle = angle
        self.bus_number = bus.numbus
        bus.numbus+=1


