from pico2d import *
from FRAMEWORK import DataManager
from INGAME import Ingame_state, Damage_Parser, Projectile
from random import randint
import UI

debug = False

class Monster:
    # Loading_state에서 JSON파일을 읽어서 저장
    MOB_MOTION_DATA = {}

    def __init__(self, mobId, xPos, yPos):
        ### 몬스터 이미지 관련 변수들 ###
        self.image = None                                       # 이미지
        self.xSize, self.ySize = 0, 0                           # 화면에 그려질 이미지 크기
        self.sxSize, self.sySize = 0, 0                         # 한 프레임 당 이미지 크기
        self.frame = 0                                          # 프레임
        self.timer = {}                                         # 타이머
        self.id = mobId                                         # 종류
        self.state = 'idle'                                     # 상태
        self.order = 'patrol'                                   # 명령

        ### 몬스터 좌표 관련 변수들 ###
        self.dir = 'LEFT'                                       # 좌우
        self.x, self.y = xPos, yPos                             # 좌표
        self.dx, self.dy = 0, 0                                 # 움직임속도

        ### 몬스터 피격, 공격 관련 변수들 ###
        self.hitBy = ''                                         # 어떤 공격에 맞았는지
        self.hitBox = (0, 0, 0, 0)                              # 히트박스
        self.attack_range = (0, 0, 0, 0)                        # 공격범위

        ### 몬스터 스탯 관련 변수들 ###
        self.maxHp, self.hp = 50, 50                            # 최대HP, 현재HP
        self.ad, self.df, self.speed, = 0, 0, 0                 # 공격력, 방어력, x축 추가 이동속도

        ### 몬스터 모션별 범위 변수들 :: JSON ###
        self.MOTION_YSHEET = {}
        self.MOTION_DELAY = {}
        self.MOTION_FRAME = {}
        self.MOTION_HITBOX = {}
        self.MOTION_ATTACK_RANGE = {}

    def load(self):
        self.image = DataManager.load('../res/Mob/' + str(self.id) + '/sheet.png')
        self.MOTION_YSHEET       = Monster.MOB_MOTION_DATA[str(self.id)]['YSHEET']
        self.MOTION_DELAY        = Monster.MOB_MOTION_DATA[str(self.id)]['DELAY']
        self.MOTION_FRAME        = Monster.MOB_MOTION_DATA[str(self.id)]['FRAME']
        self.MOTION_HITBOX       = Monster.MOB_MOTION_DATA[str(self.id)]['HITBOX']
        self.MOTION_ATTACK_RANGE = Monster.MOB_MOTION_DATA[str(self.id)]['ATTACK_RANGE']

        # 몹 세팅
        INFO = Monster.MOB_MOTION_DATA[str(self.id)]['INFO']
        self.xSize, self.ySize, self.sxSize, self.sySize, self.hp, self.ad, self.df, self.speed =\
            INFO['xSize'], INFO['ySize'], INFO['sxSize'], INFO['sySize'], INFO['hp'], INFO['ad'], INFO['df'], INFO['speed']

    def draw(self):
        if debug:
            draw_rectangle(self.hitBox[0], self.hitBox[1], self.hitBox[2], self.hitBox[3])
            draw_rectangle(self.attack_range[0], self.attack_range[1], self.attack_range[2], self.attack_range[3])
            UI.FONT['12'].draw(self.x, self.y + 32, self.order, (255, 255, 255))
            UI.FONT['12'].draw(self.x, self.y + 20, str(int(self.timer['order'])), (255, 255, 255))

        try:
            self.drawEffect()
        except:
            pass

        if self.state == 'none': return
        ySheet = self.MOTION_YSHEET[self.state]

        if self.dir == 'LEFT':
            self.image.clip_draw(self.frame // self.MOTION_DELAY[self.state] % self.MOTION_FRAME[self.state] * self.sxSize,
                                 self.sySize * ySheet, self.sxSize, self.sySize, self.x, self.y, self.xSize, self.ySize)
        else:
            self.image.clip_composite_draw(self.frame // self.MOTION_DELAY[self.state] % self.MOTION_FRAME[self.state] * self.sxSize,
                                           self.sySize * ySheet, self.sxSize, self.sySize, 0, 'h', self.x, self.y, self.xSize, self.ySize)

    def landingCheck(self):
        map = Ingame_state.map
        for tile in map.tileRect:
            if (tile[0] < self.hitBox[0] < tile[2] or
                tile[0] < self.hitBox[2] < tile[2] or
                tile[0] <= self.x <= tile[2]) and \
                self.hitBox[3] + self.dy * 2 <= tile[1] <= self.hitBox[3]:
                return True, tile[1] - self.MOTION_HITBOX[self.state][3]
        return False, None

    def collideCheck(self):
        map = Ingame_state.map
        mLeft  = min(self.hitBox[0], self.hitBox[2])
        mRight = max(self.hitBox[0], self.hitBox[2])
        mTop   = max(self.hitBox[1], self.hitBox[3])
        mBot   = min(self.hitBox[1], self.hitBox[3])

        mFront = abs(self.MOTION_HITBOX[self.state][0])
        mBack  = abs(self.MOTION_HITBOX[self.state][2])
        mUp    = abs(self.MOTION_HITBOX[self.state][1])
        mDown  = abs(self.MOTION_HITBOX[self.state][3])

        for tile in map.tileRect:
            RESULT = False, 0, 0, self.dx, self.dy
            tLeft, tTop, tRight, tBot = tile

            # 머리
            if (tLeft < mLeft < tRight or tile[0] < mRight < tile[2]) and \
                tBot <= mTop + self.dy <= tTop != tBot:
                RESULT = True, RESULT[1], RESULT[2] + tBot - mUp, RESULT[3], 0

            # 좌측
            if (tBot < mTop < tTop or tBot < mBot < tTop) and \
                (mLeft + self.dx < tRight < mLeft or tLeft < mLeft + self.dx < tRight):
                RESULT = True, RESULT[1] + tRight + mBack, RESULT[2], 0, RESULT[4]

            # 우측
            if (tBot < mTop < tTop or tBot < mBot < tTop) and \
                (mRight < tLeft < mRight + self.dx or tLeft < mRight + self.dx < tRight):
                RESULT = True, RESULT[1] + tLeft - mBack, RESULT[2], 0, RESULT[4]

            # 맵밖으로 나가는 것 체크
            if mLeft + self.dx < 0:
                RESULT = True, mBack, RESULT[2], 0, RESULT[4]
            elif mRight + self.dx > map.size[0]:
                RESULT = True, map.size[0] - mBack, RESULT[2], 0, RESULT[4]

            if RESULT[0]: return RESULT
        return False, None, None, None, None

    def updatePos(self, delta_time):
        self.frame += 1
        if self.frame >= self.MOTION_FRAME[self.state] * (self.MOTION_DELAY[self.state]):
            self.frame = 0
            if self.state == 'attack' or self.state == 'hit':
                self.frame = 0
                self.state = 'move'
                self.order = 'approach'
                self.order_timer = 0

            if self.state == 'die':
                Ingame_state.mob.remove(self)
                return

        # Collide Check
        isCollided, x, y, dx, dy = self.collideCheck()
        if isCollided:
            if x: self.x = x
            if y: self.y = y
            self.dx, self.dy = dx, dy

        # Landing Check
        isLanding, y = self.landingCheck()
        if isLanding:
            if self.state == 'fall':
                self.state = 'idle'
            self.y = y
            self.dy = 0
            self.timer['fall'] = 0
        else:
            dy = 0
            ti = self.timer['fall']
            while ti > 0:
                ti -= 0.1
                dy -= 0.5

            self.state = 'fall'
            self.order = 'wait'
            self.dx = 0
            self.dy = -2
            self.dy += dy
            self.timer['fall'] += delta_time

        self.x += self.dx
        self.y += self.dy

    def updateHitbox(self):
        if self.dir == 'LEFT':
            self.hitBox = (self.x + self.MOTION_HITBOX[self.state][0], self.y + self.MOTION_HITBOX[self.state][1],
                           self.x + self.MOTION_HITBOX[self.state][2], self.y + self.MOTION_HITBOX[self.state][3])
        else:
            self.hitBox = (self.x - self.MOTION_HITBOX[self.state][0], self.y + self.MOTION_HITBOX[self.state][1],
                           self.x - self.MOTION_HITBOX[self.state][2], self.y + self.MOTION_HITBOX[self.state][3])

    def hitCheck(self):
        chr = Ingame_state.chr

        def check():
            if chr.attack_range == (0, 0, 0, 0): return False

            HIT = False
            cLeft  = min(chr.attack_range[0], chr.attack_range[2])
            cRight = max(chr.attack_range[0], chr.attack_range[2])
            cTop   = max(chr.attack_range[1], chr.attack_range[3])
            cBot   = min(chr.attack_range[1], chr.attack_range[3])

            mLeft  = min(self.hitBox[0], self.hitBox[2])
            mRight = max(self.hitBox[0], self.hitBox[2])
            mTop   = max(self.hitBox[1], self.hitBox[3])
            mBot   = min(self.hitBox[1], self.hitBox[3])

            # 공격 범위의 한 점이 피격 범위 안에 있을 경우
            if (mLeft <= cLeft <= mRight and mBot <= cTop <= mTop) or \
                (mLeft <= cLeft <= mRight and mBot <= cBot <= mTop) or \
                (mLeft <= cRight <= mRight and mBot <= cTop <= mTop) or \
                (mLeft <= cRight <= mRight and mBot <= cBot <= mTop):
                HIT = True

            # 피격 범위의 한 점이 공격 범위 안에 있을 경우
            if cLeft < mLeft < cRight  and cBot < mTop < cTop: HIT = True
            if cLeft < mLeft < cRight  and cBot < mBot < cTop: HIT = True
            if cLeft < mRight < cRight and cBot < mTop < cTop: HIT = True
            if cLeft < mRight < cRight and cBot < mBot < cTop: HIT = True

            if HIT and self.hitBy != chr.state:
                return True
            else:
                return False

        if check():
            Damage_Parser.chr_attack_mob(self, chr)

    def attackCheck(self):
        chr = Ingame_state.chr

        def check():
            if self.attack_range == (0, 0, 0, 0): return

            HIT = False
            cLeft  = min(Ingame_state.chr.hitBox[0], Ingame_state.chr.hitBox[2])
            cRight = max(Ingame_state.chr.hitBox[0], Ingame_state.chr.hitBox[2])
            cTop   = max(Ingame_state.chr.hitBox[1], Ingame_state.chr.hitBox[3])
            cBot   = min(Ingame_state.chr.hitBox[1], Ingame_state.chr.hitBox[3])

            mLeft  = min(self.attack_range[0], self.attack_range[2])
            mRight = max(self.attack_range[0], self.attack_range[2])
            mTop   = max(self.attack_range[1], self.attack_range[3])
            mBot   = min(self.attack_range[1], self.attack_range[3])

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
            Damage_Parser.mob_attack_chr(self, chr)

