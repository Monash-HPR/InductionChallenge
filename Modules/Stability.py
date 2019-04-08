import numpy as np

# calculating centre of pressure
def centreOfPressure(d):
    # finding Lf
    Lf = (d.Cr/2 - d.Ct/2)/np.cos(d.sweepAngle)
    # nose
    Xn = 0.466*d.Ln
    
    # fins
    CnF = (1 + d.R/(d.S+d.R))*((4*d.numFins*(d.S/d.diameter)**2)/(1+np.sqrt(1+((2*Lf)/(d.Cr+d.Ct))**2)))
    Xb = d.L - d.Cr
    Xr = d.Cr - d.Ct
    Xf = Xb + (Xr/3)*((d.Cr+2*d.Ct)/(d.Cr+d.Ct))+(1/6)*((d.Cr+d.Ct)-(d.Cr*d.Ct)/(d.Cr+d.Ct))
    
    # total
    CnR = d.CnN + CnF
    Xcp = (d.CnN*Xn + CnF*Xf)/CnR
    return Xcp

def centreOfGravity(rocket):
    #propDist = (rocket.xcgInitial*rocket.mass0 - rocket.xcgFinal*rocket.massFinal)/rocket.fuelMass
    #Xcg = ((rocket.mass0 - rocket.mass)*propDist + rocket.xcgFinal*rocket.massFinal)/rocket.mass
    Xcg = (rocket.xcgProp*(rocket.mass0 - rocket.mass) + rocket.xcgRocket*rocket.massFinal)/rocket.mass
    return Xcg
