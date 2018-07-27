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
  return 0.0


# Try writing another C-style function
def getFuelBurned():
  return c_getFuelBurned()
cdef c_getFuelBurned():
  return 