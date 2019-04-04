import math

cdef float drag(float density,float velocity,float area,float Cd):
    cdef float D = 0.5 * density * velocity**2 * area * Cd
    return D

cdef float C_d(float M):
    M = abs(M)
    cdef float Cd
    cdef float Cd1
    if M == 0:
        Cd = 0
        return Cd
    else:
        Cd1 = (0.5*math.exp(-2*M)*math.cos(5.5*M)) + 0.1*M*math.log(M) + 0.5
        Cd = (math.exp(-0.5*M)*Cd1) + 0.1*math.exp(M-5)
        return Cd

cdef float pressure(float p0,float T0,float T,float L,float R,float g0):
    cdef float pres = p0 * ((T/T0)**(-g0/(L*R)))
    return pres

cdef float temp(float t0,float L,float h):
    cdef float t = t0 + L*h
    return t

cdef float density(float p,float R,float T):
    cdef float den = p/(R*T)
    return den

cdef float mach(float v,float gamma,float R,float t):
    cdef float m = v/((gamma*R*t)**0.5)
    return m

cdef float thrust(float time,float Thrust0,float Tb):
    cdef float thrust = Thrust0*(1- (10**-5 * math.exp(  (math.log1p(10**5)    /Tb)  *time))      )
    return thrust


cdef float g(float GM,float Re,float h):
    cdef float grav = GM/(Re+h)**2
    return grav

cdef float mass(float m0,float mf,float tb,float t):
    cdef float m_dot_f = mf/tb
    cdef float m = m0 - t*m_dot_f
    return m

cdef float centre_gravity(float time,float burn_time,float m0,float xcg0,float mf,float xcgf,float mt):
    cdef float m_rocket = m0 - mf
    cdef float m_fuel = mt - m_rocket

    cdef float c_g
    cdef float sum1
    
    if time >= burn_time:
        c_g = xcg0
    else:
        sum1 = xcg0*m_rocket + xcgf*m_fuel
        c_g = sum1/mt
    
    return c_g

cpdef centre_pressure():
    cdef float L = 3.5
    cdef float D = 0.127
    cdef float R = D/2
    cdef int N = 4
    #nose
    cdef int Cnn = 2
    cdef float Ln = 0.7
    cdef float Xn = 0.466*Ln

    #conical transitions
    cdef int Cnt = 0
    cdef int Xt = 0

    #fin terms
    cdef int Sa = 60
    cdef float Cr = 0.25
    cdef float Ct = 0.06
    cdef float S = math.tan(90-Sa)*((Cr/2)-(Ct/2))
    cdef float Lf = ((Cr/2)-(Ct/2))/math.cos(90-Sa)

    cdef float Cnf = ( 1 + R/(S+R) )*( (3*N*((S/D)**2)) / (1 + (1+ ( (2*Lf) /(Cr+Ct) )**2)**0.5) )
    
    cdef float Xb = L - Cr
    cdef float Xr = Cr - Ct
    cdef float Xf = Xb + (Xr/3)*((Cr + 2*Ct)/(Cr+Ct)) + (1/6)*((Cr+Ct) - (Cr*Ct)/(Cr+Ct)   )

    cdef float Cnr = Cnn + Cnt + Cnf 
    
    cdef float cp = (Cnn*Xn + Cnt*Xt + Cnf*Xf)/Cnr
    
    return cp

cdef list get_dvdt(float time,float height,float velocity,float ballast):

    #defining global variables
    cdef float rocket_area = math.pi * (0.127/2)**2
    cdef float L = -0.0065
    cdef float g0 = 9.80665
    cdef float R = 287.16
    cdef float p0 = 101325
    cdef float T0 = 288.15
    cdef float gamma = 1.4
    cdef float Thrust0 = 5800
    cdef float burn_time = 3.5
    cdef float m0 = 35 + ballast
    cdef int mf = 9
    cdef float GM = 3.986 * 10**14
    cdef float Re = 6378137
    cdef float x_cg_0 = 2.050
    cdef float x_cg_f = 2.780

    cdef float temprature = temp(T0,L,height)
    cdef float pres = pressure(p0,T0,temprature,L,R,g0)
    cdef float dens = density(pres,R,temprature)
    cdef float mach_no = mach(velocity,gamma,R,temprature)
    
    cdef float m
    cdef float f_sum
    
    if time <= burn_time:
        m = mass(m0,mf,burn_time,time)
        f_sum = thrust(time,Thrust0,burn_time) - m*g(GM,Re,height) - drag(dens,velocity,rocket_area,C_d(mach_no))
    else:
        m = m0 - mf
        f_sum = - m*g(GM,Re,height) - drag(dens,velocity,rocket_area,C_d(mach_no))

    cdef float c_g = centre_gravity(time,burn_time,m0,x_cg_0,mf,x_cg_f,m)

    
    cdef float dvdt = f_sum/m
	
    
    return [dvdt,mach_no,c_g]

cpdef list simulation(float ballast):
    #pre allocating
    cdef float time_step = 0.01
    cdef float burn_time = 3.5
    cdef list time = []
    cdef list velocity = []
    cdef list height = []
    cdef list dvdt = []
    cdef list mach = []
    cdef list c_g = []

    #inital conditons
    time.append(0)
    velocity.append(0)
    height.append(0)


    #computing velocity and height during burn
    cdef int i = 0
    cdef float dvdti
    cdef float machi
    cdef float c_gi
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

cpdef float simulation_target(float target_altitude):
    cdef float tol = 0.1
    cdef float ballast_xi = 0
    cdef float ballast_xipos = 0.01
    cdef float f_r = 1

    cdef float ballast_xineg
    cdef float fxineg
    cdef float fxi

    while f_r > tol:
        ballast_xineg = ballast_xi
        ballast_xi = ballast_xipos
        
        fxineg = target_altitude - simulation(ballast_xineg)[0]
        fxi = target_altitude - simulation(ballast_xi)[0]
        
        ballast_xipos = ballast_xi - (fxi * (ballast_xineg - ballast_xi))/(fxineg - fxi)
        
        f_r = abs(target_altitude - simulation(ballast_xipos)[0])


    cdef float ballast = ballast_xipos
    return ballast
