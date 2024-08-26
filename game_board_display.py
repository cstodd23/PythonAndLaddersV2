import pygame
import math
from logger_setup import func_logger, logger
import os

pygame.init()
pygame.font.init()

width = 200
height = 200

screen = pygame.display.set_mode((1500, 1500))

current_path = os.path.dirname(__file__)
sprites_path = os.path.join(current_path, 'sprites')
image_path = os.path.join(sprites_path, 'computer.jpg')
image = pygame.image.load(image_path).convert_alpha()
image = pygame.transform.scale(image, (width, height))

def place(x,y):
    screen.blit(image, x,y)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(image, (750, 750))
    pygame.display.flip()

pygame.quit()