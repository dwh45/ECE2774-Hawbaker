# Name: Daniel Hawbaker
# Last Edited: 07 MAR 2024
# Project: Milestone 1
# Class: ECE 2774

from Circuit import circuit
from transmissionline import tline
from Bus import bus
from transformer import Tx
from Conductor import conductor
from Geometry import geometry

SevenBus = circuit('SevenBus')
SevenBus.add_bus_element("Bus 1", 20)
SevenBus.add_bus_element("Bus 2", 230)
SevenBus.add_bus_element("Bus 3", 230)
SevenBus.add_bus_element("Bus 4", 230)
SevenBus.add_bus_element("Bus 5", 230)
SevenBus.add_bus_element("Bus 6", 230)
SevenBus.add_bus_element("Bus 7", 18)

SevenBus.add_transformer_element("T1", 10, 0.085, 230, "Bus 1", "Bus 2")
SevenBus.add_transformer_element("T2", 12, 0.105, 230, "Bus 6", "Bus 7")

SevenBus.add_geometry_element("GEOM", 19.5, 39, 19.5)

SevenBus.add_conductor_element("partridge", 0.0217, 1.5, 0.350, 2, 0.642, "GEOM")

SevenBus.add_transmissionline_element("L1", "Bus 2", "Bus 4", 10, "partridge")
SevenBus.add_transmissionline_element("L2", "Bus 2", "Bus 3", 25, "partridge")
SevenBus.add_transmissionline_element("L3", "Bus 3", "Bus 5", 20, "partridge")
SevenBus.add_transmissionline_element("L4", "Bus 4", "Bus 5", 20, "partridge")
SevenBus.add_transmissionline_element("L5", "Bus 5", "Bus 6", 10, "partridge")
SevenBus.add_transmissionline_element("L6", "Bus 4", "Bus 5", 35, "partridge")

SevenBus.make_ybus()
print(SevenBus.make_ybus())