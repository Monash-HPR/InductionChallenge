import matplotlib.pyplot as plt
import math

import Modules.backend as bk


ballast = bk.simulation_target(9144)
[apogee,height,velocity,dvdt,time,mach,c_g] = bk.simulation(ballast)
print('The rocket was launched to an apogee of: %.3fm'%apogee,'\nWith a ballast of: %.3fkg' %ballast)


cp = bk.centre_pressure()
stab_margin = []
for cg in c_g:
    stab_margin.append((cp-cg)/0.127)

plt.figure(1)
plt.subplot(3,2,1)
plt.plot(time, height)
plt.xlabel('Time [s]')
plt.ylabel('Altitude [m]')
plt.subplot(3,2,2)
plt.plot(time, velocity)
plt.xlabel('Time [s]')
plt.ylabel('Velocity [m/s]')
plt.subplot(3,2,3)
plt.plot(time, dvdt)
plt.xlabel('Time [s]')
plt.ylabel('Acceleration [m/s^2]')
plt.subplot(3,2,4)
plt.plot(time, mach)
plt.xlabel('Time [s]')
plt.ylabel('Mach')
plt.subplot(3,2,5)
plt.plot(time, stab_margin)
plt.xlabel('Time [s]')
plt.ylabel('Stability Margin')
plt.subplot(3,2,6)
plt.plot(time, c_g)
plt.xlabel('Time [s]')
plt.ylabel('CG')
plt.show()
