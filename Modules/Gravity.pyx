import math
def getForce(mass, altitude):
  g = 3.986e14/math.pow(6378137.0+altitude,2)
  return (mass*g)
