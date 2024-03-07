# Name: Daniel Hawbaker
# Last Edited: 7 MAR 2024
# Project: Milestone 1
# Class: ECE 2774

import numpy as np

class geometry:
    def __init__(self,name, Dab, Dac, Dbc):
        self.name = name
        self.Dab = Dab
        self.Dac = Dac
        self.Dbc = Dbc
        self.calc_deq()
    def calc_deq(self):
        self.Deq = np.cbrt(self.Dab + self.Dbc + self.Dac)

