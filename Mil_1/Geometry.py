# Name: Daniel Hawbaker
# Last Edited: 29 FEB 2024
# Project: Milestone 1
# Class: ECE 2774

import numpy as np

class geometry:
    def __init__(self, Dab, Dac, Dbc):
        self.Dab = Dab
        self.Dac = Dac
        self.Dbc = Dbc
        self.Deq = np.cbrt(self.Dab + self.Dbc + self.Dac)

