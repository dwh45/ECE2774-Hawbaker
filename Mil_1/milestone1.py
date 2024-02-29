# Name: Daniel Hawbaker
# Last Edited: 13 FEB 2024
# Project: Milestone 1
# Class: ECE 2774


from transmissionline import tline
from Bus import bus
from transformer import Tx
from Conductor import conductor



cond = conductor('Partridge', 0.0217, 1.5, 0.350, 2, 0.642)
L1=tline('Line 1', 2, 4, 10, cond)
L1.calc_RXB()
L1.y_matrix()
T1=Tx('T1',10, .085, 230, 20, 125, 1, 2)
T1.calc_admittance()
T1.y_matrix()


