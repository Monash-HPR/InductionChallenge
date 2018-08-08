# This is an example of a pure Python function
import numpy as np
def getForce(double h, double V):
  return c_getForce(h, V)

cdef double c_getForce(double h, double V):
  # Write your code here, then delete the "pass" statement below
  cdef double T = 288.15 - 0.0065*h
  cdef double rho = 101325*np.power(T/288.15,-9.80665/(-0.0065*287.16))/(287.16*T)
  cdef double S = np.pi*0.098*2.5
  cdef double M = V/np.sqrt(1.4*287.16*T)
  cdef double Cd = np.exp(-1.2*M)*np.sin(M*np.pi/180) + (M/6)*np.log10(M + 1)
  #print("Thermo M, Cd", M, Cd)
  return 0.5*rho*np.power(V,2)*S*Cd
