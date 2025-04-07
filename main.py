import pygame
from pygame.locals import *
from object import Object
import sys

pygame.init()
SCREEN_SIZE = (800, 450)
screen = pygame.display.set_mode((SCREEN_SIZE))
clock = pygame.time.Clock()
pygame.display.set_caption('Physics test')
FPS = 144


WALL_THICKNESS = 50
objects = [
    Object(pygame.Rect(400, 200, 0, 0), 50, (0, 240, 240), [0, 0], auto_scale=True),
    # Object(pygame.Rect(700, 200, 0, 0), 20, (240, 240, 240), [-5, 0], auto_scale=True),
    Object(pygame.Rect(-WALL_THICKNESS, 0, WALL_THICKNESS, SCREEN_SIZE[1]), -1, (240, 0, 0), [0, 0]),
    Object(pygame.Rect(SCREEN_SIZE[0], 0, WALL_THICKNESS, 450), -1, (240, 0, 0), [0, 0]),
    Object(pygame.Rect(0, -WALL_THICKNESS + 50, SCREEN_SIZE[0], WALL_THICKNESS), -1, (240, 0, 0), [0, 0]),
    Object(pygame.Rect(0, -WALL_THICKNESS + SCREEN_SIZE[1], SCREEN_SIZE[0], WALL_THICKNESS), -1, (240, 0, 0), [0, 0]),
]



mouse_obj = Object(pygame.Rect(0, 0, 1, 1), -1, (0, 0, 0), [0, 0])
mx_old, my_old = None, None

sfx = []
for i in range(5):
    sound = pygame.mixer.Sound(f'sfx/collision_{i}.wav')
    sfx.append(sound)
Object.sfx = sfx

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    screen.fill((10, 10, 10))

    if mx_old is None:
        mx_old, my_old = pygame.mouse.get_pos()
    else:
        mx_old, my_old = mx, my
    mx, my = pygame.mouse.get_pos()
    mouse_obj.rect.x, mouse_obj.rect.y = mx, my
    mouse_obj.vel = [mx_old - mx, my_old - my]

    all_objects = objects + [ mouse_obj ]
    for obj in objects:
        obj.move(all_objects)
    for obj in objects:
        obj.update(all_objects)
    for obj in objects:
        obj.uncollide(all_objects)
        obj.blit(screen)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()
