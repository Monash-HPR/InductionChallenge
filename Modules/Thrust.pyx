
import numpy as np
from math import exp
from math import log
thrust_peak = 3000
time_burnout = 4.5




def getForce( double t):
  return c_getForce( t)

cdef double c_getForce( double t):
#will return zero thrust after t>0 since the eqaution goes negative after that
  if ( t <= 4.5):
    thrust = thrust_peak * ( 1 - ( 10 ** (-5)) * exp( t * log(100000) / time_burnout))
    return thrust
  else:
    return 0



def getFuelBurned( double dt, double mass_fuel):
  return c_getFuelBurned( dt, mass_fuel)
cdef c_getFuelBurned( double dt, double mass_fuel):
#will return zero fuel mass after it reaches zero since the eqaution goes neg.
  if (mass_fuel<=0):
    return 0
  else:
    mass_fuel = mass_fuel - (mass_fuel / time_burnout)*dt
  return mass_fuel