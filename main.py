# External packages
import numpy as np                  # Maths 
import matplotlib.pyplot as plt     # MATLAB-style plotting
# Internal modules
import Modules.Drag as Drag         # the "as" syntax lets you use an alias (no need to write Modules. every time!)
import Modules.Gravity as Gravity 
import Modules.Thrust as Thrust 
import Modules.Rocket as RocketFile
import Modules.Integrator as Integrator
import Modules.Data as Data
import Modules.Stability as Stability

## Initialisation
data = Data.GeneralData()
dimensions = Data.RocketDimensions()
rocket = RocketFile.RocketClass()
state = Data.State()
initialMass = rocket.mass0

## Main Loop
def getTrajectory(data, dimensions, rocket, state, ballast):
    c = 0
    
    state.height = np.zeros(np.size(state.time))
    state.velocity = np.zeros(np.size(state.time))
    state.height[0] = 0.0001
    state.velocity[0] = 0.0001
    
    state.acceleration = np.zeros(np.size(state.time))
    state.Mach = np.zeros(np.size(state.time))
    state.stability = np.zeros(np.size(state.time))
    state.xcg = np.zeros(np.size(state.time))
 
    rocket.mass0 = initialMass + ballast   
    
    while c <= np.size(state.time) - 2:
        state.currentTime = state.time[c]
        t = state.currentTime
        s = state.height[c]
        v = state.velocity[c]
    
        if v > 0:
            drag = Drag.getForce(data, rocket, s, v)[0]
            g = Gravity.getForce(data, s)
            state.Mach[c] = (Drag.getForce(data, rocket, s, v)[1])
            xCp = Stability.centreOfPressure(dimensions)
    
            if t <= rocket.tBurnout:
                T = Thrust.getForce(rocket, t)
                m = Thrust.getFuelBurned(rocket, t) + ballast
                rocket.mass = m
                xCg = Stability.centreOfGravity(rocket)
            else:
                T = 0
                m = rocket.massFinal + ballast
                xCg = rocket.xcgRocket
        
            state.F = T - drag - m*g
        
            state.acceleration[c] = state.F/m

            state.stability[c] = (xCp - xCg)/dimensions.diameter
            state.xcg[c] = xCg
    
            state.height[c+1] = Integrator.integrateEuler(state, m, s, v)[0]
            state.velocity[c+1] = Integrator.integrateEuler(state, m, s, v)[1]
    
            c = c + 1
        else:
            break
        
    altitude = np.amax(state.height)*3.2808399
        
    return altitude
  
## Ballast calculator
altRequired = 30000
# intial guesses
xi1 = 0.2
xi = 0
xi_1 = 0
 
precision = 0.1
diff = 1

while np.absolute(diff) > precision:    
    xi_1 = xi
    xi = xi1
    
    diffPrev = getTrajectory(data, dimensions, rocket, state, xi_1) - altRequired
    diffCurr = getTrajectory(data, dimensions, rocket, state, xi) - altRequired
        
    xi1 = xi - (diffCurr*(xi_1 - xi))/(diffPrev - diffCurr)
    diff = getTrajectory(data, dimensions, rocket, state, xi1) - altRequired    
    

ballast = xi1
print('ballast: ', ballast)

## Plotting
# When you have some data ready to plot, uncomment the code below (ctrl+/)
# removing zero values from array
index = state.velocity != 0
time = state.time[index]
height = state.height[index]
velocity = state.velocity[index]
acceleration = state.acceleration[index]
mach = state.Mach[index]
stability = state.stability[index]
xcg = state.xcg[index]

plt.figure()
plt.subplot(321)
plt.plot(time, height)
plt.xlabel('Time [s]')
plt.ylabel('Altitude [m]')
plt.subplot(322)
plt.plot(time, velocity)
plt.xlabel('Time [s]')
plt.ylabel('Velocity [m/s]')
plt.subplot(323)
plt.plot(time, acceleration)
plt.xlabel('Time [s]')
plt.ylabel('Acceleration [m/s^2]')
plt.subplot(324)
plt.plot(time, mach)
plt.xlabel('Time [s]')
plt.ylabel('Mach number')
plt.subplot(325)
plt.plot(time, stability)
plt.xlabel('Time [s]')
plt.ylabel('Stability margin')
plt.subplot(326)
plt.plot(time, xcg)
plt.xlabel('Time [s]')
plt.ylabel('Centre of Gravity')
plt.show()

