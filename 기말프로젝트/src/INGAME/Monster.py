from pico2d import *
from FRAMEWORK import Image
from INGAME import Ingame_state, Damage_Parser
from random import randint
import UI

debug = True

class Monster:
    # Loading_state에서 JSON파일을 읽어서 저장
    MOB_MOTION_DATA = {}

    def __init__(self, mobId, xPos, yPos):
        ### 몬스터 이미지 관련 변수들 ###
        self.image = None                                       # 이미지
        self.xSize, self.ySize = 0, 0                           # 화면 그려질 이미지의 크기
        self.sxSize, self.sySize = 0, 0                         # 이미지 파일 원본의 크기
        self.id = mobId                                         # 몹 종류
        self.state = 'idle'                                     # 상태
        self.order = 'patrol'                                   # 명령
        self.order_timer = 0                                    # 해당명령 수행시간
        self.frame, self.frame_timer = 0, 0                     # 프레임, 프레임 타이머

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
        self.image = Image.load('../res/Mob/' + str(self.id) + '/sheet.png')
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

        if self.state == 'none': return
        ySheet = self.MOTION_YSHEET[self.state]

        if self.dir == 'LEFT':
            self.image.clip_draw(self.frame // self.MOTION_DELAY[self.state] % self.MOTION_FRAME[self.state] * self.sxSize,
                                 self.sySize * ySheet, self.sxSize, self.sySize, self.x, self.y, self.xSize, self.ySize)
        else:
            self.image.clip_composite_draw(self.frame // self.MOTION_DELAY[self.state] % self.MOTION_FRAME[self.state] * self.sxSize,
                                           self.sySize * ySheet, self.sxSize, self.sySize, 0, 'h', self.x, self.y, self.xSize, self.ySize)

    def update_pos(self):
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
        Collide_Result = Ingame_state.mob_collide_check(self)
        if Collide_Result[0]:
            if Collide_Result[1] != 0: self.x = Collide_Result[1]
            if Collide_Result[2] != 0: self.y = Collide_Result[2]
            self.dx, self.dy = Collide_Result[3], Collide_Result[4]

        # Landing Check
        result = Ingame_state.mob_landing_check(self.hitBox, self.x, self.dy)
        if result[0]:
            if self.state == 'fall': self.state = 'idle'
            self.y = result[1] - self.MOTION_HITBOX[self.state][3]
            self.dy = 0
        else:
            if self.id == 200:
                self.state = 'fall'
            else:
                self.state = 'idle'
            self.order = 'wait'
            self.dx = 0
            self.dy = -2

        self.x += self.dx
        self.y += self.dy

    def update_hitbox(self):
        if self.dir == 'LEFT':
            self.hitBox = (self.x + self.MOTION_HITBOX[self.state][0], self.y + self.MOTION_HITBOX[self.state][1],
                           self.x + self.MOTION_HITBOX[self.state][2], self.y + self.MOTION_HITBOX[self.state][3])
        else:
            self.hitBox = (self.x - self.MOTION_HITBOX[self.state][0], self.y + self.MOTION_HITBOX[self.state][1],
                           self.x - self.MOTION_HITBOX[self.state][2], self.y + self.MOTION_HITBOX[self.state][3])

    def hitCheck(self):
        hit = Ingame_state.mob_hit_check(self.hitBox)
        if hit[0] and self.hitBy != hit[1] and self.state != 'die':
            Damage_Parser.chr_attack_mob(self, Ingame_state.chr, Ingame_state.chr.ad)

    def attackCheck(self):
        HIT = False
        if self.attack_range == (0, 0, 0, 0): return

        # 공격범위의 한 점이 캐릭터의 피격박스 안에 있는 경우
        left =  min(Ingame_state.chr.hitBox[0], Ingame_state.chr.hitBox[2])
        right = max(Ingame_state.chr.hitBox[0], Ingame_state.chr.hitBox[2])
        top =   max(Ingame_state.chr.hitBox[1], Ingame_state.chr.hitBox[3])
        bot =   min(Ingame_state.chr.hitBox[1], Ingame_state.chr.hitBox[3])
        if left < self.attack_range[0] < right and bot < self.attack_range[1] < top: HIT = True
        if left < self.attack_range[0] < right and bot < self.attack_range[3] < top: HIT = True
        if left < self.attack_range[2] < right and bot < self.attack_range[1] < top: HIT = True
        if left < self.attack_range[2] < right and bot < self.attack_range[3] < top: HIT = True

        # 캐릭터의 피격 박스의 한 점이 공격범위 안에 있는 경우
        _left = min(self.attack_range[0], self.attack_range[2])
        _right = max(self.attack_range[0], self.attack_range[2])
        _top = max(self.attack_range[1], self.attack_range[3])
        _bot = min(self.attack_range[1], self.attack_range[3])
        if _left < left < _right  and _bot < top < _top: HIT = True
        if _left < left < _right  and _bot < bot < _top: HIT = True
        if _left < right < _right and _bot < top < _top: HIT = True
        if _left < right < _right and _bot < bot < _top: HIT = True

        # 피격 박스와 공격 범위가 포개어져있는 경우
        if  _left < left < _right and \
            _left < right < _right and \
            (top > _top or bot < _bot):
            HIT = True

        if HIT and Ingame_state.chr.state != 'die' and Ingame_state.chr.invincible_time <= 0:
            Damage_Parser.mob_attack_chr(self, Ingame_state.chr)

class Mob(Monster):
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

    def update_order(self, delta_time):
        if self.state == 'hit': return

        # 순찰
        if self.order == 'patrol':
            # 만약 발견 범위 안에 있다면 approach 명령
            if self.canNoticeChr(Ingame_state.chr):
                self.frame = 0
                self.order = 'approach'
                self.order_timer = 0

            # 2초마다 순찰 방향 바꿈
            if self.order_timer > 2:
                self.order_timer = 0
            if self.order_timer == 0:
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
                self.order_timer = 0

            # 만약 공격할 수 있는 거리에 있다면 attack 명령
            elif self.canAttackChr(Ingame_state.chr):
                self.frame = 0
                self.order = 'attack'
                self.order_timer = 0

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
            if self.order_timer > 0.5:
                self.order = 'patrol'
                self.order_timer = 2

        self.order_timer += delta_time

    def update_attack_range(self):
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
        self.update_order(delta_time)
        self.update_pos()
        self.update_hitbox()
        self.update_attack_range()
        self.hitCheck()
        self.attackCheck()

class Boss(Monster):
    def __init__(self, mobId, xPos, yPos):
        super().__init__(mobId, xPos, yPos)

    def setOrder(self):
        if self.state == 'hit' or self.state == 'fall': return
        self.state = 'move'

        chr = Ingame_state.chr
        if self.x < chr.x:
            self.dir = 'RIGHT'
            self.dx = 1
        else:
            self.dir = 'LEFT'
            self.dx = -1

    def update(self, delta_time):
        self.setOrder()
        self.update_pos()
        self.update_hitbox()
        self.hitCheck()
