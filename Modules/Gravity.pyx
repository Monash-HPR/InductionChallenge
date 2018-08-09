def getForce(double altitude):

  g_m = 3.986 * 10 ** 14 
  radius_earth = 6378137 # metres
  gravitation = g_m / ( ( radius_earth + altitude) ** 2)
  
  return gravitation