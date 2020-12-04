from pico2d import *
from FRAMEWORK import DataManager
from INGAME import Damage_Parser

Projectiles = []

debug = False

def createProjectile(type, pos, mag, dmg, time, dy=-0.1):
    if type == 'explosion':
        Projectiles.append(Explosion(pos, mag, dmg, time))
    elif type == 'thunder':
        Projectiles.append(Thunder(pos, mag, dmg, time))
    elif type == 'meteor':
        Projectiles.append(Meteor(pos, mag, dmg, time, dy))
    elif type == 'fireball':
        Projectiles.append(Fireball(pos, mag, dmg, time, dy))

class Explosion:
    def __init__(self, pos, mag, dmg, time):
        self.x, self.y = pos
        self.mag = mag
        self.time = time
        self.frame = 0
        self.ad = dmg
        self.attackRange = 0, 0, 0, 0

    def draw(self):
        if debug:
            draw_rectangle(*self.attackRange)

        try:
            image = DataManager.load('res/Effect/Frames/1_' + str(self.frame) + '.png')
            image.draw(self.x, self.y, image.w * self.mag, image.h * self.mag)
        except:
            pass

    def update(self, chr):
        self.frame = int((get_time() - self.time) * 20)
        if self.frame >= 32:
            for i in Projectiles:
                if i == self:
                    Projectiles.remove(self)
                    return

        if 0 <= self.frame <= 10:
            self.attackRange = self.x - 12 * self.mag, self.y - 25 * self.mag, self.x + 12 * self.mag, self.y
        else:
            self.attackRange = 0, 0, 0, 0
        self.attackCheck(chr)

    def attackCheck(self, chr):
        if self.attackRange == (0, 0, 0, 0): return

        def check():
            HIT = False
            cLeft  = min(chr.hitBox[0], chr.hitBox[2])
            cRight = max(chr.hitBox[0], chr.hitBox[2])
            cTop   = max(chr.hitBox[1], chr.hitBox[3])
            cBot   = min(chr.hitBox[1], chr.hitBox[3])

            mLeft  = min(self.attackRange[0], self.attackRange[2])
            mRight = max(self.attackRange[0], self.attackRange[2])
            mTop   = max(self.attackRange[1], self.attackRange[3])
            mBot   = min(self.attackRange[1], self.attackRange[3])

            # 공격범위의 한 점이 캐릭터의 피격박스 안에 있는 경우
            if cLeft < mLeft  < cRight and cBot < mTop < cTop: HIT = True
            if cLeft < mLeft  < cRight and cBot < mBot < cTop: HIT = True
            if cLeft < mRight < cRight and cBot < mTop < cTop: HIT = True
            if cLeft < mRight < cRight and cBot < mBot < cTop: HIT = True

            # 캐릭터의 피격 박스의 한 점이 공격범위 안에 있는 경우
            if mLeft < cLeft < mRight  and mBot < cTop < mTop: HIT = True
            if mLeft < cLeft < mRight  and mBot < cBot < mTop: HIT = True
            if mLeft < cRight < mRight and mBot < cTop < mTop: HIT = True
            if mLeft < cRight < mRight and mBot < cBot < mTop: HIT = True

            # 피격 박스와 공격 범위가 포개어져있는 경우
            if  mLeft < cLeft < mRight and mLeft < cRight < mRight and \
                (cBot < mTop < cTop or cBot < mBot < cTop):
                HIT = True

            return HIT and chr.state != 'die' and chr.invincible_time <= 0

        if check():
            Damage_Parser.mob_attack_chr(self, chr, True)

