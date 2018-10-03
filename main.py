__author__ = 'Hamish Self'

import backend.python_sim_code as s
import matplotlib.pyplot as plt

# Rocket Data
t_0 = 0                             # time after launch to begin simulation, s
m_total_0 = 25                      # kg
m_fuel_0 = 9                        # kg
a_surf = 0.07712                    # surface area (cylindrical approx), m^2
T_0 = 3000                          # peak thrust, N
t_B = 4.5                           # burnout time, secs
alt_0 = 0                           # initial altitude, m
vel_0 = 0                           # initial velocity, m s^-1


# Initialise pre-launch state
# State(m_total, m_fuel, T_0, t_B, altitude, velocity, acceleration, time)
initial_state = s.State(m_total_0, m_fuel_0, a_surf, T_0, t_B, alt_0, vel_0, t_0)
print('Initial state: {}'.format(initial_state.summary()))

state_array, sim_time = s.run_simulation(initial_state, dt=0.01)
print('Simulation time: {}s'.format(sim_time))

# Post-processing steps
alt_array = [s.alt for s in state_array]
time_array = [s.time for s in state_array]
vel_array = [s.vel for s in state_array]
accel_array = [s.acc for s in state_array]

plt.figure()
plt.subplot(2, 2, 1)
plt.plot(time_array,alt_array,'r-')
plt.xlabel('time, seconds')
plt.ylabel('z(t), m')
plt.grid()

plt.subplot(2, 2, 2)
plt.plot(time_array,vel_array,'r-')
plt.xlabel('time, seconds')
plt.ylabel('v(t), m s^-1')
plt.grid()

plt.subplot(2, 2, 3)
plt.plot(time_array,accel_array,'r-')
plt.xlabel('time, seconds')
plt.ylabel('a(t), m s^-2')
plt.grid()

plt.show()


# ALSO NEED TO ACCOUNT FOR PARACHUTE DEPLOYMENT DRAG - ASK OLI
