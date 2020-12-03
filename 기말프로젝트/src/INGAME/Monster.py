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
        self.xSize, self.ySize, self.sxSize, self.sySize, self.maxHp, self.hp, self.ad, self.df, self.speed =\
            INFO['xSize'], INFO['ySize'], INFO['sxSize'], INFO['sySize'], INFO['hp'], INFO['hp'], INFO['ad'], INFO['df'], INFO['speed']

    def draw(self):
        if debug:
            draw_rectangle(self.hitBox[0], self.hitBox[1], self.hitBox[2], self.hitBox[3])
            draw_rectangle(self.attack_range[0], self.attack_range[1], self.attack_range[2], self.attack_range[3])
            UI.FONT['12'].draw(self.x, self.y + 32, self.order, (255, 255, 255))
            UI.FONT['12'].draw(self.x, self.y + 20, str(int(self.timer['order'])), (255, 255, 255))

        try:
            self.drawHpBar()
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
            if self.state == 'die': return False
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
            cLeft  = min(chr.hitBox[0], chr.hitBox[2])
            cRight = max(chr.hitBox[0], chr.hitBox[2])
            cTop   = max(chr.hitBox[1], chr.hitBox[3])
            cBot   = min(chr.hitBox[1], chr.hitBox[3])

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
        self.updateHitbox()
        self.updateOrder(delta_time)
        self.updatePos(delta_time)
        self.updateAttackRange()
        self.hitCheck()
        self.attackCheck()

