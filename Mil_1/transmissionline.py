# Name: Daniel Hawbaker
# Last Edited: 27 FEB 2024
# Project: transmission line for milestone 1
# Class: ECE 2774

#Lengths of transmission lines
import numpy as np
from Conductor import conductor
#class TLineCode:
#    def __init__(self, r1, x1):
#        self.r1 = r1
#        self.x1 = x1

class tline:
    def __init__(self,
                 name: str,
                 busA: str,
                 busB: str,
                 length: float,
                 conductor: conductor
                 #line_code: TLineCode
                 ):
        self.name = name
        self.busA = busA
        self.busB = busB
        self.length = length
        self.conductor = conductor
        #self.line_code = line_code #Tline has a tline code, illustrating aggregation

        #self.r1: float
        #self.x1: float

    def calc_RXB(self):
        self.conductor.calc_params()
        self.Line_R = self.conductor.Rp*self.length
        self.Line_X = self.conductor.Xp*self.length
        self.Line_B = self.conductor.Bp*self.length
        self.Line_Z = self.Line_R + 1j*self.Line_X
        self.Line_Y = 1/self.Line_Z

    def y_matrix(self):
        ytmat = np.array([[self.Line_Y + self.Line_B/2, -self.Line_Y],[-self.Line_Y, self.Line_Y + self.Line_B/2]])
        print(self.name, 'TLine Y Matrix')
        print(ytmat)