class Thunder:
    def __init__(self, pos, mag, dmg, time):
        self.x, self.y = pos
        self.mag = mag
        self.time = time
        self.frame = 0
        self.ad = dmg
        self.attackRange = 0, 0, 0, 0

    def draw(self):
        if debug:
            draw_rectangle(*self.attackRange)

        try:
            image = DataManager.load('res/Effect/Thunder/' + str(self.frame) + '.png')
            image.draw(self.x, self.y, image.w * self.mag, image.h * self.mag)
        except:
            pass

    def update(self, chr):
        self.frame = int((get_time() - self.time) * 20)
        if self.frame >= 6:
            for i in Projectiles:
                if i == self:
                    Projectiles.remove(self)
                    return

        if 2 <= self.frame <= 4:
            self.attackRange = self.x - 3 * self.mag, self.y - 300 * self.mag, self.x + 3 * self.mag, self.y + 300
        else:
            self.attackRange = 0, 0, 0, 0
        self.attackCheck(chr)

    def attackCheck(self, chr):
        if self.attackRange == (0, 0, 0, 0): return

        def check():
            HIT = False
            cLeft  = min(chr.hitBox[0], chr.hitBox[2])
            cRight = max(chr.hitBox[0], chr.hitBox[2])
            cTop   = max(chr.hitBox[1], chr.hitBox[3])
            cBot   = min(chr.hitBox[1], chr.hitBox[3])

            cCenterX = (cLeft + cRight) / 2
            cCenterY = (cTop + cBot) / 2

            mLeft  = min(self.attackRange[0], self.attackRange[2])
            mRight = max(self.attackRange[0], self.attackRange[2])
            mTop   = max(self.attackRange[1], self.attackRange[3])
            mBot   = min(self.attackRange[1], self.attackRange[3])

            # 공격범위의 한 점이 캐릭터의 피격박스 안에 있는 경우
            if cLeft < mLeft  < cRight and cBot < mTop < cTop: HIT = True
            if cLeft < mLeft  < cRight and cBot < mBot < cTop: HIT = True
            if cLeft < mRight < cRight and cBot < mTop < cTop: HIT = True
            if cLeft < mRight < cRight and cBot < mBot < cTop: HIT = True

            # 캐릭터의 피격 박스의 한 점이 공격범위 안에 있는 경우
            if mLeft < cLeft < mRight  and mBot < cTop < mTop: HIT = True
            if mLeft < cLeft < mRight  and mBot < cBot < mTop: HIT = True
            if mLeft < cRight < mRight and mBot < cTop < mTop: HIT = True
            if mLeft < cRight < mRight and mBot < cBot < mTop: HIT = True

            # 피격 박스와 공격 범위가 포개어져있는 경우
            if  mLeft < cLeft < mRight and mLeft < cRight < mRight and \
                (cBot < mTop < cTop or cBot < mBot < cTop):
                HIT = True

            # 캐릭터의 중점이 공격범위 안에 있는 경우
            if mLeft < cCenterX < mRight and mBot < cCenterY < mTop: HIT = True

            return HIT and chr.state != 'die' and chr.invincible_time <= 0

        if check():
            Damage_Parser.mob_attack_chr(self, chr, True)

class Meteor:
    def __init__(self, pos, mag, dmg, time, dy):
        self.x, self.y = pos
        self.dy = dy
        self.ddy = -0.2
        self.mag = mag
        self.time = time
        self.frame = 0
        self.ad = dmg

        self.attackRange = 0, 0, 0, 0

    def draw(self):
        try:
            image = DataManager.load('res/Effect/Fire/1_' + str(self.frame) + '.png')
            image.draw(self.x, self.y, image.w * self.mag, image.h * self.mag)
        except:
            pass

        if debug:
            draw_rectangle(*self.attackRange)

    def update(self, chr):
        self.y += self.dy
        self.dy += self.ddy
        self.frame = int((get_time() - self.time) * 20)
        self.frame %= 120

        if self.y < 0:
            for i in Projectiles:
                if i == self:
                    Projectiles.remove(self)
                    return

        self.attackRange = self.x - (12 * self.mag), self.y - (15 * self.mag), self.x + (2 * self.mag), self.y
        self.attackCheck(chr)

    def attackCheck(self, chr):
        if self.attackRange == (0, 0, 0, 0): return

        def check():
            HIT = False
            cLeft  = min(chr.hitBox[0], chr.hitBox[2])
            cRight = max(chr.hitBox[0], chr.hitBox[2])
            cTop   = max(chr.hitBox[1], chr.hitBox[3])
            cBot   = min(chr.hitBox[1], chr.hitBox[3])

            mLeft  = min(self.attackRange[0], self.attackRange[2])
            mRight = max(self.attackRange[0], self.attackRange[2])
            mTop   = max(self.attackRange[1], self.attackRange[3])
            mBot   = min(self.attackRange[1], self.attackRange[3])

            # 공격범위의 한 점이 캐릭터의 피격박스 안에 있는 경우
            if cLeft < mLeft  < cRight and cBot < mTop < cTop: HIT = True
            if cLeft < mLeft  < cRight and cBot < mBot < cTop: HIT = True
            if cLeft < mRight < cRight and cBot < mTop < cTop: HIT = True
            if cLeft < mRight < cRight and cBot < mBot < cTop: HIT = True

            # 캐릭터의 피격 박스의 한 점이 공격범위 안에 있는 경우
            if mLeft < cLeft < mRight  and mBot < cTop < mTop: HIT = True
            if mLeft < cLeft < mRight  and mBot < cBot < mTop: HIT = True
            if mLeft < cRight < mRight and mBot < cTop < mTop: HIT = True
            if mLeft < cRight < mRight and mBot < cBot < mTop: HIT = True

            # 피격 박스와 공격 범위가 포개어져있는 경우
            if  mLeft < cLeft < mRight and mLeft < cRight < mRight and \
                (cBot < mTop < cTop or cBot < mBot < cTop):
                HIT = True

            return HIT and chr.state != 'die' and chr.invincible_time <= 0

        if check():
            Damage_Parser.mob_attack_chr(self, chr, True)

