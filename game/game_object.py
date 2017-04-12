import pygame
from base import Base
from random import randint, choice
from copy import deepcopy
from pygame import gfxdraw
black = (0,0,0)
white = (255, 255,255)

class Block(pygame.sprite.Sprite, Base):
    matrix = [[1]]
    animation_array = [[0]]

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def message(self, message):
        self.log(self.__name__, message)

    def in_game_message(self, message):
        text_sur = self.font.render(str(message), 
                True,
                (0, 0, 0, 100),
                (255, 255, 255, 10)
                )
        self.window.blit(text_sur, 
                [self.rect.x + self.width, self.rect.y - self.height/2]
                    )

    def __init__(self, color, width, height, group=None, window=None, display=None, pygame=pygame, start_x=0, start_y=0):
       self.__name__ = "Block"
       self.width = width
       self.height = height
       self.start_x = start_x
       self.start_y = start_y
       self.frame = 0
       self.countdown = 0
       self.animation_speed = 3
       self.step_size = 4
       self.window = window
       self.display = display
       self.old_position = None
       # Call the parent class (Sprite) constructor
       self.pygame = pygame
       #self.pygame.font.init()
       self.font1 = self.pygame.font.Font('fonts/AlumFreePromotional.ttf', self.height)
       self.font2 = self.pygame.font.Font('fonts/AlumFreePromotional2.ttf', self.height)
       self.fonts = [self.font1,self.font2]
       self.font = self.fonts[0]
       self.pygame.sprite.Sprite.__init__(self)
       self.draw_self()
       self.directions = {
            "up": self.move_up,
            "down": self.move_down,       
            "left": self.move_left,
            "right": self.move_right,
            "none": self.move_none
       }
       self.rect.x = self.start_x
       self.rect.y = self.start_y
       if group is not None:
           self.group = group
       else:
           self.group = Block_group()
           
       #self.group = group if group else Block_group()
       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.add(self.group)

    def move_up(self):
        self.rect.y -= self.step_size
      
    def move_down(self):
        self.rect.y += self.step_size

    def move_right(self):
        self.rect.x += self.step_size

    def move_left(self):
        self.rect.x -= self.step_size

    def move_none(self):
        pass

    def move_randomly(self):
        if not self.countdown:
           self.next_move = choice([i for i in self.directions.iterkeys()] + ["none"] * 5)
           self.countdown = self.line_of_site/10
        self.directions[self.next_move]()
        self.in_game_message(self.next_move)
        self.countdown -= 1
    '''
    def move_randomly(self):
        if not self.countdown: 
           self.randx = randint(-1,1)
           self.randy = randint(-1,1)
           self.countdown = self.line_of_site/10
           self.in_game_message("moving x: {} y: {}".format(self.randx, self.randy))
        self.check_limits()
        self.rect.y += self.randy
        self.rect.x += self.randx
        self.countdown -= 1
    '''
    def check_limits(self):
        if self.rect.x < 0:
            self.randx = 1
        if self.rect.y < 0:
            self.randy = 1


    def draw_self(self):    
       self.stand = self.pygame.Surface([self.width, self.height], self.pygame.SRCALPHA, 32)
       self.animation = self.pygame.Surface([self.width, self.height], self.pygame.SRCALPHA, 32) 
       self.x_size = len(self.matrix[0])
       self.y_size = len(self.matrix)
       self.draw_matrix(self.stand, self.matrix)
       self.draw_matrix(self.animation, self.animation_array)
       self.animations = [self.stand, self.animation]
       self.image = self.animations[0]
       
       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()
       

    def draw_matrix(self, surface, matrix):
       for y in range(len(matrix)):
           for x in range(len(matrix[y])):
               color = black if matrix[y][x] else white
               if matrix[y][x] is None:
                  color = (0,0,0,0)
               self.pygame.draw.rect(surface, 
                       color,
                       self.pygame.Rect(x * self.width/self.x_size,
                                   y * self.height/self.y_size,
                                   self.width/self.x_size,
                                   self.height/self.y_size
                                   )
                       )

    def animate(self):
       if not self.frame % self.animation_speed:
          if self.image == self.animations[0]:
             self.image = self.animations[1]
             self.font = self.fonts[1]
          elif self.image == self.animations[1]:
             self.font = self.fonts[0]
             self.image = self.animations[0] 
       self.frame += 1

    def check_position(self):
       self.position = self.rect.x, self.rect.y 
       if self.old_position:
         top_left_x, top_left_y = self.old_position
         top_left_x -= 5
         top_left_y -= 5
         self.pygame.gfxdraw.box(self.window,
               self.pygame.Rect(top_left_x, top_left_y, self.width + 10, self.height + 10),
               (255,255,255,0)
         )
       if self.position != self.old_position:
           self.animate()
       self.old_position = self.position    


    def update(self):
       self.rect.x, self.rect.y = self.pygame.mouse.get_pos() 
       self.check_position()

    def check_collision(self, sprite2):
       col = self.pygame.sprite.collide_rect(self, sprite2)
       return col

