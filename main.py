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

FONTS = {
    'basic': pygame.font.Font('dogica/TTF/dogica.ttf', 16),
    'small': pygame.font.Font('dogica/TTF/dogica.ttf', 8),
}


WALL_THICKNESS = 100_000
WALL_COLORS = (100, 0, 0)
OFFSET = 10
objects = [
    # Object(pygame.FRect(200, 200, 20, 20), 10, (0, 240, 240), [0, 0], auto_scale=False),
    # Object(pygame.FRect(250, 200, 20, 20), 10, (0, 240, 240), [0, 0], auto_scale=False),
    # Object(pygame.FRect(300, 200, 20, 20), 10, (0, 240, 240), [0, 0], auto_scale=False),
    # Object(pygame.FRect(350, 200, 20, 20), 10, (0, 240, 240), [0, 0], auto_scale=False),
    # Object(pygame.FRect(400, 200, 20, 20), 10, (0, 240, 240), [0, 0], auto_scale=False),
    # Object(pygame.FRect(450, 200, 50, 50), 1000, (0, 0, 240), [0, 0], auto_scale=False),
    # Object(pygame.FRect(200, 200, 50, 50), 10, (0, 240, 0), [0, 0], auto_scale=False),
    # Object(pygame.FRect(700, 200, 0, 0), 20, (240, 240, 240), [-5, 0], auto_scale=True),

    Object(pygame.FRect(-WALL_THICKNESS + OFFSET, 0, WALL_THICKNESS, SCREEN_SIZE[1]), -1, WALL_COLORS, [0, 0], unmovable=True),
    Object(pygame.FRect(SCREEN_SIZE[0] - OFFSET, 0, WALL_THICKNESS, 450), -1, WALL_COLORS, [0, 0], unmovable=True),
    Object(pygame.FRect(0, -WALL_THICKNESS + OFFSET, SCREEN_SIZE[0], WALL_THICKNESS), -1, WALL_COLORS, [0, 0], unmovable=True),
    Object(pygame.FRect(0, SCREEN_SIZE[1] - OFFSET, SCREEN_SIZE[0], WALL_THICKNESS), -1, WALL_COLORS, [0, 0], unmovable=True),
]

# for i in range(10):
#     mass = 10
#     objects.append(
#         Object(pygame.FRect(100 + i*50, 200 + i * 10, 40, 40), mass , (0,0,0), [0, 0], auto_scale=True)
#     )
#
objects.append(Object(pygame.FRect(600, 200, 40, 40), 100, (0,0,0), [0, 0], auto_scale=True))

pygame.mouse.set_visible(False)
# pygame.mouse.set_cursor()
mouse_obj = Object(pygame.FRect(0, 0, 20, 20), -1, (255, 255, 255), [0, 0], unmovable=True)
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
    mouse_obj.new_vel = [mx - mx_old, my - my_old]
    # mouse_obj.vel = [mx-mx_old, my-my_old]

    energy = 0
    energy_mouse = 0
    all_objects = objects + [ mouse_obj ]
    for obj in all_objects:
        obj.move(all_objects)
    for obj in all_objects:
        obj.update(all_objects)
    for obj in all_objects:
        energy_mouse += obj.energy
        if obj != mouse_obj:
            energy += obj.energy
        obj.uncollide(all_objects)
        obj.blit(screen, FONTS['small'])

    Object.blit_text(screen, FONTS['basic'], f'''
FPS =    {round(clock.get_fps())}
Energy = {round(energy_mouse)}
    ''')


    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()
