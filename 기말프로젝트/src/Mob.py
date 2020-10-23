import Ingame_state
from pico2d import *
from random import randint

# 슬라임 모션 딜레이
SLIME_MOTION_DELAY = {
    'attack': 15,
    'die': 30,
    'hit': 15,
    'idle': 15,
    'move': 20
}

# 슬라임 모션 프레임
SLIME_MOTION_FRAME = {
    'attack': 5,
    'die': 4,
    'hit': 4,
    'idle': 4,
    'move': 4
}

# 슬라임 모션별 히트박스
SLIME_MOTION_HITBOX = {
    'attack': (-14, 2, 14, -12),
    'die': (-16, 2, 16, -12),
    'hit': (-14, 2, 14, -12),
    'idle': (-16, 2, 16, -12),
    'move': (-14, 2, 14, -12)
}

# 모션별 딜레이
MOTION_DELAY = {
    '100': SLIME_MOTION_DELAY
}

# 모션별 프레임 수
MOTION_FRAME = {
    '100': SLIME_MOTION_FRAME
}

# 모션별 히트박스
MOTION_HITBOX = {
    '100': SLIME_MOTION_HITBOX
}

class Mob:
    # 슬라임 이미지 로드 (32x25)
    slime_image = None

    def __init__(self, mobId, xPos, yPos):
        ### 몬스터 시스템 관련 변수들 ###
        self.image = None                                                           # 이미지
        self.id = mobId                                                             # 몹 종류
        self.state = 'idle'                                                         # 상태
        self.order = 'patrol'                                                       # 명령
        self.order_timer = 0                                                        # 해당명령 수행시간
        self.frame, self.frame_timer = 0, 0                                         # 프레임, 프레임 타이머
        self.dir = 'LEFT'                                                           # 좌우
        self.x, self.y = xPos, yPos                                                 # 좌표
        self.dx, self.dy = 0, 0                                                     # 움직임속도
        self.hitBox = ()                                                            # 히트박스
        self.hitBy = ''                                                             # 어떤 공격에 맞았는지

        ### 몬스터 스탯 관련 변수들 ###
        self.maxHp, self.hp = 50, 50                            # 최대HP, 현재HP
        self.AD, self.DF, self.Speed, = 5, 0, 0                 # 공격력, 방어력, x축 추가 이동속도

    def load(self):
        # MobSet load
        if Mob.slime_image is None:
            Mob.slime_image = load_image('../res/Mob/100/sheet.png')
        if self.id == 100:
            self.image = Mob.slime_image

    def draw(self):
        draw_rectangle(self.hitBox[0], self.hitBox[1], self.hitBox[2], self.hitBox[3])
        if self.state == 'attack': ySheet = 4
        elif self.state == 'die' : ySheet = 3
        elif self.state == 'hit' : ySheet = 2
        elif self.state == 'idle': ySheet = 1
        elif self.state == 'move': ySheet = 0
        elif self.state == 'none': return
        if self.dir == 'LEFT':
            self.image.clip_draw(self.frame // MOTION_DELAY[str(self.id)][self.state] % MOTION_FRAME[str(self.id)][self.state] * 32, 25 * ySheet, 32, 25, self.x, self.y)
        else:
            self.image.clip_composite_draw(self.frame // MOTION_DELAY[str(self.id)][self.state] % MOTION_FRAME[str(self.id)][self.state] * 32, 25 * ySheet, 32, 25, 0, 'h', self.x, self.y, 32, 25)

    def update(self, delta_time):
        self.update_mob_hitbox()

        # 히트 체크
        hit = Ingame_state.mob_hit_check(self.hitBox)
        if hit[0] and self.hitBy != hit[1]:
            self.state = 'hit'
            self.hitBy = hit[1]
            self.hp -= hit[2]
            print(self.hp)
            if self.hp <= 0:
                self.state = 'die'
                self.order = 'none'
                self.dx = 0

        self.update_mob_order(delta_time)
        self.update_mob_state(delta_time)

    def update_mob_hitbox(self):
        if self.dir == 'LEFT':
            self.hitBox = (self.x + MOTION_HITBOX[str(self.id)][self.state][0], self.y + MOTION_HITBOX[str(self.id)][self.state][1],
                           self.x + MOTION_HITBOX[str(self.id)][self.state][2], self.y + MOTION_HITBOX[str(self.id)][self.state][3])
        else:
            self.hitBox = (self.x - MOTION_HITBOX[str(self.id)][self.state][0], self.y + MOTION_HITBOX[str(self.id)][self.state][1],
                           self.x - MOTION_HITBOX[str(self.id)][self.state][2], self.y + MOTION_HITBOX[str(self.id)][self.state][3])

    def update_mob_order(self, delta_time):
        # 순찰
        if self.order == 'patrol':
            # 만약 발견 범위 안에 있다면 approach 명령
            if (self.dir == 'LEFT' and self.x > Ingame_state.chr.x and self.x - Ingame_state.chr.x > 80 and abs(self.y - Ingame_state.chr.y) < 30) or \
               (self.dir == 'RIGHT' and self.x < Ingame_state.chr.x and Ingame_state.chr.x - self.x < 80 and abs(self.y - Ingame_state.chr.y) < 30):
                self.frame = 0
                self.order = 'approach'
                self.order_timer = 0

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
            if abs(Ingame_state.chr.x - self.x) > 50 and abs(Ingame_state.chr.y - self.y) > 80:
                self.frame = 0
                self.order = 'wait'
                self.order_timer = 0

            # 만약 공격할 수 있는 거리에 있다면 attack 명령
            elif abs(Ingame_state.chr.x - self.x) < 30 and abs(Ingame_state.chr.y - self.y) < 10:
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
            if self.order_timer > 1:
                self.order = 'approach'
                self.order_timer = 0

        # 대기
        if self.order == 'wait':
            self.dx = 0
            if self.order_timer > 0.5:
                self.order = 'patrol'
                self.order_timer = 0

        self.order_timer += delta_time

    def update_mob_state(self, delta_time):
        self.frame += 1
        if self.frame >= MOTION_FRAME[str(self.id)][self.state] * MOTION_DELAY[str(self.id)][self.state]:
            self.frame = 0
            if self.state == 'die':
                Ingame_state.mob.remove(self)
                return

        if self.state == 'die':
            return

        # Collide Check
        Collide_Result = Ingame_state.mob_collide_check(self.hitBox, self.dx, self.dy)
        if Collide_Result[0]:
            if Collide_Result[1] != 0: self.x = Collide_Result[1]
            if Collide_Result[2] != 0: self.y = Collide_Result[2]
            self.dx, self.dy = Collide_Result[3], Collide_Result[4]

        # Landing Check
        Landing_Result = Ingame_state.mob_landing_check(self.hitBox)
        if Landing_Result[0]:
            self.dy = 0
            self.y = Landing_Result[1]
        else:
            self.order = 'wait'
            self.dx = 0
            self.dy = -2

        self.x += self.dx
        self.y += self.dy