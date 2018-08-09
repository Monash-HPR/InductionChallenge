import math
import numpy as np
def getForce(double velocity, double area, double ground_temp, double ground_pressure, double altitude):

  #constants
  lapse_rate = -0.0065
  gravity_sea = 9.80665
  specific_gas_constant = 287.16
  adiabatic_index = 1.4

  
  current_temp = ground_temp + lapse_rate * altitude
  current_pressure = ground_pressure * ( current_temp / ground_temp) ** ( -gravity_sea / ( lapse_rate * specific_gas_constant))
  current_density = current_pressure / (specific_gas_constant * current_temp)
  mach_number = math.fabs(velocity / ( ( adiabatic_index * specific_gas_constant * current_temp) ** ( 0.5)))
  drag_coef = math.exp( -1.2 * mach_number) * math.sin(np.deg2rad(mach_number)) + (mach_number / 6) * math.log10(mach_number + 1)
  drag = 0.5 * current_density * (velocity ** 2) * area * drag_coef * np.sign(velocity)

  
  return drag