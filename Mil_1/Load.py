# Name: Daniel Hawbaker
# Last Edited: 26 MAR 2024
# Project: Milestone 3
# Class: ECE 2774
from Bus import bus

class load:
    def __init__(self, name: str, realPWR: float, reactPWR: float, busA: bus):
        self.name = name
        self.realPWR = realPWR
        self.reactPWR = reactPWR
        self.busA = busA
        