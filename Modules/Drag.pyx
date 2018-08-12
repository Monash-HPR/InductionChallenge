# This is an example of a pure Python function
import numpy as np
def Drag (V,H,S):
    #Defining the variables
    gamma=1.4;
    R=287.16;
    L= -0.0000065;
    t0= 288.15;
    p0=101325;
    g0=9.80665;

    #Claculating Temperature and Preassure;
    temp = t0 + (L*H);
    press = p0*((temp/t0)**(-g0/(L*R)));

    #Mach Number calcultations
    mach = V/np.sqrt(gamma*R*temp);


    #Density Calculation
    density = press/(R*temp);

    #Drag Coefficient
    dragCoeff = (np.exp(-1.2*mach)*np.sin(mach))+((mach/6)*np.log10(mach+1));

    Drag = 0.5*density*S*dragCoeff*(V**2);
    print(Drag)
    return Drag