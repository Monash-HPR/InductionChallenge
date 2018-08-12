def Gravity(H):
    GM=3.986*(10**14);
    Re=6378137;

    gravitation= GM/(Re+H)**2
    return gravitation