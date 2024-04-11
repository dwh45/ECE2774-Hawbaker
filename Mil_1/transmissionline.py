# Name: Daniel Hawbaker
# Last Edited: 7 MAR 2024
# Project: transmission line for milestone 1
# Class: ECE 2774

#Lengths of transmission lines
import numpy as np
from Conductor import conductor
import pandas as pd
from Bus import bus
from settings import s
from Generator import generator
#class TLineCode:
#    def __init__(self, r1, x1):
#        self.r1 = r1
#        self.x1 = x1

class tline:
    def __init__(self, name: str, busA: bus, busB: bus, length: float, conductor: conductor):
        self.name = name
        self.busA = busA
        self.busB = busB
        self.length = length
        self.conductor = conductor

        self.calc_RXB()
        self.y_matrix()
        #self.yprim = pd.DataFrame(np.zeros([2, 2], dtype=complex), dtype=complex, index=[self.busA.name, self.busB.name], columns=[self.busA.name, self.busB.name])
        #self.line_code = line_code #Tline has a tline code, illustrating aggregation

        #self.r1: float
        #self.x1: float

    def calc_RXB(self):
        zbase = self.busA.voltage ** 2 / s.s_mva
        ybase = 1 / zbase
        self.conductor.calc_params()
        self.Line_R = self.conductor.Rp*self.length #Line resistance
        self.Line_X = self.conductor.Xp*self.length #Line reactance
        self.Line_B = 1j*(self.conductor.Bp*self.length)/ybase #Shunt admittance

        self.Line_Z = (self.Line_R + 1j*self.Line_X) / (self.busA.voltage **2 / s.s_mva) #Line impedance
        self.Line_Y = 1/self.Line_Z #Line admittance



    def y_matrix(self):
        self.yprim = pd.DataFrame(np.zeros([2, 2], dtype=complex), dtype=complex, index=[self.busA.name, self.busB.name], columns=[self.busA.name, self.busB.name])
        self.yprim.loc[self.busA.name, self.busA.name] = self.yprim.loc[self.busB.name, self.busB.name] = self.Line_Y + self.Line_B/2
        self.yprim.loc[self.busA.name, self.busB.name] = self.yprim.loc[self.busB.name, self.busA.name] = -self.Line_Y

        #ytmat = np.array([[self.Line_Y + self.Line_B/2, -self.Line_Y],[-self.Line_Y, self.Line_Y + self.Line_B/2]])
        #print(self.name, 'TLine Y Matrix')
        #print(ytmat)

#need to ensure values are in pu