class Fireball:
    def __init__(self, pos, mag, dmg, time, dx):
        self.x, self.y = pos
        self.dx = dx
        self.mag = mag
        self.time = time
        self.frame = 0
        self.ad = dmg

        self.attackRange = 0, 0, 0, 0

    def draw(self):
        try:
            image = DataManager.load('res/Effect/Fireball/1_' + str(self.frame) + '.png')

            if self.dx > 0:
                image.draw(self.x, self.y, image.w * self.mag, image.h * self.mag)
            else:
                image.clip_composite_draw(0, 0, image.w, image.h, 0, 'h', self.x, self.y, image.w * self.mag, image.h * self.mag,)
        except:
            pass

        if debug:
            draw_rectangle(*self.attackRange)

    def update(self, chr):
        self.x += self.dx
        self.frame = int((get_time() - self.time) * 20)
        self.frame %= 61

        if self.x < 0 or self.x > get_canvas_width():
            for i in Projectiles:
                if i == self:
                    Projectiles.remove(self)
                    return

        if self.dx > 0:
            self.attackRange = self.x + (20 * self.mag), self.y - (13 * self.mag), self.x + (5 * self.mag), self.y + (2 * self.mag)
        else:
            self.attackRange = self.x - (20 * self.mag), self.y - (13 * self.mag), self.x - (5 * self.mag), self.y + (2 * self.mag)
        self.attackCheck(chr)

    def attackCheck(self, chr):
        if self.attackRange == (0, 0, 0, 0): return

        def check():
            HIT = False
            cLeft  = min(chr.hitBox[0], chr.hitBox[2])
            cRight = max(chr.hitBox[0], chr.hitBox[2])
            cTop   = max(chr.hitBox[1], chr.hitBox[3])
            cBot   = min(chr.hitBox[1], chr.hitBox[3])

            mLeft  = min(self.attackRange[0], self.attackRange[2])
            mRight = max(self.attackRange[0], self.attackRange[2])
            mTop   = max(self.attackRange[1], self.attackRange[3])
            mBot   = min(self.attackRange[1], self.attackRange[3])

            # 공격범위의 한 점이 캐릭터의 피격박스 안에 있는 경우
            if cLeft < mLeft  < cRight and cBot < mTop < cTop: HIT = True
            if cLeft < mLeft  < cRight and cBot < mBot < cTop: HIT = True
            if cLeft < mRight < cRight and cBot < mTop < cTop: HIT = True
            if cLeft < mRight < cRight and cBot < mBot < cTop: HIT = True

            # 캐릭터의 피격 박스의 한 점이 공격범위 안에 있는 경우
            if mLeft < cLeft < mRight  and mBot < cTop < mTop: HIT = True
            if mLeft < cLeft < mRight  and mBot < cBot < mTop: HIT = True
            if mLeft < cRight < mRight and mBot < cTop < mTop: HIT = True
            if mLeft < cRight < mRight and mBot < cBot < mTop: HIT = True

            # 피격 박스와 공격 범위가 포개어져있는 경우
            if  mLeft < cLeft < mRight and mLeft < cRight < mRight and \
                (cBot < mTop < cTop or cBot < mBot < cTop):
                HIT = True

            return HIT and chr.state != 'die' and chr.invincible_time <= 0

        if check():
            Damage_Parser.mob_attack_chr(self, chr, True)