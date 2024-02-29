# Name: Daniel Hawbaker
# Last Edited: 29 FEB 2024
# Project: settings for milestone 1
# Class: ECE 2774

class settings:
        def __init__(self):

            self._S_mva = 100
            self._f = 60
            self.vbase = 20
            self.zbase = self.vbase ** 2 / self._S_mva
        @property
        def s_mva(self):
            return self._S_mva

        @property
        def f(self):
            return self._f

        @f.setter
        def f(self, value):
            if value in [50, 60]:
                self._f = value
            else:
                raise ValueError(f"you need to define 50hz or 60hz")

        def calc_zbase (self):
            self.zbase = self.vbase**2/self._S_mva
            return self.zbase
        def calc_ybase(self):
            ybase = 1/self.zbase
            return ybase

s = settings()