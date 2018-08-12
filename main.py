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

## Initialisatin
dt=0.005;
time=t=np.arange(0,7,dt);

#Rocket Specs
diamter=0.098;
length=2.5;
freeMass=16;
fuelMass=9;
Saturn=Rocket.Rocket(freeMass+fuelMass,np.pi*diamter*length);

#Pre Allocating other variables
F=[0]*(len(time)-1);
Mf=[0]*(len(time)-1);
T=[0]*(len(time)-1);
D=[0]*(len(time)-1);
g=[0]*(len(time)-1);
a=[0]*(len(time)-1);
v=[0]*(len(time)-1);
s=[0]*(len(time)-1);

T[0] = Thrust.getForce(time[0]);
g[0] = Gravity.Gravity(s[0]);
F[0]=T[0]-(Saturn.mass*g[0]);
a[0]=F[0]/Saturn.mass;
vellAcc=0;



## Main Loop
for i in range(1,len(time)-1):
    T[i]=Thrust.getForce(time[i]);
    g[i]=Gravity.Gravity(s[i]);
    D[i]=Drag.Drag(v[i-1],s[i-1],Saturn.area)
    Mf[i] = fuelMass - Thrust.getFuelBurnt(fuelMass, time[i]);
    Saturn.mass=freeMass+Mf[i];
    F[i]=T[i]-(Saturn.mass *g[i])-D[i];
    a[i]=F[i]/Saturn.mass;
    vellAcc=Integration.eulerInteg(v[i-1],s[i-1],a[i],dt);
    v[i]=vellAcc[0];
    s[i]=vellAcc[1];


## Plotting
# When you have some data ready to plot, uncomment the code below (ctrl+/)
# plt.figure(1)
# plt.subplot(211)
# plt.plot(time, height)
# plt.xlabel('Time [s]')
# plt.ylabel('Altitude [m]')
# plt.subplot(211)
# plt.plot(time, velocity)
# plt.xlabel('Time [s]')
# plt.ylabel('Velocity [m/s]')
# plt.show()