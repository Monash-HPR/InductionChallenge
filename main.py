# External packages
import numpy as np                  # Maths 
import scipy                        # Science
import matplotlib.pyplot as plt
import math   # MATLAB-style plotting
# Internal modules
import Modules.Drag as Drag         # the "as" syntax lets you use an alias (no need to write Modules. every time!)
import Modules.Gravity as Gravity 
import Modules.Thrust as Thrust 
import Modules.Rocket as Rocket
import Modules.Integrator as Integrator


## Initialisation
mass_dry = 16 #kg
mass_fuel = 9 #kg
mass = mass_fuel + mass_dry #kg

length = 2.5 #metres
diameter = 0.098 #metres 
ground_temp = 288.15 # kelvin
ground_pressure = 101325 #in Pa

dt = 0.01 #change in time between integration steps
time_max = 50 # max run time for simulation in seconds
no_steps = round(time_max / dt) #number of steps used in simulation

time = np.zeros(no_steps + 1)
velocity = np.zeros(no_steps + 1)
acceleration = np.zeros(no_steps + 1)
altitude = np.zeros(no_steps + 1)
steps = np.zeros(no_steps + 1)

# area caluclation is currently surface area on the side of the rocket
area = math.pi * diameter *length
# not really using this class.Rocket part.
rocket = Rocket(mass, area)

## Main Loop

for step in range (1,no_steps):
  #find values from functions
  current_drag = Drag.getForce(velocity[step], area, ground_temp, ground_pressure, altitude[step])
  current_thrust = Thrust.getForce((dt * step))
  current_gravitation = Gravity.getForce(altitude[step])

  ## fuel calculations using the fuel burned function, although weird how it needs to be a plus and not a minus on the second equation
  mass_fuel = Thrust.getFuelBurned(dt, mass_fuel)
  current_mass = mass_dry + mass_fuel


  ## make calculations based on values found above
  total_force = current_thrust - current_gravitation * current_mass - current_drag
  steps[step+1] = dt * step
  acceleration[step + 1] = total_force / current_mass

  #find velocity and altitude
  velocity[step + 1] = velocity[step] + 0.5*(acceleration[step +1] + acceleration[step]) * dt
  altitude[step + 1] = altitude[step] + velocity[step + 1] * dt + 0.5 * (dt **2) *acceleration[step]


  ## check to stop the loop if rocket has landed
  if (altitude[step] < 0):
  	steps_completed_flight = step
  	step = no_steps


  # print("grav =", current_gravitation)
  # print("time =", dt*step)
  # print("drag =", current_drag)
  # print("velo =", velocity[step])
  # print("haut =", altitude[step])
  # print("acc =", acceleration[step])
  # print("mass =", current_mass)
  #print("mass_fuel =", mass_fuel)
  # print("")


## final calculations
altitude_max=max(altitude)
print("Maximum altitude = %.2f" % altitude_max)
print("Flight time = %.2f" % (steps_completed_flight*dt))


## Plotting
#When you have some data ready to plot, uncomment the code below (ctrl+/)
plot = plt.figure(1)
ax1 = plt.subplot(211)
ax1.plot(steps, altitude)
plt.xlabel('Time [s]')
plt.ylabel('Altitude [m]')
ax2 = plt.subplot(212)
ax2.plot(steps,velocity)
plt.xlabel('Time [s]')
plt.ylabel('Velocity [m/s]')
plt.show()
