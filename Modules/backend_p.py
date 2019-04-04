import math

def drag(density,velocity,area,Cd):
    D = 0.5 * density * velocity**2 * area * Cd
    return D

def C_d(M):
    M = abs(M)
    if M == 0:
        Cd = 0
        return Cd
    else:
        Cd1 = (0.5*math.exp(-2*M)*math.cos(5.5*M)) + 0.1*M*math.log(M) + 0.5
        Cd = (math.exp(-0.5*M)*Cd1) + 0.1*math.exp(M-5)
        return Cd

def pressure(p0,T0,T,L,R,g0):
    pres = p0 * ((T/T0)**(-g0/(L*R)))
    return pres

def temp(t0,L,h):
    t = t0 + L*h
    return t

def density(p,R,T):
    den = p/(R*T)
    return den

def mach(v,gamma,R,t):
    m = v/((gamma*R*t)**0.5)
    return m

def thrust(time,Thrust0,Tb):
    thrust = Thrust0*(1- (10**-5 * math.exp(  (math.log1p(10**5)    /Tb)  *time))      )
    return thrust


def g(GM,Re,h):
    grav = GM/(Re+h)**2
    return grav

def mass(m0,mf,tb,t):
    m_dot_f = mf/tb
    m = m0 - t*m_dot_f
    return m

def centre_gravity(time,burn_time,m0,xcg0,mf,xcgf,mt):
    m_rocket = m0 - mf
    m_fuel = mt - m_rocket
    if time >= burn_time:
        c_g = xcg0
    else:
        sum1 = xcg0*m_rocket + xcgf*m_fuel
        c_g = sum1/mt
    
    return c_g

def centre_pressure():
    L = 3.5
    D = 0.127
    R = D/2
    N = 4
    #nose
    Cnn = 2
    Ln = 0.7
    Xn = 0.466*Ln

    #conical transitions
    Cnt = 0
    Xt = 0

    #fin terms
    Sa = 60
    Cr = 0.25
    Ct = 0.06
    S = math.tan(90-Sa)*((Cr/2)-(Ct/2))
    Lf = ((Cr/2)-(Ct/2))/math.cos(90-Sa)

    Cnf = ( 1 + R/(S+R) )*( (3*N*((S/D)**2)) / (1 + (1+ ( (2*Lf) /(Cr+Ct) )**2)**0.5) )
    
    Xb = L - Cr
    Xr = Cr - Ct
    Xf = Xb + (Xr/3)*((Cr + 2*Ct)/(Cr+Ct)) + (1/6)*((Cr+Ct) - (Cr*Ct)/(Cr+Ct)   )

    Cnr = Cnn + Cnt + Cnf 
    
    cp = (Cnn*Xn + Cnt*Xt + Cnf*Xf)/Cnr
    
    return cp

def get_dvdt(time,height,velocity,ballast):

    #defining global variables
    rocket_area = math.pi * (0.127/2)**2
    L = -0.0065
    g0 = 9.80665
    R = 287.16
    p0 = 101325
    T0 = 288.15
    gamma = 1.4
    Thrust0 = 5800
    burn_time = 3.5
    m0 = 35 + ballast
    mf = 9
    GM = 3.986 * 10**14
    Re = 6378137
    x_cg_0 = 2.050
    x_cg_f = 2.780

    temprature = temp(T0,L,height)
    pres = pressure(p0,T0,temprature,L,R,g0)
    dens = density(pres,R,temprature)
    mach_no = mach(velocity,gamma,R,temprature)
    
    
    
    if time <= burn_time:
        m = mass(m0,mf,burn_time,time)
        f_sum = thrust(time,Thrust0,burn_time) - m*g(GM,Re,height) - drag(dens,velocity,rocket_area,C_d(mach_no))
    else:
        m = m0 - mf
        f_sum = - m*g(GM,Re,height) - drag(dens,velocity,rocket_area,C_d(mach_no))

    c_g = centre_gravity(time,burn_time,m0,x_cg_0,mf,x_cg_f,m)

    
    dvdt = f_sum/m
    
    return [dvdt,mach_no,c_g]

def simulation(ballast):
    #pre allocating
    time_step = 0.01
    burn_time = 3.5
    time = []
    velocity = []
    height = []
    dvdt = []
    mach = []
    c_g = []

    #inital conditons
    time.append(0)
    velocity.append(0)
    height.append(0)


    #computing velocity and height during burn
    i = 0
    while height[i] >= 0: 
        [dvdti,machi,c_gi] = get_dvdt(time[i],height[i],velocity[i],ballast)
        dvdt.append(dvdti)
        mach.append(machi)
        c_g.append(c_gi)
        velocity.append(velocity[i] + time_step*dvdt[i])
        height.append(height[i] + time_step*velocity[i])
        time.append(time[i] + time_step)
        i = i+1

    [dvdti,machi,c_gi] = get_dvdt(time[i],height[i],velocity[i],ballast)
    dvdt.append(dvdti)
    mach.append(machi)
    c_g.append(c_gi)
    
    return [max(height),height,velocity,dvdt,time,mach,c_g]

def simulation_target(target_altitude):
    tol = 0.1
    ballast_xi = 0
    ballast_xipos = 0.01
    f_r = 1

    while f_r > tol:
        ballast_xineg = ballast_xi
        ballast_xi = ballast_xipos
        
        fxineg = target_altitude - simulation(ballast_xineg)[0]
        fxi = target_altitude - simulation(ballast_xi)[0]
        
        ballast_xipos = ballast_xi - (fxi * (ballast_xineg - ballast_xi))/(fxineg - fxi)
        
        f_r = abs(target_altitude - simulation(ballast_xipos)[0])


    ballast = ballast_xipos
    return ballast
