# Name: Daniel Hawbaker
# Last Edited: 29 FEB 2024
# Project: Milestone 1
# Class: ECE 2774


from transmissionline import tline
from Bus import bus
from transformer import Tx
from Conductor import conductor
from Geometry import geometry

bus1=bus('Bus1', 20)
bus2=bus('Bus2', 230)
geom=geometry(19.5, 39, 19.5)
cond = conductor('Partridge', 0.0217, 1.5, 0.350, 2, 0.642, geom)
L1=tline('Line 1', 2, 4, 10, cond)
L1.calc_RXB()
L1.y_matrix()
T1=Tx('T1',10, .085, 230, 20, 125, 1, 2)
T1.calc_admittance()
T1.y_matrix()
print(bus.numbus)

# in main. Use sevenbus = circuit('') creates the circuit
# sevenbus.add_bus_element ("Bus2", 230)  adds a bus with the amount of KV

# sevenbus.add_transformer_element("T1", "Bus 1", "Bus 2", 125, 8.5, 10)


# in the main keep adding all the elements in this way Transformer, Conductor, Buses, etc.
