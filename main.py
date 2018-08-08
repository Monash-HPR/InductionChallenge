# External packages
import numpy as np                  # Maths
import scipy                        # Science
import matplotlib.pyplot as plt     # MATLAB-style plotting
# Internal modules
import Modules.Drag as Drag         # the "as" syntax lets you use an alias (no need to write Modules. every time!)
import Modules.Gravity as Gravity
import Modules.Thrust as Thrust
import Modules.Rocket as Rocket
import Modules.Integrator as Integrator

## Initialisation
## Main Loop
(time, height, velocity) = Integrator.integrateHeun(0.01)
print("Time to apogee: " + str(time[-1]) + "s", "Max Height: " + str(height[-1]) + "m")

## Plotting
# When you have some data ready to plot, uncomment the code below (ctrl+/)
plt.figure(1)
plt.subplot(2, 1, 1)
plt.plot(time, height)
plt.xlabel('Time [s]')
plt.ylabel('Altitude [m]')
plt.subplot(2, 1, 2)
plt.plot(time, velocity)
plt.xlabel('Time [s]')
plt.ylabel('Velocity [m/s]')
plt.show()
