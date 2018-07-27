# This is an example of a pure Python class
class Rocket():
  # Every class needs to be initialised in some way
  # We will use it to provide some default values
  def __init__(self):
    self.mass = 1
    self.area = 1

  # This is an example of using a Python @property decorator
  # It lets you perform some operations every time Rocket.area is accessed
  # Can you think of a way to take advantage of this?
  @property 
  def area(self):
    return self.area


  def getMass(self):
    # Should you update the mass here or somewhere else?
    # Do you need more arguments to this function?
    # Is it a good idea to use the @property decorator here?
    return self.mass