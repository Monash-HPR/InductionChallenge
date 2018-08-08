# You should use numpy for some of the maths functions you will need to call
import numpy as np

# This is an example of using a Python function as a way to call a C function
def getForce( double t):
  return c_getForce( t)
# This is the C-style function
# Note the return type (double) and argument type (also a double)
# It has a different name to the Python function to distinguish it
cdef double c_getForce( double t):
  # Write your code here, then delete the statement below
  if t >= 4.5:
    return 0
  else:
    return 3000*(1-np.power(10.0,-5)*np.exp(np.log(np.power(10.0,5))*t/4.5))


# Try writing another C-style function
def getFuelBurned(double t):
  return c_getFuelBurned(t)

cdef double c_getFuelBurned( double t):
  if t >= 4.5:
    return 9
  else:
    return (2*t)
