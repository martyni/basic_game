from datetime import datetime

class Base(object):
   verbose = True
   def log(self, name, message):
      if self.verbose:
         print "{}:{}:{}".format(
            datetime.utcnow(), 
            name, 
            message
         )
      return message
  
