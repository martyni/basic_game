import yaml
import pygame
from pygame.key import *

with open('controls.yaml', 'r') as config:
    controls = yaml.load(config)


def check_controls(controls, option="default"):
    for action in controls[option]:
        if not controls[option][action]:

            controls[option][action] = get_key(action)
        print controls

def get_key(action):
    print raw_input('select key for action {}'.format(action))

if __name__ == "__main__":
    check_controls(controls)
