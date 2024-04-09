# Name: Daniel Hawbaker
# Last Edited: 26 MAR 2024
# Project: Milestone 3
# Class: ECE 2774

from Circuit import circuit
from transmissionline import tline
from Bus import bus
from transformer import Tx
from Conductor import conductor
from Geometry import geometry

SevenBus = circuit('SevenBus')
SevenBus.add_bus_element("Bus 1", 20, "slack", 1.0, 0)
SevenBus.add_bus_element("Bus 2", 230, "PQ", 1.0, 0)
SevenBus.add_bus_element("Bus 3", 230, "PQ", 1.0, 0)
SevenBus.add_bus_element("Bus 4", 230, "PQ", 1.0, 0)
SevenBus.add_bus_element("Bus 5", 230, "PQ", 1.0, 0)
SevenBus.add_bus_element("Bus 6", 230, "PQ", 1.0, 0)
SevenBus.add_bus_element("Bus 7", 18, "PV", 1.0, 0)

SevenBus.add_transformer_element("T1", 10, 0.085, 125, "Bus 1", "Bus 2")
SevenBus.add_transformer_element("T2", 12, 0.105, 200, "Bus 6", "Bus 7")

SevenBus.add_geometry_element("GEOM", 19.5, 39, 19.5)

SevenBus.add_conductor_element("partridge", 0.0217, 1.5, 0.385, 2, 0.642, "GEOM")

SevenBus.add_transmissionline_element("L1", "Bus 2", "Bus 4", 10, "partridge")
SevenBus.add_transmissionline_element("L2", "Bus 2", "Bus 3", 25, "partridge")
SevenBus.add_transmissionline_element("L3", "Bus 3", "Bus 5", 20, "partridge")
SevenBus.add_transmissionline_element("L4", "Bus 4", "Bus 6", 20, "partridge")
SevenBus.add_transmissionline_element("L5", "Bus 5", "Bus 6", 10, "partridge")
SevenBus.add_transmissionline_element("L6", "Bus 4", "Bus 5", 35, "partridge")

SevenBus.add_load_element("load2", 0, 0, "Bus 2")
SevenBus.add_load_element("load3", -110, -50, "Bus 3")
SevenBus.add_load_element("load4", -100, -70, "Bus 4")
SevenBus.add_load_element("load5", -100, -65, "Bus 5")
SevenBus.add_load_element("load6", 0, 0, "Bus 6")
SevenBus.add_load_element("load7", 0, 0, "Bus 7")

SevenBus.add_generator_element("Gen 1", "Bus 1", 100, 0)
SevenBus.add_generator_element("Gen 2", "Bus 7", 200, 0)

SevenBus.make_ybus()
SevenBus.make_jacobian()
SevenBus.initialize_powerINT()
SevenBus.make_power_mismatch()
SevenBus.make_solution_vector()
SevenBus.calc_current()
SevenBus.calc_powerloss()
#print(SevenBus.make_ybus())
print(SevenBus.solution())
print(SevenBus.calc_current())
print(SevenBus.calc_powerloss())