from pico2d import *
from FRAMEWORK import DataManager

Projectiles = []

def createProjectile(type, pos, size, time):
    if type == 'explosion':
        Projectiles.append(Explosion(pos, size, time))

class Explosion:
    def __init__(self, pos, size, time):
        self.pos = pos
        self.size = size
        self.time = time

    def draw(self):
        frame = int((get_time() - self.time) * 20)
        if frame > 32:
            for i in Projectiles:
                if i == self:
                    Projectiles.remove(self)
                    return
        image = DataManager.load('../res/Effect/Frames/1_' + str(frame) + '.png')
        image.draw(*self.pos, *self.size)

