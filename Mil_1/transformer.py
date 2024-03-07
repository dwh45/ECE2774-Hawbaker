# Name: Daniel Hawbaker
# Last Edited: 7 MAR 2024
# Project: transformer for milestone 1
# Class: ECE 2774

import numpy as np
from settings import s
import pandas as pd
from Bus import bus

class Tx:
    def __init__(self, name, xr_ratio, z_percent, power_rating, busA: bus, busB: bus):
        self.name = name
        self.xr_ratio = xr_ratio
        self.z_percent = z_percent
        #self.high_voltage = high_voltage
        #self.low_voltage = low_voltage
        self.power_rating = power_rating
        self.busA = busA
        self.busB = busB

        self.ztx: complex
        self.ytx: complex
        self.calc_admittance()
        self.y_matrix()

    def calc_admittance (self):
       # zpuold = (self.z_percent / 100) * (np.exp(1j*np.arctan(self.xr_ratio)))
        #zpusys = zpuold * ((self.low_voltage ** 2) / self.power_rating) / s.zbase
        zpusys = self.z_percent * (np.exp(1j*np.arctan(self.xr_ratio))) * s.s_mva / self.power_rating
        self.R = np.real(zpusys)
        self.X = np.imag(zpusys)
        self.Z= self.R + 1j*self.X
        self.Y = 1/self.Z

    def y_matrix(self):
        self.yprim = pd.DataFrame(np.zeros([2, 2], dtype=complex), dtype=complex, index=[self.busA.name, self.busB.name], columns=[self.busA.name, self.busB.name])
        self.yprim.loc[self.busA.name, self.busA.name] = self.yprim.loc[self.busB.name, self.busB.name] = self.Y
        self.yprim.loc[self.busA.name, self.busB.name] = self.yprim.loc[self.busB.name, self.busA.name] = -self.Y
        #ymat = np.array([[self.Y, -self.Y],[-self.Y, self.Y]])
        #print(self.name, 'XFMR Y Matrix')
        #print(ymat)

#Testing below
#if __name__ == '__main__':
#    T1=Tx('A',10, .085, 230, "Bus 1", "Bus 2")
#    T1.calc_admittance()
#    T1.y_matrix()

#Dr. Kereste way
#self.zt: complex
#self.yt: complex
#self.ypri = pd.DataFrame(np.zeros((2,2), dtype=complex), dtype=complex, index = [self.bus1.name, self.bus2.name], columns=[self.bus1.name, self.bus2.name
#had this prior to calc impedence and under __init__

#zt = self.impedence_percent * s.mva_base / self.power_rating*exp(1j*np.arctan(self.xr_Ratio