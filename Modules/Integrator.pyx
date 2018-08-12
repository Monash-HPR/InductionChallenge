import numpy as np 

def eulerInteg(v,s,a,dt):
    v=v+dt*a;
    s=s+dt*v;
    return [v,s];