class Block_group(pygame.sprite.Group):
   pass


class Main_Player(Block):
    global target_x
    target_x = 0
    global target_y
    target_y = 0
    def update(self):
       global target_x

       global target_y
       x, y = self.pygame.mouse.get_pos()
       x -= x % self.step_size
       y -= y % self.step_size
       if y > self.rect.y:
           #self.rect.y += self.step_size
           self.move_down()
       elif y < self.rect.y:
           self.move_up()
           #self.rect.y -= self.step_size
       if x > self.rect.x:
           self.move_right()
           #self.rect.x += self.step_size
       elif x < self.rect.x:
           self.move_left()
           #self.rect.x -= self.step_size
       target_x, target_y = self.rect.x, self.rect.y 
       self.check_position()

    def draw_self(self): 
       self.stand = self.pygame.image.load("base.png")
       self.stand = self.pygame.transform.rotozoom(self.stand, 2, 2)
       self.animation = self.pygame.image.load("base.png")
       self.animation = self.pygame.transform.rotozoom(self.animation, -2, 2)
       self.animations = [self.stand, self.animation]
       self.image = self.animations[0]
       self.rect = self.image.get_rect()
       
       


class Cursor(Block):
    matrix = [
            [None, 1, None],
            [1, 1, 1],
            [None, 1, None],
            ]
    animation = [
            [1, 1, 1],
            [1, None, 1],
            [1, 1, 1],
            ]
    def update(self):
        self.rect.x, self.rect.y = self.pygame.mouse.get_pos()

class Enemy(Block):
   line_of_site = 300
   matrix = [ 
          [None, None,1,1,1,1,1,None],
          [None,1,0,0,0,0,0,1],
          [None,1,0,1,0,1,0,1],
          [None,None,1,1,1,1,1,None],
          [None,1,0,0,0,0,1,None],
          [None,1,1,0,0,1,None,1],
          [None,None,1,1,1,1,None,None],
          [None,1,None, None, None,1,None,None],
   ]
   animation_array = [
              [None, None,1,1,1,1,1,None],
              [None,1,0,0,0,0,0,1],
              [None,1,0,1,0,1,0,1],
              [None,None,1,1,1,1,1,None],
              [None,1,0,0,0,0,1,None],
              [1,None,1,0,0,1,1,None],
              [None,None,1,1,1,1,None,None],
              [None,None,1, None, None,None,1,None],
       ]
   def update(self):
      self.check_position()
      self.step_size = 1
      for sprite in self.group: 
         if self.check_collision(sprite):
            if sprite != self:
               self.in_game_message((sprite.rect.x, sprite.rect.y))
               top_left_x = sprite.rect.x if sprite.rect.x > self.rect.x else self.rect.x 
               top_left_y = sprite.rect.y if sprite.rect.y > self.rect.y else self.rect.y
               bottom_right_x  = self.rect.bottomright[0] if self.rect.bottomright[0] < sprite.rect.bottomright[0] else sprite.rect.bottomright[0]
               bottom_right_y  = self.rect.bottomright[1] if self.rect.bottomright[1] < sprite.rect.bottomright[1] else sprite.rect.bottomright[1]
               self.pygame.gfxdraw.box(self.window,
                       self.pygame.Rect(top_left_x, top_left_y, bottom_right_x - top_left_x, bottom_right_y - top_left_y),
                       (255,0,0,50)
               )
         else:
            if abs(target_y - self.rect.y + target_x - self.rect.x) > self.line_of_site:
               self.move_randomly()
               break
            if target_y > self.rect.y:
                self.move_down()
                #self.rect.y += self.step_size
            elif target_y < self.rect.y:
                #self.rect.y -= self.step_size
                self.move_up()
            if target_x > self.rect.x:
                self.move_right()
                #self.rect.x += self.step_size
            elif target_x < self.rect.x:
                self.move_left()
                #self.rect.x -= self.step_size

            self.in_game_message("I'll kill you!!")



class Tree(Block):

    matrix = [
           [None,1,1,1,1,1,1,None],
           [1,0,0,0,0,0,0,1],
           [None,1,1,0,0,1,None,None],
           [None,None,1,0,0,1,None,None],
           [None,None,None,1,1,None,None,None],
           [None,None,None,1,1,None,None,None],
           [None,None,None,1,1,None,None,None],
           [None,None,None,1,1,None,None,None],
    ]
    animation_array = [
           [None,1,1,1,1,1,1,None],
           [1,0,0,0,0,0,0,1],
           [None,1,1,0,0,1,None,None],
           [None,None,1,0,1,None,None,None],
           [None,None,None,1,1,None,None,None],
           [None,None,None,1,1,None,None,None],
           [None,None,None,1,1,None,None,None],
           [None,None,None,1,1,None,None,None],
    ]
    def update(self):
       if not self.countdown:
          self.animate()
          self.countdown = 10
       self.countdown -= 1   
