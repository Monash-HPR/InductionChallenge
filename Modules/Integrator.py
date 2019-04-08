import numpy as np 

def integrateEuler(state, mass, s, v):
    dt = np.amax(state.time)/np.size(state.time)
  
    sEst = s + dt*v
    vEst = v + dt*(state.F/mass)
    
    return (sEst, vEst)