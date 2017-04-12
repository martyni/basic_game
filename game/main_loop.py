import pygame
from base import Base
from pygame.locals import *
from colours import *
from game_object import Main_Player, Enemy, Block, Block_group, Tree, Cursor

class mygame(Base):
   def __init__(self, width=1280 , height=800):
      self.pygame = pygame
      self.__name__ = "mygame"
      self.pygame.init()
      self.pygame.font.init()
      self.width = width
      self.height = height
      self.window = self.pygame.display.set_mode( (width, height),HWSURFACE|DOUBLEBUF|RESIZABLE) 
      self.clock = self.pygame.time.Clock()
      self.running = True
      self.size = (self.width, self.height)

   def message(self, message):
      self.log(self.__name__, str(message))
 
   def quit(self):
      self.message("Quit")
      self.running = False

   def resize(self, event):
      self.new_size = event.dict['size']
      self.window=self.pygame.display.set_mode(self.new_size, HWSURFACE|DOUBLEBUF|RESIZABLE)
      x_scalar = float(self.new_size[0]) / self.size[0]
      y_scalar = float(self.new_size[1]) / self.size[1]
      for sprite in self.default_sprites:
          w = sprite.rect.w
          h = sprite.rect.h
          new_width = int(w * x_scalar)
          new_height = int(h * y_scalar)
          sprite.width = int(sprite.width * x_scalar)
          sprite.height = int(sprite.height * y_scalar)
          sprite.draw_self()
          sprite.rect = sprite.rect.fit(pygame.Rect(sprite.rect.x, sprite.rect.y, new_width, new_height))
      self.size = self.width, self.height = event.dict['size']
      self.message("Resized to {} {}".format(*self.size))

   def main(self):
      self.default_sprites = Block_group()
      self.sprite = Main_Player(RED, 48, 48, self.default_sprites, self.window, self.pygame.display, self.pygame, 500, 700)
      #self.sprite.main_player()
      self.sprite2 = Enemy(BLUE, 48, 48, self.default_sprites, self.window, self.pygame.display, self.pygame)
      self.sprite3 = Tree(BLUE, 48, 48, self.default_sprites, self.window, self.pygame.display, self.pygame, 500, 600)
      self.sprite4 = Cursor(BLUE, 16, 16, self.default_sprites, self.window, self.pygame.display, self.pygame)
      print '{} <--'.format(self.default_sprites)
      print "hi"
      pygame.mouse.set_visible(0)
      for sprite in self.sprite, self.sprite2, self.sprite3, self.sprite4:
         self.default_sprites.add(sprite)
      while self.running:
         self.window.fill(GREEN)
         for event in self.pygame.event.get():
            if event.type==QUIT: 
               self.quit()
            elif event.type==VIDEORESIZE:
               self.resize(event)
         self.default_sprites.draw(self.window)
         self.default_sprites.update()
         self.pygame.display.update([s.rect for s in self.default_sprites])
         self.clock.tick(30)
      self.pygame.quit()

def main():
   m = mygame()
   m.main()
   
   
if __name__ == "__main__":
   main()
