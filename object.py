from math import dist
import pygame

class Object:

    sfx = []

    def __init__(self, rect, mass, color, vel, auto_scale=False, unmovable=False):
        self.rect = rect
        self.mass = mass
        self.color = color
        self.vel = vel
        self.new_vel = self.vel.copy()
        self.unmovable = unmovable

        if auto_scale:
            self.rect.w = self.rect.h = mass / 2 # maybe sqrt or something

    def move(self, objects):
        for i in range(2):
            if i == 1: continue
            self.rect[i] += self.vel[i]

    def update(self, objects):
        for i in range(2):
            for obj in objects:
                if obj is self:
                    continue
                elif self.rect.colliderect(obj.rect):
                    m1, m2 = self.mass, obj.mass
                    r = m2 / m1
                    # v1, v2 = self.vel[i], obj.vel[i]
                    v1, v2 = self.new_vel[i], obj.vel[i]


                    if m1 == -1:
                        continue
                    elif m2 == -1:
                        # flip better
                        self.new_vel[i] = 1 * (-self.vel[i] + obj.vel[i])
                        continue

                    self.new_vel[i] = (1-r)/(r+1) * v1 + 2*r/(1+r) * v2

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


    @staticmethod
    def uncollide_rects(i, obj_1, obj_2):
        if i == 0:
            # v1, v2 = -obj_1.vel[i], -obj_2.vel[i]
            # x = (obj_2.rect.left - obj_1.rect.right) / (v2 - v1)
            # print(f'{obj_1=} {obj_2=}')
            # print(obj_2.rect.left - obj_1.rect.right, 'ahem')
            # print(x, 'x')
            # edge = obj_1.rect.right * v1 * x

            if obj_1.unmovable:
                edge = obj_1.rect.right
            else:
                edge = obj_2.rect.left

            if not obj_1.unmovable:
                obj_1.rect.right = edge
            if not obj_2.unmovable:
                obj_2.rect.left = edge
            # print(pygame.FRect.colliderect(obj_1.rect, obj_2.rect), '<-')

    @property
    def energy(self):
        return self.mass * self.vel[0] ** 2

    def uncollide(self, objects):
        play_sound = False
        for i in range(2):
            if i == 1: continue

            for obj in objects:
                if obj is self:
                    continue

                elif self.rect.colliderect(obj.rect):

                    if self.vel[i] == obj.vel[i]:
                        continue
                    play_sound = True

                    if self.vel[i] * obj.vel[i] <= 0:
                        # Head on collision / dynamic and static
                        print('[head on]')
                        if self.vel[i] > 0:
                            obj_1, obj_2 = self, obj
                        elif self.vel[i] < 0:
                            print('left')
                            obj_1, obj_2 = obj, self
                        else:
                            if obj.vel[i] > 0:
                                obj_1, obj_2 = obj, self
                            else:
                                obj_1, obj_2 = self, obj
                                print('left')

                    
                    elif self.vel[i] > 0 and obj.vel[i] > 0:
                        print('[both right]')

                        if self.vel[i] > obj.vel[i]:
                            obj_1, obj_2 = self, obj
                        else:
                            obj_1, obj_2 = obj, self

                    elif self.vel[i] < 0 and obj.vel[i] < 0:

                        if self.vel[i] > obj.vel[i]:
                            obj_1, obj_2 = self, obj
                        else:
                            obj_1, obj_2 = obj, self

                    # print(f'{obj_1=} {obj_2=}')

                    self.uncollide_rects(i, obj_1, obj_2)

        collision_strength = dist(self.vel, self.new_vel) / 5
        # if collision_strength: print(collision_strength)
        if play_sound:
            i = min(int(collision_strength), 3)
            Object.sfx[i].set_volume(collision_strength / 2)
            Object.sfx[i].play()

        self.vel = self.new_vel.copy()

    @staticmethod
    def blit_text(surf, font, txt, pos=(0, 0), color=(255, 255, 255), y_spacing=4):
        x, y = pos
        for line in txt.split('\n'):
            img = font.render(line, True, color)
            surf.blit(img, (x, y) )
            y += img.get_height() + y_spacing

    def blit(self, surf, font):

        # self.blit_text(surf, font, f'{round(self.vel[0], 4)}', pos=(self.rect[0], self.rect[1] - 8))
        text = f'''E: {round(self.energy)}
{(round(self.vel[0]), round(self.vel[1]))}'''
        self.blit_text(surf, font, text, pos=(self.rect[0], self.rect[1] - 20))
        pygame.draw.rect(surf, self.color, self.rect)

    def __repr__(self):
        if self.rect.w == 20:
            return 'MOUSE'
        else:
            return f'{self.rect}'
