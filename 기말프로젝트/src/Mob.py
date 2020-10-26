import Ingame_state
from pico2d import *
from random import randint

debug = True

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

SLIME_ATTACK_RANGE = {
    'attack': (0, 0, 30, -10)
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

# 모션별 공격범위
MOTION_HIT_RANGE = {
    '100': SLIME_ATTACK_RANGE
}

class Mob:
    # 슬라임 이미지 로드 (32x25)
    slime_image = None

    def __init__(self, mobId, xPos, yPos):
        ### 몬스터 이미지 관련 변수들 ###
        self.image = None                                                           # 이미지
        self.id = mobId                                                             # 몹 종류
        self.state = 'idle'                                                         # 상태
        self.order = 'patrol'                                                       # 명령
        self.order_timer = 0                                                        # 해당명령 수행시간
        self.frame, self.frame_timer = 0, 0                                         # 프레임, 프레임 타이머

        ### 몬스터 좌표 관련 변수들 ###
        self.dir = 'LEFT'                                                           # 좌우
        self.x, self.y = xPos, yPos                                                 # 좌표
        self.dx, self.dy = 0, 0                                                     # 움직임속도

        ### 몬스터 피격, 공격 관련 변수들 ###
        self.hitBy = ''                                                             # 어떤 공격에 맞았는지
        self.hitBox = (0, 0, 0, 0)                                                  # 히트박스
        self.attack_range = (0, 0, 0, 0)                                            # 공격범위

        ### 몬스터 스탯 관련 변수들 ###
        self.maxHp, self.hp = 50, 50                            # 최대HP, 현재HP
        self.AD, self.DF, self.Speed, = 1, 0, 0                 # 공격력, 방어력, x축 추가 이동속도

    def load(self):
        # MobSet load
        if Mob.slime_image is None:
            Mob.slime_image = load_image('../res/Mob/100/sheet.png')
        if self.id == 100:
            self.image = Mob.slime_image

    def draw(self):
        if debug:
            draw_rectangle(self.hitBox[0], self.hitBox[1], self.hitBox[2], self.hitBox[3])
            draw_rectangle(self.attack_range[0], self.attack_range[1], self.attack_range[2], self.attack_range[3])
        ySheet = -1
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

    def update_mob_hitbox(self):
        if self.dir == 'LEFT':
            self.hitBox = (self.x + MOTION_HITBOX[str(self.id)][self.state][0], self.y + MOTION_HITBOX[str(self.id)][self.state][1],
                           self.x + MOTION_HITBOX[str(self.id)][self.state][2], self.y + MOTION_HITBOX[str(self.id)][self.state][3])
        else:
            self.hitBox = (self.x - MOTION_HITBOX[str(self.id)][self.state][0], self.y + MOTION_HITBOX[str(self.id)][self.state][1],
                           self.x - MOTION_HITBOX[str(self.id)][self.state][2], self.y + MOTION_HITBOX[str(self.id)][self.state][3])

    def update_mob_hit_check(self):
        hit = Ingame_state.mob_hit_check(self.hitBox)
        if hit[0] and self.hitBy != hit[1] and self.state != 'die':
            self.state = 'hit'
            self.frame = 0
            self.dx = 0
            self.hitBy = hit[1]
            self.hp -= hit[2]
            if self.hp <= 0:
                self.state = 'die'
                self.order = 'none'
                self.frame = 0
            if debug:
                print('몬스터 HP : %d' % self.hp)

    def update_mob_order(self, delta_time):
        # 순찰
        if self.order == 'patrol':
            # 만약 발견 범위 안에 있다면 approach 명령
            if ((self.dir == 'LEFT' and 0 < self.x - Ingame_state.chr.x < 150 and abs(self.y - Ingame_state.chr.y) < 30) or
               (self.dir == 'RIGHT' and 0 < Ingame_state.chr.x - self.x < 150 and abs(self.y - Ingame_state.chr.y) < 30)) and self.state != 'attack':
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
            if abs(Ingame_state.chr.x - self.x) > 150 or abs(Ingame_state.chr.y - self.y) > 30:
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

        # 대기
        if self.order == 'wait':
            self.dx = 0
            if self.order_timer > 0.5:
                self.order = 'patrol'
                self.order_timer = 2

        self.order_timer += delta_time

    def update_mob_pos(self):
        self.frame += 1
        if self.frame >= MOTION_FRAME[str(self.id)][self.state] * (MOTION_DELAY[str(self.id)][self.state]):
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
        Collide_Result = Ingame_state.mob_collide_check(self.hitBox, self.dx, self.dy)
        if Collide_Result[0]:
            if Collide_Result[1] != 0: self.x = Collide_Result[1]
            if Collide_Result[2] != 0: self.y = Collide_Result[2]
            self.dx, self.dy = Collide_Result[3], Collide_Result[4]

        # Landing Check
        Landing_Result = Ingame_state.mob_landing_check(self.hitBox, self.x, self.dy)
        if Landing_Result[0]:
            self.y = Landing_Result[1]
            self.dy = 0
        else:
            self.state = 'idle'
            self.order = 'wait'
            self.dx = 0
            self.dy = -2

        self.x += self.dx
        self.y += self.dy

    def update_mob_attack_range(self):
        self.attack_range = (0, 0, 0, 0)
        if self.state == 'attack':
            if MOTION_DELAY[str(self.id)][self.state] * 2.3 < self.frame < MOTION_DELAY[str(self.id)][self.state] * 2.8:
                if self.dir == 'RIGHT':
                    self.attack_range = (self.x + MOTION_HIT_RANGE[str(self.id)][self.state][0], self.y + MOTION_HIT_RANGE[str(self.id)][self.state][1],
                                         self.x + MOTION_HIT_RANGE[str(self.id)][self.state][2], self.y + MOTION_HIT_RANGE[str(self.id)][self.state][3])
                else:
                    self.attack_range = (self.x - MOTION_HIT_RANGE[str(self.id)][self.state][0], self.y + MOTION_HIT_RANGE[str(self.id)][self.state][1],
                                         self.x - MOTION_HIT_RANGE[str(self.id)][self.state][2], self.y + MOTION_HIT_RANGE[str(self.id)][self.state][3])

    def update_mob_attack_chr_check(self):
        HIT = False
        if self.attack_range == (0, 0, 0, 0): return
        left = min(Ingame_state.chr.hitBox[0], Ingame_state.chr.hitBox[2])
        right = max(Ingame_state.chr.hitBox[0], Ingame_state.chr.hitBox[2])
        top = max(Ingame_state.chr.hitBox[1], Ingame_state.chr.hitBox[3])
        bot = min(Ingame_state.chr.hitBox[1], Ingame_state.chr.hitBox[3])

        if left < self.attack_range[0] < right and bot < self.attack_range[1] < top: HIT = True
        if left < self.attack_range[0] < right and bot < self.attack_range[3] < top: HIT = True
        if left < self.attack_range[2] < right and bot < self.attack_range[1] < top: HIT = True
        if left < self.attack_range[2] < right and bot < self.attack_range[3] < top: HIT = True

        if HIT and Ingame_state.chr.state != 'hit' and Ingame_state.chr.invincible_time == 0:
            if Ingame_state.chr.state == 'idle' or Ingame_state.chr.state == 'run':
                Ingame_state.chr.state = 'hit'
                Ingame_state.chr.frame = 0

                if self.x < Ingame_state.chr.x:
                    Ingame_state.chr.dx = 0.1
                    Ingame_state.chr.dir = 'LEFT'
                else:
                    Ingame_state.chr.dx = -0.1
                    Ingame_state.chr.dir = 'RIGHT'

            Ingame_state.chr.hp -= self.AD
            Ingame_state.chr.invincible_time = 1
            if debug:
                print('캐릭터 HP : %d' % Ingame_state.chr.hp)

    def update(self, delta_time):
        self.update_mob_order(delta_time)
        self.update_mob_pos()
        self.update_mob_hitbox()
        self.update_mob_hit_check()
        self.update_mob_attack_range()
        self.update_mob_attack_chr_check()