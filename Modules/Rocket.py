# This is an example of a pure Python class
import numpy as np

class RocketClass():
  # Every class needs to be initialised in some way
  # We will use it to provide some default values
  def __init__(self):
    self.mass = 1
    self.area = 0.012666768698
    self.peakThrust = 5800
    self.tBurnout = 3.5
    self.mass0 = 35
    self.fuelMass = 9
    self.massFinal = self.mass0 - self.fuelMass
    self.xcgProp = 2.78
    self.xcgRocket = 2.05

  # This is an example of using a Python @property decorator
  # It lets you perform some operations every time Rocket.area is accessed
  # Can you think of a way to take advantage of this?
  @property 
 # def area(self):
     #self.area = np.pi*(0.127/2)**2
     #return self.area

  @property
  def getMass(self, state):
    # Should you update the mass here or somewhere else?
    # Do you need more arguments to this function?
    # Is it a good idea to use the @property decorator here?
    self.mass = self.mass0 - (self.fuelMass/self.tBurnout)*state.currentTime
    return self.mass