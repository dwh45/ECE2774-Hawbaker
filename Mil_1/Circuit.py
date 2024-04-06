# Name: Daniel Hawbaker
# Last Edited: 04 APR 2024
# Project: Milestone 3b
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
from settings import s

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


    def add_bus_element(self, name: str, voltage, bus_type, voltmag: float, angle: float):
        if self.name not in self.buses.keys():
            self.buses[name] = bus(name, voltage, bus_type, voltmag, angle)
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
        Jac1 = np.zeros([len(self.buses)-1, len(self.buses)-1]) #initializes J1 of jacobian as 6x6 array of 0's
        Jac2 = np.zeros([len(self.buses)-1, len(self.buses)-2]) #initializes J2 of jacobian as 5x6 array of 0's
        Jac3 = np.zeros([len(self.buses)-2, len(self.buses)-1]) #initializes J3 of jacobian as 6x5 array of 0's
        Jac4 = np.zeros([len(self.buses)-2, len(self.buses)-2]) #initializes J4 of jacobian as 5x5 array of 0's
        J1 = 0
        J2 = 0
        J3 = 0
        J4 = 0
        for n in range(0, len(self.buses) - 1):
            N = "Bus " + str(n+2)
            for k in range(0, len(self.buses) - 1):
                K = "Bus " + str(k+2)
                if n == k:
                    for x in range(1, bus.numbus+1):
                        M = "Bus " + str(x)
                        if (x-2) == k:
                            j1 = 0
                            J1 = J1 + j1
                        else:
                            j1 = np.abs(self.YBus.loc[K, M]) * self.buses[M].voltmag * np.sin(self.buses[K].angle - self.buses[M].angle - np.angle(self.YBus.loc[K,M]))
                            J1 = J1 + j1
                    Jac1[n, k] = -1 * self.buses[K].voltmag * J1
                    J1 = 0
                else:
                    #N = "Bus " + str(n+2)
                    Jac1[n, k] = self.buses[K].voltmag * np.abs(self.YBus.loc[K, N]) * self.buses[N].voltmag * np.sin(self.buses[K].angle - self.buses[N].angle - np.angle(self.YBus.loc[K,N]))
#ALL ABOVE IS FOR J1 QUADRANT OF JACOBIAN
            for k in range(0, len(self.buses) - 2):
                K = "Bus " + str(k+2)
                if n == k:
                    for x in range(1, bus.numbus+1):
                        N = "Bus " + str(x)
                        j2 = np.abs(self.YBus.loc[K, N]) * self.buses[N].voltmag * np.cos(self.buses[K].angle - self.buses[N].angle - np.angle(self.YBus.loc[K,N]))
                        J2 = J2 + j2
                    Jac2[n, k] = self.buses[K].voltmag * np.abs(self.YBus.loc[K, K]) * np.cos(np.angle(self.YBus.loc[K,K])) + J2
                    J2 = 0
                else:
                    N = "Bus " + str(n+2)
                    Jac2[n, k] = self.buses[K].voltmag * np.abs(self.YBus.loc[K, N]) * np.cos(self.buses[K].angle - self.buses[N].angle - np.angle(self.YBus.loc[K,N]))
#ALL ABOVE IS FOR J2 QUADRANT OF JACOBIAN
        for n in range(0, len(self.buses) - 2):
            N = "Bus " + str(n+2)
            for k in range(0, len(self.buses) - 1):
                K = "Bus " + str(k+2)
                if n == k:
                    for x in range (1, bus.numbus+1):
                        N = "Bus " + str(x)
                        if (x-2) == k:
                            j3 = 0
                            J3 = J3 + j3
                        else:
                            j3 = np.abs(self.YBus.loc[K, N]) * self.buses[N].voltmag * np.cos(self.buses[K].angle - self.buses[N].angle - np.angle(self.YBus.loc[K,N]))
                            J3 = J3 + j3
                    Jac3[n, k] = self.buses[K].voltmag * J3
                    J3 = 0
                else:
                    N = "Bus " + str(n+2)
                    Jac3[n, k] = -1 * self.buses[K].voltmag * np.abs(self.YBus.loc[K, N]) * np.cos(self.buses[K].angle - self.buses[N].angle - np.angle(self.YBus.loc[K,N]))
#ALL ABOVE IS FOR J3 QUADRANT OF JACOBIAN
            for k in range(0, len(self.buses) - 2):
                K = "Bus " + str(k+2)
                if n == k:
                    for x in range (1, bus.numbus+1):
                        N = "Bus " + str(x)
                        j4 = np.abs(self.YBus.loc[K, N]) * self.buses[N].voltmag * np.sin(self.buses[K].angle - self.buses[N].angle - np.angle(self.YBus.loc[K,N]))
                        J4 = J4 + j4
                    Jac4[n, k] = -1 * self.buses[K].voltmag * np.abs(self.YBus.loc[K, K]) * np.sin(np.angle(self.YBus.loc[K,K])) + J4
                    J4 = 0
                else:
                    N = "Bus " + str(n+2)
                    Jac4[n, k] = self.buses[K].voltmag * np.abs(self.YBus.loc[K, N]) * np.sin(self.buses[K].angle - self.buses[N].angle - np.angle(self.YBus.loc[K,N]))
