__author__ = 'Hamish Self'

# Dependencies
import numpy as np
import copy
import time
import cython


# State Class definition
# ==============================================================================
class State:

    # Constructor method
    def __init__(self, m_total_0, m_fuel_0, a_surf, T_0, t_B, alt, vel, time):
        # physical properties
        self.mass_total_0 = m_total_0   # total initial mass, kg, includes fuel
        self.mass_fuel_0 = m_fuel_0     # initial fuel mass, kg
        self.area = a_surf              # surface area, m^2

        # simulation
        self.time = time                # time after launch, s

        # motor properties
        self.thrust_peak = T_0          # peak thrust, N
        self.time_burnout = t_B         # burnout time, s

        # positional properties
        self.alt = alt                  # altitude above sea level, m
        self.vel = vel                  # velocity, m s^-1
        self.acc = None                 # acceleration, m s^-2

    # Forces
    def thrust(self):
        cdef double thrust_0 = self.thrust_peak
        cdef double t_burnout = self.time_burnout
        cdef double t = self.time
        cdef double thrust_newton
        if t <= t_burnout:
            thrust_newton = thrust_0*(1-10**(-5)*np.exp(np.log(10**5)*(t/t_burnout)))
        else:
            thrust_newton = 0
        return thrust_newton

    def mach_num(self):
        cdef double alt = self.alt
        cdef double vel = abs(self.vel)
        cdef double gamma = 1.4
        cdef double R_const = 287.16
        cdef double temp_val = temp(alt)
        cdef double sound_speed = np.sqrt(gamma*R_const*temp_val)
        cdef double m
        m = vel/sound_speed
        return m

    def drag_co(self):
        cdef double m = self.mach_num()
        drag_coefficient = np.exp(-1.2*m)*np.sin(m) + (m/6)*np.log10(m+1)
        return drag_coefficient

    def drag(self):
        # sign convention: return negative force if positive velocity, positive
        # force if negative velocity, as drag always acts to oppose the
        # vehicle's motion
        cdef double vel = self.vel
        cdef double rho = density(self.alt)
        cdef double area = self.area
        cdef double c_D = self.drag_co()
        cdef double drag_newton = 0.
        if vel >= 0:
            drag_newton = - 0.5*rho*(vel**2)*area*c_D
        elif vel < 0:
            drag_newton = 0.5 * rho * (vel ** 2) * area * c_D
        return drag_newton

    # NB: this function returns an acceleration rather than a force (no M)
    def grav(self):
        # expect alt in metres
        # Sign convention: Gravitational force always negative, as it points
        # towards the centre of the Earth
        cdef double alt = self.alt
        cdef double mu = 3.986 * 10**14         # mu = GM, standard gravitational parameter
        cdef double r_earth = 6378137           # metres, radius of the earth
        cdef double r_craft = alt + r_earth     # metres,
        # distance of the craft from the centre of the Earth
        cdef double g_accel = -mu/(r_craft**2)   # m s^-2, gravitational acceleration
        return g_accel

    def mass_rocket(self):
        cdef double t = self.time
        cdef double t_burnout = self.time_burnout
        cdef double m_total_0 = self.mass_total_0
        cdef double m_fuel_0 = self.mass_fuel_0
        cdef double mass_fuel_val
        if t < t_burnout:
            mass_fuel_val = m_fuel_0*(1 - t/t_burnout)
        else:
            mass_fuel_val = 0
        # total mass = empty mass + remaining fuel mass
        cdef double mass_total_val = (m_total_0 - m_fuel_0) + mass_fuel_val
        return mass_total_val

    def net_accel(self):
        # net force excluding gravitation
        cdef double thrust_force = self.thrust()
        cdef double drag_force = self.drag()
        cdef double aero_force = thrust_force + drag_force

        # convert to an acceleration for use with the gravitation acceleration,
        #   NB: mass is a function of time
        cdef double mass = self.mass_rocket()
        cdef double aero_accel = aero_force/mass

        # total vehicle acceleration: >0 upwards, <0 if downwards
        cdef double grav_accel = self.grav()
        cdef double total_accel = aero_accel + grav_accel
        return total_accel

    # Summary method
    # THIS IS BAD BUT IT WORKS, FIX IF I CAN BE FUCKED
    def summary(self):
        d = {'total mass': self.mass_rocket(),
             'time': self.time,
             'altitude': self.alt,
             'velocity': self.vel,
             'acceleration': self.net_accel()
             }
        return d