class Mob(Monster):
    def __init__(self, mobId, xPos, yPos):
        super().__init__(mobId, xPos, yPos)
        self.timer['fall']  = 0
        self.timer['order'] = 0

    def canNoticeChr(self, chr):
        if self.state == 'attack': return False
        if self.id == 100:  # 슬라임
            if self.dir == 'LEFT' and 0 < self.x - chr.x < 150 and abs(self.y - chr.y) < 30:
                return True
            elif self.dir == 'RIGHT' and 0 < chr.x - self.x < 150 and abs(self.y - chr.y) < 30:
                return True
        elif self.id == 101:  # 가시
            if self.dir == 'LEFT' and 0 < self.x - chr.x < 150 and abs(self.y - chr.y) < 30:
                return True
            elif self.dir == 'RIGHT' and 0 < chr.x - self.x < 150 and abs(self.y - chr.y) < 30:
                return True
        elif self.id == 102:  # 쓰레기
            if self.dir == 'LEFT' and 0 < self.x - chr.x < 170 and abs(self.y - chr.y) < 30:
                return True
            elif self.dir == 'RIGHT' and 0 < chr.x - self.x < 170 and abs(self.y - chr.y) < 30:
                return True

    def canAttackChr(self, chr):
        if self.id == 100:  # 슬라임
            if self.dir == 'LEFT' and 0 < self.x - chr.x < 30 and abs(self.y - chr.y) < 10:
                return True
            elif self.dir == 'RIGHT' and 0 < chr.x - self.x < 30 and abs(self.y - chr.y) < 10:
                return True
        elif self.id == 101:  # 가시
            if abs(self.x - chr.x) < 30 and abs(self.y - chr.y) < 10: return True
        elif self.id == 102:  # 쓰레기
            if self.dir == 'LEFT' and 0 < self.x - chr.x < 50 and abs(self.y - chr.y) < 10:
                return True
            elif self.dir == 'RIGHT' and 0 < chr.x - self.x < 50 and abs(self.y - chr.y) < 10:
                return True

    def updateOrder(self, delta_time):
        if self.state == 'hit': return

        # 순찰
        if self.order == 'patrol':
            # 만약 발견 범위 안에 있다면 approach 명령
            if self.canNoticeChr(Ingame_state.chr):
                self.frame = 0
                self.order = 'approach'
                self.timer['order'] = 0

            # 2초마다 순찰 방향 바꿈
            if self.timer['order'] > 2:
                self.timer['order'] = 0
            if self.timer['order'] == 0:
                r = randint(1, 100)
                if 0 <= r < 33:
                    self.dir = 'LEFT'
                    self.state = 'move'
                    self.dx = -1
                elif 33 <= r < 66:
                    self.dir = 'RIGHT'
                    self.state = 'move'
                    self.dx = 1
                else:
                    self.state = 'idle'
                    self.dx = 0

        # 다가가기
        if self.order == 'approach':
            # 만약 발견 범위 밖에 있다면 wait 명령
            if not self.canNoticeChr(Ingame_state.chr):
                self.frame = 0
                self.order = 'wait'
                self.timer['order'] = 0

            # 만약 공격할 수 있는 거리에 있다면 attack 명령
            elif self.canAttackChr(Ingame_state.chr):
                self.frame = 0
                self.order = 'attack'
                self.timer['order'] = 0

            elif Ingame_state.chr.x - self.x < 0:
                self.dir = 'LEFT'
                self.state = 'move'
                self.dx = -1.4
            else:
                self.dir = 'RIGHT'
                self.state = 'move'
                self.dx = 1.4

        # 공격
        if self.order == 'attack':
            self.state = 'attack'
            self.dx = 0

        # 대기
        if self.order == 'wait':
            self.dx = 0
            if self.timer['order'] > 0.5:
                self.order = 'patrol'
                self.timer['order'] = 2

        self.timer['order'] += delta_time

    def updateAttackRange(self):
        self.attack_range = (0, 0, 0, 0)
        attack_start, attack_end = 0, 0
        if self.id == 100:
            attack_start = 2.3
            attack_end = 2.8
        elif self.id == 101:
            attack_start = 4
            attack_end = 6
        elif self.id == 102:
            attack_start = 4
            attack_end = 5

        if self.state == 'attack':
            if self.MOTION_DELAY[self.state] * attack_start < self.frame < self.MOTION_DELAY[self.state] * attack_end:
                if self.dir == 'RIGHT':
                    self.attack_range = (self.x + self.MOTION_ATTACK_RANGE[self.state][0], self.y + self.MOTION_ATTACK_RANGE[self.state][1],
                                         self.x + self.MOTION_ATTACK_RANGE[self.state][2], self.y + self.MOTION_ATTACK_RANGE[self.state][3])
                else:
                    self.attack_range = (self.x - self.MOTION_ATTACK_RANGE[self.state][0], self.y + self.MOTION_ATTACK_RANGE[self.state][1],
                                         self.x - self.MOTION_ATTACK_RANGE[self.state][2], self.y + self.MOTION_ATTACK_RANGE[self.state][3])

    def update(self, delta_time):
        self.updateOrder(delta_time)
        self.updatePos(delta_time)
        self.updateHitbox()
        self.updateAttackRange()
        self.hitCheck()
        self.attackCheck()

