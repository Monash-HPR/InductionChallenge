# This is an example of a pure Python function
import numpy as np

def getForce(data, rocket, s, v):
    T = data.temp0 + data.lapseRate*s
    density = data.density0*(T/data.temp0)**(-data.g0/(data.lapseRate*data.rAir))
    M = v/np.sqrt(data.gammaAir*data.rAir*T)
    Cd = np.exp(-0.5*M)*(0.5*np.exp(-2*M)*np.cos(5.5*M)+0.1*M*np.log(M)+0.5)+ 0.1*np.exp(M-5)
    drag = 0.5*density*(v**2)*rocket.area*Cd
    return (drag, M)