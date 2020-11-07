import Ingame_state
import UI
from random import randint
from pico2d import *

debug = True

# 달리기 입력 무시
RUN_EXCEPTION = (
    'attack1', 'attack2', 'attack3',
    'air_attack1', 'air_attack2', 'hit'
)

# 점프 입력 무시
JUMP_EXCEPTION = (
    'attack1', 'attack2', 'attack3',
    'air_attack1', 'air_attack2', 'hit'
)

# 공격 입력 무시
ATTACK1_EXCEPTION = (
    'attack1', 'attack2', 'attack3',
    'air_attack1', 'air_attack2', 'hit'
)

class Character:
    # 50x37
    def __init__(self):
        ### 캐릭터 키보드 관련 변수들 ###
        self.image = None
        self.leftKeyDown = False
        self.rightKeyDown = False
        self.attackKeyDown = False

        ### 캐릭터 시스템 관련 변수들 ###
        self.frame, self.timer = 0, 0                                           # 프레임, 타이머
        self.state, self.subState = 'idle', 'jump'                              # 상태, 서브상태
        self.dir, self.x, self.y, self.dx, self. dy = 'RIGHT', 300, 400, 0, 0   # 좌우, 좌표와 움직임속도

        ### 캐릭터 피격, 공격 관련 변수들 ###
        self.hitBox = (0, 0, 0, 0)                                              # 히트박스
        self.attack_range = (0, 0, 0, 0)                                        # 공격범위
        self.invincible_time = 0                                                # 남은 무적 시간

        ### 캐릭터 스탯 관련 변수들 ###
        self.maxHp, self.localMaxHP, self.hp = 50, 50, 50                       # 원래 최대HP, 최종 최대HP, 현재HP
        self.ad, self.AS, self.df, self.speed, = 5, 0, 0, 0                     # 공격력, 공격속도, 방어력, x축 추가 이동속도
        self.relic = []                                                         # 유물

        ### 캐릭터 모션별 범위 변수들 :: JSON ###
        self.MOTION_DELAY = {}
        self.MOTION_DELAY_ORIGIN = {}
        self.MOTION_FRAME = {}
        self.MOTION_HITBOX = {}
        self.MOTION_ATTACK_RANGE = {}

    def load(self):
        self.image = load_image('../res/Chr/chrSet.png')
        self.loadMotionData()

    def draw(self):
        if debug:
            draw_rectangle(self.attack_range[0], self.attack_range[1], self.attack_range[2], self.attack_range[3])
            draw_rectangle(self.hitBox[0], self.hitBox[1], self.hitBox[2], self.hitBox[3])

        # 점프
        if self.subState == 'jump' or self.subState == 'jump2':
            if self.dir == 'RIGHT':
                self.image.clip_draw(self.frame // self.MOTION_DELAY['jump'] % 7 * 50, 37 * 13 - (self.frame // self.MOTION_DELAY['jump'] // 7 * 37), 50, 37, self.x, self.y)
            elif self.dir == 'LEFT':
                self.image.clip_composite_draw(self.frame // self.MOTION_DELAY['jump'] % 7 * 50, 37 * 13 - (self.frame // self.MOTION_DELAY['jump'] // 7 * 37), 50, 37,
                                               0, 'h', self.x, self.y, 50, 37)
        # 대기
        elif self.state == 'idle':
            if self.dir == 'RIGHT':
                self.image.clip_draw(self.frame // self.MOTION_DELAY[self.state] * 50, 555, 50, 37, self.x, self.y)
            elif self.dir == 'LEFT':
                self.image.clip_composite_draw(self.frame // self.MOTION_DELAY[self.state] * 50, 37 * 15, 50, 37,
                                               0, 'h', self.x, self.y, 50, 37)
        # 달리기
        elif self.state == 'run':
            if self.dir == 'RIGHT':
                self.image.clip_draw(self.frame // self.MOTION_DELAY[self.state] * 50 + 50, 37 * 14, 50, 37, self.x, self.y)
            elif self.dir == 'LEFT':
                self.image.clip_composite_draw(self.frame // self.MOTION_DELAY[self.state] * 50 + 50, 37 * 14, 50, 37,
                                               0, 'h', self.x, self.y, 50, 37)
        # 일반공격1
        elif self.state == 'attack1':
            if self.dir == 'RIGHT':
                self.image.clip_draw(self.frame // (self.MOTION_DELAY[self.state]) * 50, 37 * 9, 50, 37, self.x, self.y)
            elif self.dir == 'LEFT':
                self.image.clip_composite_draw(self.frame // (self.MOTION_DELAY[self.state]) * 50, 37 * 9, 50, 37,
                                               0, 'h', self.x, self.y, 50, 37)
        # 일반공격2
        elif self.state == 'attack2':
            if self.dir == 'RIGHT':
                if self.frame // self.MOTION_DELAY[self.state] < 4:
                    self.image.clip_draw(self.frame // self.MOTION_DELAY[self.state] * 50 + 50 * 3, 37 * 9, 50, 37, self.x, self.y)
                else:
                    self.image.clip_draw((self.frame // self.MOTION_DELAY[self.state] - 4) * 50, 37 * 8, 50, 37, self.x, self.y)
            elif self.dir == 'LEFT':
                if self.frame // self.MOTION_DELAY[self.state] < 4:
                    self.image.clip_composite_draw(self.frame // self.MOTION_DELAY[self.state] * 50 + 50 * 3, 37 * 9, 50, 37,
                                                   0, 'h', self.x, self.y, 50, 37)
                else:
                    self.image.clip_composite_draw((self.frame // self.MOTION_DELAY[self.state] - 4) * 50, 37 * 8, 50, 37,
                                                   0, 'h', self.x, self.y, 50, 37)
        # 일반공격3
        elif self.state == 'attack3':
            if self.dir == 'RIGHT':
                if self.frame // self.MOTION_DELAY[self.state] < 3:
                    self.image.clip_draw(self.frame // self.MOTION_DELAY[self.state] * 50 + 50 * 4, 37 * 8, 50, 37, self.x, self.y)
                else:
                    self.image.clip_draw((self.frame // self.MOTION_DELAY[self.state] - 3) * 50, 37 * 7, 50, 37, self.x, self.y)
            elif self.dir == 'LEFT':
                if self.frame // self.MOTION_DELAY[self.state] < 3:
                    self.image.clip_composite_draw(self.frame // self.MOTION_DELAY[self.state] * 50 + 50 * 4, 37 * 8, 50, 37,
                                                   0, 'h', self.x, self.y, 50, 37)
                else:
                    self.image.clip_composite_draw((self.frame // self.MOTION_DELAY[self.state] - 3) * 50, 37 * 7, 50, 37,
                                                   0, 'h', self.x, self.y, 50, 37)
        # 공중공격
        elif self.state == 'air_attack1':
            if self.dir == 'RIGHT':
                if self.frame // self.MOTION_DELAY[self.state] < 3:
                    self.image.clip_draw(self.frame // self.MOTION_DELAY[self.state] * 50 + 50 * 4, 37, 50, 37, self.x, self.y)
                else:
                    self.image.clip_draw((self.frame // self.MOTION_DELAY[self.state] - 3) * 50, 0, 50, 37, self.x, self.y)
            else:
                if self.frame // self.MOTION_DELAY[self.state] < 3:
                    self.image.clip_composite_draw(self.frame // self.MOTION_DELAY[self.state] * 50 + 50 * 4, 37, 50, 37, 0, 'h', self.x, self.y, 50, 37)
                else:
                    self.image.clip_composite_draw((self.frame // self.MOTION_DELAY[self.state] - 3) * 50, 0, 50, 37, 0, 'h', self.x, self.y, 50, 37)
        # 공중공격 마무리
        elif self.state == 'air_attack2':
            if self.dir == 'RIGHT':
                self.image.clip_draw(self.frame // self.MOTION_DELAY[self.state] * 50, 0, 50, 37, self.x, self.y)
            else:
                self.image.clip_composite_draw(self.frame // self.MOTION_DELAY[self.state] * 50, 0, 50, 37, 0, 'h', self.x, self.y, 50, 37)

        # 피격
        elif self.state == 'hit':
            if self.dir == 'RIGHT':
                self.image.clip_draw(self.frame // self.MOTION_DELAY[self.state] * 50 + 50 * 3, 37 * 7, 50, 37, self.x, self.y)
            else:
                self.image.clip_composite_draw(self.frame // self.MOTION_DELAY[self.state] * 50 + 50 * 3, 37 * 7, 50, 37, 0, 'h',
                                               self.x, self.y, 50, 37)

    def loadMotionData(self):
        with open('../res/Chr/info.json', 'r') as f:
            data = json.load(f)
        for i in data:
            if i['TYPE'] == 'MOTION_DELAY':
                self.MOTION_DELAY = dict(i)
                self.MOTION_DELAY_ORIGIN = dict(i)
            elif i['TYPE'] == 'MOTION_FRAME':
                self.MOTION_FRAME = dict(i)
            elif i['TYPE'] == 'MOTION_HITBOX':
                self.MOTION_HITBOX = dict(i)
            elif i['TYPE'] == 'MOTION_ATTACK_RANGE':
                self.MOTION_ATTACK_RANGE = dict(i)

    def eventHandler(self, e):
        # 죽은 상태일 경우 키입력 무시
        if self.hp <= 0:
            return

        # 점프
        if (e.key, e.type) == (SDLK_c, SDL_KEYDOWN) and self.state not in JUMP_EXCEPTION and self.subState == 'none':
            self.subState = 'jump'
            self.frame, self.timer = 0, 0
            self.y, self.dy = self.y + 10, 6

        # 더블점프
        elif (e.key, e.type) == (SDLK_c, SDL_KEYDOWN) and self.subState == 'jump':
            self.subState = 'jump2'
            self.frame, self.timer = 0, 0
            self.y, self.dy = self.y + 5, 5

        # 왼쪽 달리기
        elif (e.key, e.type) == (SDLK_LEFT, SDL_KEYDOWN):
            self.leftKeyDown = True
            if self.state not in RUN_EXCEPTION:
                self.dir = 'LEFT'
                self.state = 'run'
                self.dx = -2

        elif (e.key, e.type) == (SDLK_LEFT, SDL_KEYUP):
            self.leftKeyDown = False
            if self.state not in RUN_EXCEPTION:
                self.state = 'idle'
                self.dx = 0

        # 오른쪽 달리기
        elif (e.key, e.type) == (SDLK_RIGHT, SDL_KEYDOWN):
            self.rightKeyDown = True
            if self.state not in RUN_EXCEPTION:
                self.dir = 'RIGHT'
                self.state = 'run'
                self.dx = 2

        elif (e.key, e.type) == (SDLK_RIGHT, SDL_KEYUP):
            self.rightKeyDown = False
            if self.state not in RUN_EXCEPTION:
                self.state = 'idle'
                self.dx = 0

        # 상호작용
        elif (e.key, e.type) == (SDLK_z, SDL_KEYDOWN) and (self.state == 'idle'):
            interaction_result = Ingame_state.chr_interaction_check()
            if interaction_result != (-1, -1):
                self.interaction_handler(interaction_result)

        # 기본공격 1타
        elif ((e.key, e.type) == (SDLK_x, SDL_KEYDOWN) or self.attackKeyDown) and self.state not in ATTACK1_EXCEPTION and self.subState == 'none':
            self.state = 'attack1'
            self.frame, self.dx = 0, 0
            self.attackKeyDown = True

        # 기본공격 2타
        elif ((e.key, e.type) == (SDLK_x, SDL_KEYDOWN) or self.attackKeyDown) and self.state == 'attack1' and self.frame >= (self.MOTION_FRAME['attack1'] - 0.8) * self.MOTION_DELAY['attack1']:
            self.state = 'attack2'
            self.frame = 0

        # 기본공격 3타
        elif ((e.key, e.type) == (SDLK_x, SDL_KEYDOWN) or self.attackKeyDown) and self.state == 'attack2' and self.frame >= (self.MOTION_FRAME['attack2'] - 2) * self.MOTION_DELAY['attack2']:
            self.state = 'attack3'
            self.frame = 0

        # 공중공격 1타
        elif (e.key, e.type) == (SDLK_x, SDL_KEYDOWN) and (self.subState == 'jump' or self.subState == 'jump2'):
            self.state, self.subState = 'air_attack1', 'none'
            self.frame, self.dx, self.dy = 0, 0, -4
            self.attackKeyDown = True

        # 공격키업
        if (e.key, e.type) == (SDLK_x, SDL_KEYUP):
            self.attackKeyDown = False

    def interaction_handler(self, type):
        if type == (0, 1): # 유물 상자
            if len(self.relic) >= abs(100 - 105) + 1: return
            while True:
                temp = randint(100, 105)
                if temp not in self.relic:
                    self.relic.append(temp)
                    UI.addString([self.x, self.y], '유물을 획득했습니다!', (255, 255, 255), 1, 0.5)
                    break

        self.update_chr_stat()

    def update_chr_pos(self, delta_time):
        self.frame += 1

        # 대기
        if self.state == 'idle':
            if self.rightKeyDown:
                self.state = 'run'
                self.dir = 'RIGHT'
                if not Ingame_state.chr_collide_check()[0]:
                    self.dx = 2
            elif self.leftKeyDown:
                self.state = 'run'
                self.dir = 'LEFT'
                if not Ingame_state.chr_collide_check()[0]:
                    self.dx = -2
            else:
                if self.frame >= self.MOTION_FRAME['idle'] * self.MOTION_DELAY['idle']:
                    self.frame = 0

            # Fallen Check
            Landing_Result = Ingame_state.chr_landing_check()
            if not Landing_Result[0]:
                if self.subState != 'jump2':
                    self.subState = 'jump'

        # 달리기
        elif self.state == 'run' and self.subState == 'none':
            if self.frame >= self.MOTION_FRAME['run'] * self.MOTION_DELAY['run']:
                self.frame = 0

            # Fallen Check
            Landing_Result = Ingame_state.chr_landing_check()
            if not Landing_Result[0]:
                self.subState = 'jump'
                self.frame = 0

        # 공격
        elif self.state == 'attack1':
            if self.frame >= self.MOTION_FRAME['attack1'] * self.MOTION_DELAY['attack1']:
                self.frame = 0
                self.state = 'idle'
        elif self.state == 'attack2':
            if self.frame >= self.MOTION_FRAME['attack2'] * self.MOTION_DELAY['attack2']:
                self.frame = 0
                self.state = 'idle'
        elif self.state == 'attack3':
            if self.frame >= self.MOTION_FRAME['attack3'] * self.MOTION_DELAY['attack3']:
                self.frame = 0
                self.state = 'idle'

        # 공중공격
        elif self.state == 'air_attack1':
            self.dy -= 0.05

            # Frame Repeat
            if self.frame >= (self.MOTION_FRAME['air_attack1'] - 1) * self.MOTION_DELAY['air_attack1']:
                self.frame = self.MOTION_DELAY['air_attack1']

            # Landing Check
            Landing_Result = Ingame_state.chr_landing_check()
            if Landing_Result[0]:
                self.state = 'air_attack2'
                self.frame, self.dy = 0, 0
                self.y = Landing_Result[1]

        elif self.state == 'air_attack2':
            #self.frame += 1
            if self.frame >= self.MOTION_FRAME['air_attack2'] * self.MOTION_DELAY['air_attack2']:
                self.state = 'idle'
                self.frame = 0

        # 피격
        elif self.state == 'hit':
            if self.frame >= self.MOTION_FRAME['hit'] * self.MOTION_DELAY['hit']:
                self.state = 'idle'
                self.frame = 0
                self.dx = 0
                if self.hp <= 0:
                    self.state = 'die'

        # 사망
        elif self.state == 'die':
            if self.frame >= self.MOTION_FRAME['die'] * self.MOTION_DELAY['die']:
                self.frame = self.MOTION_FRAME['die'] * self.MOTION_DELAY['die']

        # 점프
        if self.subState == 'jump' or self.subState == 'jump2':
            # update Cycle
            self.timer += delta_time
            if self.timer > delta_time * 5:
                self.dy -= 2
                self.timer = 0

            # Frame Fix
            if self.frame > (self.MOTION_FRAME['jump'] - 1) * self.MOTION_DELAY['jump']:
                self.frame = (self.MOTION_FRAME['jump'] - 1) * self.MOTION_DELAY['jump']

            # Landing Check
            Landing_Result = Ingame_state.chr_landing_check()
            if Landing_Result[0]:
                self.state = 'idle'
                self.subState = 'none'
                self.frame = 0
                self.dy = 0
                self.y = Landing_Result[1]
            else:
                # keep going if now pressing button
                if self.leftKeyDown:
                    self.dx = -2
                elif self.rightKeyDown:
                    self.dx = 2

        # 무적시간 감소
        if self.invincible_time > 0:
            self.invincible_time -= delta_time
            if self.invincible_time < 0:
                self.invincible_time = 0

        # Collide Check
        Collide_Result = Ingame_state.chr_collide_check()
        if Collide_Result[0]:
            if Collide_Result[1] != 0: self.x = Collide_Result[1]
            if Collide_Result[2] != 0: self.y = Collide_Result[2]
            self.dx, self.dy = Collide_Result[3], Collide_Result[4]

        # Chr Pos Update
        self.x += self.dx * (1 + self.speed / 100)
        self.y += self.dy

    def update_chr_hitbox(self):
        if self.dir == 'RIGHT':
            if self.subState == 'jump' or self.subState == 'jump2':
                self.hitBox = (self.x - self.MOTION_HITBOX[self.subState][0], self.y + self.MOTION_HITBOX[self.subState][1],
                               self.x - self.MOTION_HITBOX[self.subState][2], self.y + self.MOTION_HITBOX[self.subState][3])
            else:
                self.hitBox = (self.x - self.MOTION_HITBOX[self.state][0], self.y + self.MOTION_HITBOX[self.state][1],
                               self.x - self.MOTION_HITBOX[self.state][2], self.y + self.MOTION_HITBOX[self.state][3])
        else:
            if self.subState == 'jump' or self.subState == 'jump2':
                self.hitBox = (self.x - self.MOTION_HITBOX[self.subState][0], self.y + self.MOTION_HITBOX[self.subState][1],
                               self.x - self.MOTION_HITBOX[self.subState][2], self.y + self.MOTION_HITBOX[self.subState][3])
            else:
                self.hitBox = (self.x + self.MOTION_HITBOX[self.state][0], self.y + self.MOTION_HITBOX[self.state][1],
                               self.x + self.MOTION_HITBOX[self.state][2], self.y + self.MOTION_HITBOX[self.state][3])

    def update_chr_stat(self):
        # 계산 전에 캐릭터 스탯 초기화
        self.maxHp, self.localMaxHP = 50, 50
        self.ad, self.AS, self.df, self.speed, = 5, 0, 0, 0

        # 유물로 인한 스탯 상승
        for relic in self.relic:
            if relic == 100:
                self.localMaxHP += 10
                self.hp += 10
            if relic == 101:
                self.ad += 1

        # 공격속도 적용
        self.MOTION_DELAY['attack1'] = int(self.MOTION_DELAY_ORIGIN['attack1'] * (100 - self.AS) / 100)
        self.MOTION_DELAY['attack2'] = int(self.MOTION_DELAY_ORIGIN['attack2'] * (100 - self.AS) / 100)
        self.MOTION_DELAY['attack3'] = int(self.MOTION_DELAY_ORIGIN['attack3'] * (100 - self.AS) / 100)
        self.MOTION_DELAY['air_attack2'] = int(self.MOTION_DELAY_ORIGIN['air_attack2'] * (100 - self.AS) / 100)

    def update_chr_attack_range(self):
        self.attack_range = (0, 0, 0, 0)

        if (self.state == 'attack1' and self.frame > self.MOTION_DELAY['attack1'] * 1.5) or \
           (self.state == 'attack2' and self.frame > self.MOTION_DELAY['attack2'] * 5) or \
           (self.state == 'attack3' and self.MOTION_DELAY['attack3'] * 2 < self.frame < self.MOTION_DELAY['attack3'] * 4) or \
           (self.state == 'air_attack1') or \
           (self.state == 'air_attack2') and self.frame < self.MOTION_DELAY['air_attack2'] * 3:
            if self.dir == 'RIGHT':
                self.attack_range = (self.x + self.MOTION_ATTACK_RANGE[self.state][0], self.y + self.MOTION_ATTACK_RANGE[self.state][1],
                                     self.x + self.MOTION_ATTACK_RANGE[self.state][2], self.y + self.MOTION_ATTACK_RANGE[self.state][3])
            else:
                self.attack_range = (self.x - self.MOTION_ATTACK_RANGE[self.state][0], self.y + self.MOTION_ATTACK_RANGE[self.state][1],
                                     self.x - self.MOTION_ATTACK_RANGE[self.state][2], self.y + self.MOTION_ATTACK_RANGE[self.state][3])

    def update(self, delta_time):
        # Pos update
        self.update_chr_pos(delta_time)

        # Hitbox update
        self.update_chr_hitbox()

        # Attack range update
        self.update_chr_attack_range()

        # Portal check
        Ingame_state.chr_portal_check()