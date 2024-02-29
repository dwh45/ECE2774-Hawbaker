# Name: Daniel Hawbaker
# Last Edited: 27 FEB 2024
# Project: Milestone 1
# Class: ECE 2774
import numpy as np
from settings import s

class conductor:
    def __init__(self, name, GMR, spacing, Rc, bundles, diameter):
        self.name = name
        self.GMR = GMR
        self.d = spacing
        self.Rc = Rc
        self.n = bundles
        self.r = 0.5*diameter/12

    def calc_params(self):
        Deq = np.cbrt(self.d * self.d * (np.sqrt(self.d ** 2 + self.d ** 2)))
        if self.n == 1:
            self.Rp = self.Rc
            DSL = self.GMR
            DSC = self.r
        elif self.n == 2:
            self.Rp = self.Rc/2
            DSL = np.sqrt(self.d * self.GMR)
            DSC = np.sqrt(self.d * self.r)
        elif self.n == 3:
            self.Rp = self.Rc/3
            DSL = np.cbrt(self.d ** 2 * self.GMR)
            DSC = np.cbrt(self.d ** 2 * self.r)
        elif self.n == 4:
            self.Rp = self.Rc/4
            DSL = 1.091 * ((self.d ** 3 * self.GMR) ** (1 / 4))
            DSC = 1.091 * ((self.d ** 3 * self.r) ** (1 / 4))
        else:
            print("invalid bundle entry. Setting n to 1")
            self.n: int = 1
        self.Xp = (s.f*2*np.pi)*(2e-7)*np.log(Deq/DSL)*1609  #Calc reactance
        self.Bp = (s.f*2*np.pi)*((2*np.pi*8.854e-12)/(np.log(Deq/DSC)))*1609 #Calc susceptance (shunt)



