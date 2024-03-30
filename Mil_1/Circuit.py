# Name: Daniel Hawbaker
# Last Edited: 28 MAR 2024
# Project: Milestone 3
# Class: ECE 2774

#circuit class to make user interface

from Bus import bus
from typing import Dict, List
from Generator import generator
from Conductor import conductor
from transformer import Tx
from Geometry import geometry
from transmissionline import tline
from Load import load
import numpy as np
import pandas as pd

class circuit:
    def __init__(self, name: str):
        self.name = name
        self.bus_order: List[str] = list() #makes a list of buses
        self.buses: Dict[str, bus] = dict() #brings in bus names
        self.xmfr: Dict[str, Tx] = dict() #brings in transformer names
        self.geometries: Dict[str, geometry] = dict()
        self.conductors: Dict[str, conductor] = dict()
        self.Tlines: Dict[str, tline] = dict()
        self.load: Dict[str, load] = dict()
        self.generator: Dict[str, generator] = dict()

    def add_bus_element(self, name: str, voltage):
        if self.name not in self.buses.keys():
            self.buses[name] = bus(name, voltage)
            self.bus_order.append(name)

    def add_transformer_element(self, name: str, xr_ratio: float, z_percent: float, power_rating: float, busA: str, busB: str ):
        self.xmfr[name] = Tx(name, xr_ratio, z_percent, power_rating, self.buses[busA], self.buses[busB])
        #self.add_bus_Element() another way to do this.

    def add_geometry_element(self, name, Dab, Dac, Dbc):
        self.geometries[name] = geometry(name, Dab, Dac, Dbc)
    def add_conductor_element(self, name: str, GMR, spacing, Rc, bundles, diameter, geometries_name: str):
        self.conductors[name] = conductor(name, GMR, spacing, Rc, bundles, diameter, self.geometries[geometries_name])
    def add_transmissionline_element(self, name: str, busA: str, busB: str, length: float, conductor_name: str):
        self.Tlines[name] = tline(name, self.buses[busA], self.buses[busB], length, self.conductors[conductor_name])

    def add_load_element(self, name: str, realPWR: float, reactPWR: float, busA: str):
        self.load[name] = load(name, realPWR, reactPWR, self.buses[busA])

    def add_generator_element(self, name: str, busA: str, realPWR: float, reactPWR: float):
        self.generator[name] = generator(name, self.buses[busA], realPWR, reactPWR)
    def make_ybus(self):
        size = np.zeros([len(self.buses), len(self.buses)])
        self.YBus = pd.DataFrame(data=size, index=self.bus_order, columns=self.bus_order, dtype=complex)

        for A in self.xmfr.keys():
            self.YBus.loc[self.xmfr[A].busA.name, self.xmfr[A].busA.name] += (self.xmfr[A].yprim.loc)[self.xmfr[A].busA.name, self.xmfr[A].busA.name]
            self.YBus.loc[self.xmfr[A].busB.name, self.xmfr[A].busB.name] += (self.xmfr[A].yprim.loc)[self.xmfr[A].busB.name, self.xmfr[A].busB.name]
            self.YBus.loc[self.xmfr[A].busA.name, self.xmfr[A].busB.name] += (self.xmfr[A].yprim.loc)[self.xmfr[A].busA.name, self.xmfr[A].busB.name]
            self.YBus.loc[self.xmfr[A].busB.name, self.xmfr[A].busA.name] += (self.xmfr[A].yprim.loc)[self.xmfr[A].busB.name, self.xmfr[A].busA.name]

        for A in self.Tlines.keys():
            self.YBus.loc[self.Tlines[A].busA.name, self.Tlines[A].busA.name] += (self.Tlines[A].yprim.loc)[self.Tlines[A].busA.name, self.Tlines[A].busA.name]
            self.YBus.loc[self.Tlines[A].busB.name, self.Tlines[A].busB.name] += (self.Tlines[A].yprim.loc)[self.Tlines[A].busB.name, self.Tlines[A].busB.name]
            self.YBus.loc[self.Tlines[A].busA.name, self.Tlines[A].busB.name] += (self.Tlines[A].yprim.loc)[self.Tlines[A].busA.name, self.Tlines[A].busB.name]
            self.YBus.loc[self.Tlines[A].busB.name, self.Tlines[A].busA.name] += (self.Tlines[A].yprim.loc)[self.Tlines[A].busB.name, self.Tlines[A].busA.name]

        return self.YBus

    def make_jacobian(self):
        J1 = np.zeros([len(self.buses)-1, len(self.buses)-1])
        J2 = np.zeros([len(self.buses)-1, len(self.buses)-2])
        J3 = np.zeros([len(self.buses)-2, len(self.buses)-1])
        J4 = np.zeros([len(self.buses)-2, len(self.buses)-2])
        TOP = np.hstack((J1,J2))
        BOT= np.hstack((J3,J4))
        jacobian = np.vstack((TOP,BOT))
        return jacobian

    def make_power_mismatch(self):
        PWR = np.zeros([len(self.buses), 1])
        QPWR = np.zeros([len(self.buses), 1])
        power = np.hstack((PWR, QPWR))
        return power

    def make_solution_vector(self):
        delta = np.zeros([1, len(self.buses)])
        V = np.zeros([1, len(self.buses)])
        Xvector = np.vstack((delta,V))
        return Xvector

