# You should use numpy for some of the maths functions you will need to call
import numpy as np 

# This is an example of using a Python function
def getForce(rocket, t):
    thrust = rocket.peakThrust*(1 - (10**-5)*np.exp(np.log(10**5)*t/rocket.tBurnout))
    return thrust


def getFuelBurned(rocket, t):
    mass = rocket.mass0 - (rocket.fuelMass/rocket.tBurnout)*t
    return mass
