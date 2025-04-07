from math import dist
import pygame

class Object:

    sfx = []

    def __init__(self, rect, mass, color, vel, auto_scale=False):
        self.rect = rect
        self.mass = mass
        self.color = color
        self.vel = vel
        self.new_vel = self.vel.copy()

        if auto_scale:
            self.rect.w = self.rect.h = mass / 2 # maybe sqrt or something

    def move(self, objects):
        for i in range(2):
            self.rect[i] += self.vel[i]

    def update(self, objects):
        for i in range(2):
            for obj in objects:
                if obj is self:
                    continue
                elif self.rect.colliderect(obj.rect):
                    m1, m2 = self.mass, obj.mass
                    r = m2 / m1
                    # v1, v2 = abs(self.vel[i]), abs(obj.vel[i])
                    # v1, v2 = abs(self.new_vel[i]), abs(obj.vel[i])
                    v1, v2 = self.vel[i], obj.vel[i]

                    if m1 == -1:
                        continue
                    elif m2 == -1:
                        self.new_vel[i] = -self.vel[i] - obj.vel[i]
                        continue

                    # if v1 * m1 == v2 * m2:
                    #     direction = 0
                    # elif v1 * m1 > v2 * m2:
                    #     direction = v1 / self.vel[i]
                    # else:
                    #     direction = v2 / obj.vel[i]

                    # self.new_vel[i] = (m1*v1 - m2*(v1-2*v2) ) / (m1 + m2)
                    self.new_vel[i] = (1-r)/(r+1) * v1 + 2*r/(1+r) * v2
                    
                    # self.new_vel[i] = direction * (m1*v1 - m2*(v1-2*v2) ) / (m1 + m2)
                    if self.color[0] == 0:
                        col = 'BLUE'
                    else:
                        col = 'WHITE'
                    print(f'''
[{col}] speed {self.vel[i]} -> {self.new_vel[i]}
    {v1*m1=}; {v2*m2=}
    {self.vel[i]=}; {obj.vel[i]=}''')

                    # if direction > 0:
                    #     self.new_vel[i] = self.new_vel[i] + 2 * m2 / (m2 + m1)
                    # elif direction < 0:
                    #     self.new_vel[i] = self.new_vel[i] - 2 * m2 / (m2 + m1)
                    # else:
                    #     self.new_vel[i] = 0


    def uncollide(self, objects):
        play_sound = False
        for i in range(2):
            for obj in objects:
                if obj is self:
                    continue
                elif self.rect.colliderect(obj.rect):

                    if i == 0:
                        if self.vel[i] > 0:
                            self.rect.right = obj.rect.left
                            play_sound = True
                        elif self.vel[i] < 0:
                            self.rect.left = obj.rect.right
                            play_sound = True
                    else:
                        if self.vel[i] > 0:
                            self.rect.bottom = obj.rect.top
                            play_sound = True
                        elif self.vel[i] < 0:
                            self.rect.top = obj.rect.bottom
                            play_sound = True

        collision_strength = dist(self.vel, self.new_vel) / 5
        # if collision_strength: print(collision_strength)
        if play_sound:
            i = min(int(collision_strength), 3)
            Object.sfx[i].set_volume(collision_strength / 2)
            Object.sfx[i].play()

        self.vel = self.new_vel.copy()


    def blit(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)
