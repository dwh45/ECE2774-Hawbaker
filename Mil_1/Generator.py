# Name: Daniel Hawbaker
# Last Edited: 26 MAR 2024
# Project: Milestone 3
# Class: ECE 2774

from Bus import bus

class generator:
    def __init__(self, name: str, busA: bus, realPWR: float, reactPWR: float, genX1: float, genX2: float, genX0: float):
        self.name = name
        self.busA= busA
        self.realPWR = realPWR
        self.reactPWR = reactPWR
        self.genX1 = genX1
        self.genX1 = genX2
        self.genX0 = genX0