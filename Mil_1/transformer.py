# Name: Daniel Hawbaker
# Last Edited: 29 FEB 2024
# Project: transformer for milestone 1
# Class: ECE 2774

import numpy as np
from settings import s

class Tx:
    def __init__(self, name, xr_ratio, z_percent, high_voltage, low_voltage, power_rating, busA, busB):
        self.name = name
        self.xr_ratio = xr_ratio
        self.z_percent = z_percent
        self.high_voltage = high_voltage
        self.low_voltage = low_voltage
        self.power_rating = power_rating
        self.busA = busA
        self.busB = busB

    def calc_admittance (self):
        zpuold = (self.z_percent / 100) * (np.exp(1j*np.arctan(self.xr_ratio)))
        zpusys = zpuold * ((self.low_voltage ** 2) / self.power_rating) / s.zbase
        self.R = np.real(zpusys)
        self.X = np.imag(zpusys)
        self.Z= self.R + 1j*self.X
        self.Y = 1/self.Z

    def y_matrix(self):
        ymat = np.array([[self.Y, -self.Y],[-self.Y, self.Y]])
        print(self.name, 'XFMR Y Matrix')
        print(ymat)

#Testing below
#if __name__ == '__main__':
#    T1=Tx('A',10, .085, 230, 20, 125, 1, 2)
#    T1.calc_admittance()
#    T1.y_matrix()