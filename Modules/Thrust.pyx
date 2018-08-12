import numpy as np


def getForce(t):
    T0=3000;
    tb=4.5
    T=T0*(1-10**(-5)*np.exp(np.log(10**5)*t/tb));
    return T


def getFuelBurnt(mf,t):
    tb=2.5
    MF=-(mf/tb)*t;
    return MF