class Boss(Monster):
    def __init__(self, mobId, xPos, yPos):
        super().__init__(mobId, xPos, yPos)
        self.order = 'Chase'
        self.timer['fall']  = 0
        self.timer['order'] = 0

        self.skillCoolTime = {}
        self.skillCoolTime.update({'RapidFall' : 0})

    def changeOrder(self, order):
        self.order = order
        self.timer['order'] = 0

    def updatePosBoss(self, delta_time):
        chr = Ingame_state.chr

        # 필수
        self.frame += 1
        if self.frame >= self.MOTION_FRAME[self.state] * (self.MOTION_DELAY[self.state]):
            self.frame = 0
            if self.state == 'attack' or self.state == 'hit':
                self.frame = 0
                self.state = 'idle'
            if self.state == 'die':
                Ingame_state.mob.remove(self)
                return

        # 충돌 계산
        isCollided, x, y, dx, dy = self.collideCheck()
        isLanding, y = self.landingCheck()

        # 패턴 부분
        if self.order == 'RapidFall':
            if isLanding:
                if self.dir == 'RIGHT':
                    Projectile.createProjectile('explosion', (self.x - 5, self.y), (250, 250), get_time())
                else:
                    Projectile.createProjectile('explosion', (self.x + 5, self.y), (250, 250), get_time())
                self.changeOrder('RapidFall_After')
                self.y, self.dy = y, 0
                return

        elif self.order == 'RapidFall_After':
            self.state = 'idle'
            if self.timer['order'] > 2:
                self.changeOrder('Chase')

        elif self.order == 'Chase' and self.state != 'hit':
            if self.x < chr.x:
                self.dir = 'RIGHT'
                self.state = 'move'
                self.dx = 1.2
            else:
                self.dir = 'LEFT'
                self.state = 'move'
                self.dx = -1.2

        if isCollided:
            if x: self.x = x
            if y: self.y = y
            self.dx, self.dy = dx, dy
        
        if isLanding:
            if self.state == 'fall':
                self.state = 'idle'
            self.y = y
            self.dy = 0
            self.timer['fall'] = 0
        else:
            dy = 0
            ti = self.timer['fall']
            while ti > 0:
                ti -= 0.1
                dy -= 0.5
            self.state = 'fall'
            self.dx = 0
            self.dy = -2 + dy
            self.timer['fall'] += delta_time

        self.timer['order'] += delta_time
        self.x += self.dx
        self.y += self.dy

    def setOrder(self):
        if self.state == 'hit' or \
           self.state == 'fall' or \
           self.order != 'Chase':
            return

        chr = Ingame_state.chr

        # 내려찍기 패턴
        if get_time() - self.skillCoolTime.get('RapidFall') > 0:
            self.skillCoolTime['RapidFall'] = get_time()
            self.order = 'RapidFall'
            self.timer['fall'] = 1
            self.x, self.y = chr.x, chr.y + 250
            UI.addString([self.x, self.y], '피해보아라!!', (255, 100, 100), 2, 0.1, '24')
            return

        else:
            self.order = 'Chase'

    def updatePosWithOrder(self):
        self.attack_range = (0, 0, 0, 0)
        if self.order == 'RapidFall':
            self.attack_range = (self.x - 10, self.y + 75, self.x + 10, self.y - 40)

    def update(self, delta_time):
        self.updatePosBoss(delta_time)
        self.setOrder()
        self.updatePosWithOrder()
        self.updateHitbox()
        self.hitCheck()
        self.attackCheck()

    def drawEffect(self):
        for p in Projectile.Projectiles:
            p.draw()

        if self.order == 'RapidFall':
            frame = self.frame % 119
            eff = DataManager.load('../res/Effect/Fire/1_' + str(frame) + '.png')
            if self.dir == 'RIGHT':
                eff.draw(self.x - 5, self.y, 200, 200)
            else:
                eff.draw(self.x + 15, self.y, 200, 200)