class Boss(Monster):
    def __init__(self, mobId, xPos, yPos):
        super().__init__(mobId, xPos, yPos)
        self.order = 'Chase'
        self.timer['fall']  = 0
        self.timer['order'] = 0
        self.timer['skill'] = 0
        self.startTime = get_time()
        self.onlyOnce = {}

        self.skillCoolTime = {}
        self.skillCoolTime.update({
                                    'RapidFall' : 0,
                                    'WaveExplosion' : 0,
                                    'WaveExplosion2' : 0,
                                    'Thunder': 0,
                                    'Meteor': 0,
                                    'Fireball': 0,
                                    'Attack' : 0
                                   })
        self.skillCount = 0

    def changeOrder(self, order):
        self.frame = 0
        self.timer['order'] = 0
        self.timer['skill'] = 0
        self.skillCount = 0
        self.order = order

    def setOrder(self):
        if self.state == 'hit' or \
           self.state == 'fall' or \
           self.order != 'Chase':
            return

        chr = Ingame_state.chr

        # 보스방 입장 후 지난 시간
        time = get_time() - self.startTime

        # 랜덤으로 하나를 골라서 해당 패턴을 사용할 수 있는지 체크
        #pattern = randint(0, 5)
        pattern = 4

        # 내려찍기 패턴
        if pattern == 0:
            if get_time() - self.skillCoolTime.get('RapidFall') > 10:
                self.skillCoolTime['RapidFall'] = get_time()
                self.order = 'RapidFall'
                self.timer['fall'] = 0.5
                self.x, self.y = chr.x, chr.y + 250
                UI.addString([self.x, self.y], '도망칠 수 없다!!', (255, 100, 100), 2, 0.1, '24')
                return

        # 연쇄 폭발 패턴
        elif pattern == 1:
            if get_time() - self.skillCoolTime.get('WaveExplosion') > 15:
                self.skillCoolTime['WaveExplosion'] = get_time()
                self.order = 'WaveExplosion'
                UI.addString([self.x, self.y], '퍼져나가라!!', (255, 100, 100), 2, 0.1, '24')
                return

        # 연쇄 폭발 패턴2
        elif pattern == 2:
            if get_time() - self.skillCoolTime.get('WaveExplosion2') > 15:
                self.skillCoolTime['WaveExplosion2'] = get_time()
                self.order = 'WaveExplosion2'
                UI.addString([self.x, self.y], '돌아와라!!', (255, 100, 100), 2, 0.1, '24')
                return

        # 번개 패턴
        elif pattern == 3:
            if get_time() - self.skillCoolTime.get('Thunder') > 20:
                self.skillCoolTime['Thunder'] = get_time()
                self.order = 'Thunder'
                UI.addString([self.x, self.y], '내리쳐라!!', (255, 100, 100), 2, 0.1, '24')
                return

        # 메테오 패턴
        elif pattern == 4:
            if get_time() - self.skillCoolTime.get('Meteor') > 60:
                self.skillCoolTime['Meteor'] = get_time()
                self.order = 'Meteor'
                UI.addString([self.x, self.y], '모조리 쓸어버려주지!!', (255, 100, 100), 2, 0.1, '24')
                return
        
        # 파이어볼 패턴
        elif pattern == 5:
            if get_time() - self.skillCoolTime.get('Fireball') > 15:
                self.skillCoolTime['Fireball'] = get_time()
                self.order = 'Fireball'

                if self.x < chr.x:
                    self.dir = 'RIGHT'
                else:
                    self.dir = 'LEFT'
                UI.addString([self.x, self.y], '받아라!!', (255, 100, 100), 2, 0.1, '24')
                return

        self.order = 'Chase'

    def updatePosBoss(self, delta_time):
        chr = Ingame_state.chr

        # 필수
        self.frame += 1
        if self.frame >= self.MOTION_FRAME[self.state] * self.MOTION_DELAY[self.state]:
            self.frame = 0
            if self.state == 'hit' or 'attack' in self.state:
                self.frame = 0
                self.state = 'idle'
                self.order = 'Chase'

            elif self.state == 'die':
                self.frame = (self.MOTION_FRAME[self.state] - 1) * self.MOTION_DELAY[self.state]
                chr.onlyOnce.update( {'clear' : True} )

        # 충돌 계산
        isCollided, x, y, dx, dy = self.collideCheck()
        isLanding, y = self.landingCheck()

        ### 패턴 구현 부분 ###
        
        # 내려찍기
        if self.order == 'RapidFall':
            if isLanding:
                if self.dir == 'RIGHT':
                    Projectile.createProjectile('explosion', (self.x - 5, self.y), 3, 5, get_time())
                else:
                    Projectile.createProjectile('explosion', (self.x + 5, self.y), 3, 5, get_time())
                self.changeOrder('RapidFall_After')
                self.y, self.dy = y, 0
                return

        elif self.order == 'RapidFall_After':
            if self.state != 'hit':
                self.state = 'idle'
            if self.timer['order'] > 5:
                self.changeOrder('Chase')

        # 연쇄 폭발
        elif self.order == 'WaveExplosion':
            self.dx = 0
            self.state = 'idle'

            if self.timer['skill'] > 1:
                self.timer['skill'] = 0.9
                self.skillCount += 1
                Projectile.createProjectile('explosion', (self.x + self.skillCount * 50, self.y), 2, 3, get_time())
                Projectile.createProjectile('explosion', (self.x - self.skillCount * 50, self.y), 2, 3, get_time())

            if self.skillCount >= 20:
                self.changeOrder('WaveExplosion_After')

            self.timer['skill'] += delta_time

        elif self.order == 'WaveExplosion_After':
            if self.state != 'hit':
                self.state = 'idle'
            if self.timer['order'] > 5:
                self.changeOrder('Chase')

        # 연쇄 폭발2
        elif self.order == 'WaveExplosion2':
            self.dx = 0
            self.state = 'idle'

            if self.timer['skill'] > 0.1:
                self.timer['skill'] = 0
                self.skillCount += 1
                Projectile.createProjectile('explosion', (self.x + (20 - self.skillCount) * 50, self.y), 2, 3, get_time())
                Projectile.createProjectile('explosion', (self.x - (20 - self.skillCount) * 50, self.y), 2, 3, get_time())

            if self.skillCount >= 20:
                self.changeOrder('WaveExplosion2_After')

            self.timer['skill'] += delta_time

        elif self.order == 'WaveExplosion2_After':
            if self.state != 'hit':
                self.state = 'idle'
            if self.timer['order'] > 5:
                self.changeOrder('Chase')

        # 번개
        elif self.order == 'Thunder':
            self.dx = 0
            self.state = 'idle'

            if self.timer['skill'] > 1:
                self.timer['skill'] = 0.5
                self.skillCount += 1
                Projectile.createProjectile('thunder', (chr.x, self.y + 128), 2, 5, get_time())

            if self.skillCount >= 7:
                self.changeOrder('Thunder_After')

            self.timer['skill'] += delta_time

        elif self.order == 'Thunder_After':
            if self.state != 'hit':
                self.state = 'idle'
            if self.timer['order'] > 5:
                self.changeOrder('Chase')

        # 메테오
        elif self.order == 'Meteor':
            self.dx = 0
            self.state = 'attack2'
            if self.frame >= 7 * self.MOTION_DELAY[self.state]:
                self.frame = 7 * self.MOTION_DELAY[self.state]

            if self.timer['skill'] > 1:
                self.timer['skill'] = 0.9
                self.skillCount += 1

                meteorXPos = randint(0, 800)
                Projectile.createProjectile('meteor', (meteorXPos, 620), randint(150, 250) / 100, 5, get_time(), -5)

            if self.timer['order'] >= 10:
                self.changeOrder('Meteor_After')
                UI.addString([self.x, self.y], '아직도 살아있단 말이냐', (255, 255, 255), 3, 0.1)

            self.timer['skill'] += delta_time

        elif self.order == 'Meteor_After':
            if self.state != 'hit':
                self.state = 'idle'

            if self.timer['order'] > 10:
                self.changeOrder('Chase')

        # 파이어볼
        elif self.order == 'Fireball':
            self.dx = 0
            self.state = 'idle'

            if self.timer['skill'] > 1:
                self.timer['skill'] = 0.9
                self.skillCount += 1

                if self.x < chr.x:
                    Projectile.createProjectile('fireball', (self.x + 50, self.y), 5, 5, get_time(), 5)
                else:
                    Projectile.createProjectile('fireball', (self.x - 50, self.y), 5, 5, get_time(), -5)

            if self.skillCount >= 1:
                self.changeOrder('Fireball_After')

            self.timer['skill'] += delta_time

        elif self.order == 'Fireball_After':
            if self.state != 'hit':
                self.state = 'idle'

            if self.timer['order'] > 1:
                self.changeOrder('Chase')

        # 추적
        elif self.order == 'Chase' and self.state != 'hit':
            if abs(chr.x - self.x) < 100 and abs(chr.y - self.y) < 40 and \
                get_time() - self.skillCoolTime.get('Attack') > 5:
                self.skillCoolTime['Attack'] = get_time()
                self.changeOrder('Attack' + str(randint(1, 2)))
                self.dx = 0
                return

            if self.x < chr.x:
                self.dir = 'RIGHT'
                self.state = 'move'
                self.dx = 1.2
            else:
                self.dir = 'LEFT'
                self.state = 'move'
                self.dx = -1.2

        elif 'Attack' in self.order:
            self.state = self.order.lower()

        ### 패턴 구현 끝 ###

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

    def updateAttackRangeWithOrder(self):
        self.attack_range = (0, 0, 0, 0)
        if self.order == 'RapidFall':
            self.attack_range = (self.x - 10, self.y + 20, self.x + 10, self.y - 40)

        elif 'attack' in self.state:
            if self.MOTION_DELAY[self.state] * 4 <= self.frame <= self.MOTION_DELAY[self.state] * 5:
                if self.dir == 'RIGHT':
                    self.attack_range = (
                    self.x + self.MOTION_ATTACK_RANGE[self.state][0], self.y + self.MOTION_ATTACK_RANGE[self.state][1],
                    self.x + self.MOTION_ATTACK_RANGE[self.state][2], self.y + self.MOTION_ATTACK_RANGE[self.state][3])
                else:
                    self.attack_range = (
                    self.x - self.MOTION_ATTACK_RANGE[self.state][0], self.y + self.MOTION_ATTACK_RANGE[self.state][1],
                    self.x - self.MOTION_ATTACK_RANGE[self.state][2], self.y + self.MOTION_ATTACK_RANGE[self.state][3])

    def update(self, delta_time):
        self.updatePosBoss(delta_time)
        self.setOrder()
        self.updateAttackRangeWithOrder()
        self.updateHitbox()
        self.hitCheck()
        self.attackCheck()

        # if get_time() - self.startTime > 10 and \
        #     self.onlyOnce.get('10') != True:
        #     self.onlyOnce.update({'10' : True})
        #     print('10초 경과')

    def drawHpBar(self):
        image = DataManager.load('../res/UI/Ingame/CHR_HP_BAR.png')
        image.clip_draw_to_origin(0, 0, image.w, image.h, 10, 544, (self.hp / self.maxHp) * (get_canvas_width() - 20), image.h)