#ALL ABOVE IS FOR J4 QUADRANT OF JACOBIAN
        TOP = np.hstack((Jac1,Jac2))
        BOT= np.hstack((Jac3,Jac4))
        self.jacobian = np.vstack((TOP,BOT))
        return self.jacobian

    def initialize_powerINT(self):
        PWR = np.zeros([len(self.buses), 1])
        QPWR = np.zeros([len(self.buses), 1])
        self.powerINT = np.vstack((PWR, QPWR))
        self.powerINT[1] = self.load["load2"].realPWR
        self.powerINT[2] = self.load["load3"].realPWR
        self.powerINT[3] = self.load["load4"].realPWR
        self.powerINT[4] = self.load["load5"].realPWR
        self.powerINT[5] = self.load["load6"].realPWR
        self.powerINT[6] = self.load["load7"].realPWR - self.generator["Gen 2"].realPWR
        self.powerINT[8] = self.load["load2"].reactPWR
        self.powerINT[9] = self.load["load3"].reactPWR
        self.powerINT[10] = self.load["load4"].reactPWR
        self.powerINT[11] = self.load["load5"].reactPWR
        self.powerINT[12] = self.load["load6"].reactPWR
        self.powerINT[13] = self.load["load7"].reactPWR
        self.powerINT = self.powerINT/s.s_mva
        self.counting = 0
        return self.powerINT


    def make_power_mismatch(self):
        PWR = np.zeros([len(self.buses), 1])
        QPWR = np.zeros([len(self.buses), 1])
        #if self.counting != 0:
         #   self.powerINT = self.powerINT - self.power
        P = 0
        Q = 0
        for k in range(0, bus.numbus):
            K = "Bus " + str(k+1)
            for n in range(0, bus.numbus):
                N = "Bus " + str(n+1)
                p = np.abs(self.YBus.loc[K, N]) * self.buses[N].voltmag * np.cos(self.buses[K].angle - self.buses[N].angle - np.angle(self.YBus.loc[K,N]))
                P = P + p
            PWR[k] = self.buses[K].voltmag * P
        for k in range(0, bus.numbus):
            K = "Bus " + str(k+1)
            for n in range(0, bus.numbus):
                N = "Bus " + str(n+1)
                q = np.abs(self.YBus.loc[K,N]) * self.buses[N].voltmag * np.sin(self.buses[K].angle - self.buses[N].angle - np.angle(self.YBus.loc[K,N]))
                Q = Q + q
            QPWR[k] = self.buses[K].voltmag * Q
        self.power = np.vstack((PWR, QPWR))
        self.mismatch = self.powerINT - self.power
        self.counting+=1

        for z in range(len(self.mismatch)-1,-1,-1):
            if z > 6:
                Z = "Bus " + str(z-bus.numbus+1)
                if self.buses[Z].bus_type == "PV":
                    self.mismatch = np.delete(self.mismatch, z)
            else:
                Z = "Bus " + str(z +1)
            if self.buses[Z].bus_type == "slack":
                self.mismatch = np.delete(self.mismatch, z)
                #self.mismatch = np.delete(self.mismatch, z)
        return self.mismatch

    def make_solution_vector(self):
        delta = np.zeros([1, len(self.buses)])
        V = np.ones([1, len(self.buses)])
        self.Xvector = np.hstack((delta,V))
        for z in range(bus.numbus*2-1,-1,-1):
            if z > 6:
                Z = "Bus " + str(z-bus.numbus+1)
                if self.buses[Z].bus_type == "PV":
                    self.Xvector = np.delete(self.Xvector, z)
            else:
                Z = "Bus " + str(z +1)
            if self.buses[Z].bus_type == "slack":
                self.Xvector = np.delete(self.Xvector, z)
        deltaX = np.linalg.solve(self.jacobian, self.mismatch)
        #deltaX = np.linalg.inv(self.jacobian) * self.mismatch
        self.Xvector = self.Xvector + deltaX
        return self.Xvector

    def solution(self):

        tolerance = 0.0001
        for f in range(100):
            counter = 0
            for g in range(len(self.mismatch)):
                for x in range(0, bus.numbus):
                    X = "Bus " + str(x + 1)
                    if self.buses[X].bus_type != "slack" and self.buses[X].bus_type != "PV":
                        self.buses[X].voltmag = self.buses[X].voltmag - self.Xvector[x + bus.numbus - 2] +1
                        self.buses[X].angle = self.buses[X].angle + np.rad2deg(self.Xvector[x - 1])
                    elif self.buses[X].bus_type != "slack":
                        self.buses[X].angle = self.buses[X].angle + np.rad2deg(self.Xvector[x - 1])
                        #self.buses[X].voltmag = self.buses[X].voltmag - np.abs(self.Xvector[x + bus.numbus -2])
                if np.abs(self.mismatch[g]) <= tolerance:
                    counter += 1
                if counter == len(self.mismatch):
                    solutionVect = pd.array(data=np.zeros(len(self.buses)*2))
                    a = 0
                    for k in self.buses:
                        solutionVect[a] = np.rad2deg(self.buses[k].angle)
                        solutionVect[a + bus.numbus] = self.buses[k].voltmag
                        a+=1
                    print(solutionVect)
                self.make_jacobian()
                self.make_power_mismatch()
                self.make_solution_vector()