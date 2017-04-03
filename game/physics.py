from numpy import array


class physics_object(object):
   def __init__(self, x, y, z=None, mass=1, speed=array(0,0,0)):
       self.x = x
       self.y = y
       self.z = z
       self.mass = mass
       self.speed = speed
       self.speed_array = [self.speed]

   def force(self, acceleration):
       return self.mass * acceleration

   def position(self, time, speed=None):
       if not speed:
          speed=self.speed
       return speed * time
  
