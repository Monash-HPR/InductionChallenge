import numpy as np

class GeneralData():
    def __init__(self):
        self.lapseRate = -0.0065
        self.g0 = 9.80665
        self.rAir = 287.16
        self.density0 = 1.01325
        self.temp0 = 288.15
        self.gammaAir = 1.4
        self.GM = 3.986*10**14
        self.rEarth = 6378137

class RocketDimensions():
    def __init__(self):
        self.diameter = 0.127
        self.R = self.diameter/2
        self.CnN = 2
        self.numFins = 4
        self.Cr = 0.25
        self.Ct = 0.06
        self.sweepAngle = 60
        self.Ln = 0.7
        self.S = 0.11
        self.L = 3.5
        
class State():
    def __init__(self):
        self.time = np.linspace(0, 60, 1000)
        self.currentTime = self.time[0]
        self.height = np.zeros(np.size(self.time))
        self.velocity = np.zeros(np.size(self.time))
        self.F = 0
        self.acceleration = np.zeros(np.size(self.time))
        self.Mach = np.zeros(np.size(self.time))
        self.stability = np.zeros(np.size(self.time))
        self.xcg = np.zeros(np.size(self.time))