# Standard atmosphere properties
# ==============================================================================
def temp(alt):
    # expect alt in metres
    lapse_rate = 0.0065    # K m^-1
    temp_0 = 288.15         # K, sea level temperature
    temp_val = temp_0 - lapse_rate*alt
    return temp_val


def density(alt):
    lapse_rate = 0.0065    # K m^-1
    temp_0 = 288.15         # K, sea level temperature
    gas_const = 287.16      # units??
    density_0 = 1.225       # km m^-3, sea level density
    g_0 = 9.80665           # m s^-2, sea level gravitational acceleration
    temp_val = temp(alt)
    density_val = density_0*(temp_val/temp_0)**((g_0/(lapse_rate*gas_const) - 1))
    return density_val


# Solver
# ==============================================================================
# THIS ISN'T USEFUL BECAUSE WE DON'T HAVE AN EXPRESSION FOR DYDT IN A SINGLE
# VARIABLE
def rk4_step(in_state, double dt):
    # vars (single variable function case): dy/dt, t_0, y_0, dt
    cdef double change_t, change_v, change_z
    # STEPS: calculate the 4 guesses

    # GUESS STATE 1
    state_1 = copy.deepcopy(in_state)
    cdef double t_1 = state_1.time
    cdef double z_1 = state_1.alt
    cdef double v_1 = state_1.vel
    cdef double a_1 = state_1.net_accel()

    # GUESS STATE 2
    # state_2 = copy.deepcopy(in_state)
    change_t = 0.5*dt
    change_v = 0.5*a_1*dt
    change_z = 0.5*v_1*dt
    state_1.time = t_1 + change_t
    state_1.vel = v_1 + change_v
    state_1.alt = a_1 + change_z
    cdef double v_2 = state_1.vel
    cdef double a_2 = state_1.net_accel()

    # GUESS STATE 3
    # state_3 = copy.deepcopy(in_state)
    change_t = 0.5*dt
    change_v = 0.5*a_2*dt
    change_z = 0.5*v_2*dt
    state_1.time = t_1 + change_t
    state_1.vel = v_1 + change_v
    state_1.alt = z_1 + change_z
    cdef double v_3 = state_1.vel
    cdef double a_3 = state_1.net_accel()

    # GUESS STATE 4
    # state_4 = copy.deepcopy(in_state)
    change_t = dt
    change_v = dt*a_3
    change_z = dt*v_3
    state_1.time = t_1 + change_t
    state_1.vel = v_1 + change_v
    state_1.alt = z_1 + change_z
    cdef double v_4 = state_1.vel
    cdef double a_4 = state_1.net_accel()

    # NEXT STATE
    # next_state = copy.deepcopy(in_state)
    change_t = dt
    change_v = dt * (a_1/6. + a_2/3. + a_3/3. + a_4/6.)
    change_z = dt * (v_1/6. + v_2/3. + v_3/3. + v_4/6.)
    state_1.time = t_1 + change_t
    state_1.vel = v_1 + change_v
    state_1.alt = z_1 + change_z
    state_1.acc = state_1.net_accel()

    return state_1


def run_simulation(state_0, double dt=0.01):
    # Given initial state, will carry out a simulation and return a numpy array
    # of State class instances for use in post-processing and data analysis.
    cdef double time_start = time.time()
    # plan
    # given current state
    cdef double altitude = state_0.alt
    current_state = state_0

    # storage array
    state_record = np.array([state_0])
    cdef double apogee = 0
    cdef double time_apogee = 0

    while altitude >= 0:
        next_state = rk4_step(current_state, dt)
        altitude = next_state.alt
        # if condition to find max altitude and corresponding time
        # if altitude >= apogee:
            # apogee = np.round(altitude, 1)
            # time_apogee = np.round(next_state.time, 1)
        if altitude >= 0:
            current_state = next_state
            state_record = np.append(state_record, current_state)

    # time_total = np.round(current_state.time, 1)
    cdef double sim_time = time.time() - time_start

    return state_record, sim_time