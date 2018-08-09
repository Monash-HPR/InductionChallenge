# Kenneth Choo
# Version 0.0, 9/8/2018
#
# Notes:
# 1. This is a rough and ready 1DOF simulator of a rocket flight. It runs in pure Python since I haven't yet
#    found a way to set this up (even though I installed Cython). It should still run but the performance is
#    suboptimal.
#
# TODO:
# 1. Rewrite in Cython with associated compiler files.
# 2. Implement a rocket class instead of loading in four or five variables
# 3. Implement better integrator (Heun or RK4) and adaptive stepsizing (currently possible only by 'cheating')

import math

def drag(velocity, position, area):
  gamma = 1.4
  gas_const = 287.16
  temp_stand = 288.15
  lapse_rate = - 0.0065
  g0 = 9.80665
  pres_stand = 101325

  temp = temp_stand + lapse_rate*position
  pres = pres_stand*math.pow((temp/temp_stand), -(g0/(lapse_rate*gas_const)))
  dens = pres/(gas_const*temp)
  speed_sound = math.pow((gas_const*gamma*temp), 0.5)
  mach_no = velocity/speed_sound
  drag_coeff = math.exp(-1.2*mach_no)*math.sin(math.radians(mach_no)) + (mach_no/6)*math.log(mach_no+1, 10)

  drag_force = 0.5*dens*math.pow(velocity, 2)*area*drag_coeff
  return drag_force

def thrust(time):
  peak_thrust = 3000
  burn_time= 4.5
  thrust = peak_thrust*(1-(10**-5)*math.exp(math.log((10**5))*(time/burn_time))) #not just 10**5, this refactor emphasises smaller times
  if thrust < 0:
    return 0
  else:
    return thrust

def mass(time, m_init, m_fuel, burn_time):
  m_empty = m_init-m_fuel
  rate = -(m_fuel/burn_time)
  mass = m_init + rate*time
  if mass < m_empty:
    return m_empty
  else:
    return mass

def gravitation(height):
  g_param = 3.986 * 10**14
  r_e = 6378137
  g_acc = g_param/(r_e + height)**2
  return g_acc

def integrator(step, m_init, m_fuel, b_time, area): # Euler method for now
  time = 0
  position = 0
  velocity = 0
  pos_max = 0

  while position >= 0:
    if velocity >= 0: # sign of drag force changes to oppose velocity
      sign = 1
    else:
      sign = -1
    a_net = (thrust(time) - sign*(drag(velocity, position, area)))/mass(time, m_init, m_fuel, b_time) - gravitation(position)
    position = position + step*velocity
    velocity = velocity + step*a_net
    time = time + step
    if position > pos_max:
      pos_max = position
      time_max = time

  return (pos_max, time_max, time)

result = integrator(0.001, 25, 9, 4.5, 0.777)
print('Maximum height: ' + str(round(result[0], 2)) + ' m , ' + 'Time to maximum: ' + str(round(result[1], 2)) + ' s , ' + 'Time of flight: ' + str(round(result[2], 2)) + ' s')
