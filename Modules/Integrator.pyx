import numpy as np
cimport numpy as np
import Gravity
import Drag
import Thrust

DTYPE = np.double
ctypedef np.double_t DTYPE_t


cdef double sysF(h, v, t):
  m = 25 - Thrust.getFuelBurned(t)
  #print(Thrust.getForce(t), Drag.getForce(h, v), Gravity.getForce(m, h))
  return (Thrust.getForce(t) - Drag.getForce(h, v) - Gravity.getForce(m, h))/m

def integrateHeun(timeStep):
  # Write your integrator here!
  cdef double dt = timeStep
  t = np.arange(0, 120, dt)
  v = np.zeros(t.shape[0])
  s = np.zeros(t.shape[0])

  cdef int i = 0
  while v[i] > 0 or i == 0:
    #s[i+1] = s[i] + dt*v[i]
    #v[i+1] = v[i] + dt*sysF(s[i], v[i], t[i])

    #Calculate k1 values
    s_k1 = v[i]
    v_k1 = sysF(s[i], v[i], t[i])

    #Step forward
    s[i+1] = s[i] + dt*s_k1
    v[i+1] = v[i] + dt*v_k1

    #Calculate k2 values
    s_k2 = v[i+1]
    v_k2 = sysF(s[i+1], v[i+1], t[i+1])

    # x_i+1 = x_1 + dt(k1 + k2)/2
    s[i+1] = s[i] + dt*(s_k1 + s_k2)/2
    v[i+1] = v[i] + dt*(v_k1 + v_k2)/2

    i += 1 # step

  t = t[:i+1]
  v = v[:i+1]
  s = s[:i+1]

  return (t, s, v)
