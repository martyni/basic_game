import game
import unittest

class BasicGameTests(unittest.TestCase):
   @classmethod
   def setUpClass(self):
      self.test_game = game.main()

   def test_game_window(self):
      self.assertTrue(self.test_game.window)  
   
   @classmethod
   def tearDownClass(self):
      self.test_game.quit()



