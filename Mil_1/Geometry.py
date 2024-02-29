# Name: Daniel Hawbaker
# Last Edited: 27 FEB 2024
# Project: Milestone 1
# Class: ECE 2774
import numpy as np
from settings import s

zpuold = 0.085 / 100 * np.exp(1j * np.arctan(10))

zpusys = zpuold * ((20 ** 2) / 125) / s.zbase
R = np.real(zpusys)

X = np.imag(zpusys)

Z = R + 1j * X
Y = 1 / Z
print(Y)