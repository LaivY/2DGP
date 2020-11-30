from pico2d import *
from FRAMEWORK import DataManager
from INGAME import Ingame_state, Relic
import UI
debug = False

# 달리기 입력 무시
RUN_EXCEPTION = (
    'attack1', 'attack2', 'attack3',
    'air_attack1', 'air_attack2', 'hit', 'slide'
)

# 점프 입력 무시
JUMP_EXCEPTION = (
    'attack1', 'attack2', 'attack3',
    'air_attack1', 'air_attack2', 'hit', 'slide'
)

# 공격 입력 무시
ATTACK1_EXCEPTION = (
    'attack1', 'attack2', 'attack3',
    'air_attack1', 'air_attack2', 'hit', 'slide'
)

# 슬라이딩 입력 무시
SLIDE_EXCEPTION = (
    'air_attack1', 'air_attack2', 'slide'
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
        self.state, self.subState = 'idle', 'none'                              # 상태, 서브상태
        self.dir, self.x, self.y, self.dx, self. dy = 'RIGHT', 100, 400, 0, 0   # 좌우, 좌표와 움직임속도
        self.relicGainPos = []                                                  # 유물 획득 위치 정보

        ### 캐릭터 피격, 공격 관련 변수들 ###
        self.hitBox = (0, 0, 0, 0)                                              # 히트박스
        self.attack_range = (0, 0, 0, 0)                                        # 공격범위
        self.invincible_time = 0                                                # 남은 무적 시간

        ### 캐릭터 스탯 관련 변수들 ###
        self.maxHP, self.hp = 50, 50                                            # 최대HP, 현재HP
        self.ad, self.AS, self.cri, self.df  = 5, 0, 5, 0                       # 공격력, 공격속도, 치명타, 방어력
        self.relic = []                                                         # 유물

        ### 캐릭터 모션별 범위 변수들 :: JSON ###
        self.MOTION_YSHEET = {}
        self.MOTION_DELAY = {}
        self.MOTION_DELAY_ORIGIN = {}
        self.MOTION_FRAME = {}
        self.MOTION_HITBOX = {}
        self.MOTION_ATTACK_RANGE = {}

    def load(self):
        self.image = DataManager.load("../res/Chr/chrSet.png")

    def draw(self):
        if 'jump' in self.subState:
            state = 'jump'
            ySheet = self.MOTION_YSHEET['jump']
        else:
            state = self.state
            ySheet = self.MOTION_YSHEET[self.state]

        if self.dir == 'RIGHT':
            self.image.clip_draw(self.frame // self.MOTION_DELAY[state] % self.MOTION_FRAME[state] * 50, ySheet * 37, 50, 37, self.x, self.y)
        elif self.dir == 'LEFT':
            self.image.clip_composite_draw(self.frame // self.MOTION_DELAY[state] % self.MOTION_FRAME[state] * 50, ySheet * 37, 50, 37, 0, 'h', self.x, self.y, 50, 37)

        if debug:
            draw_rectangle(self.attack_range[0], self.attack_range[1], self.attack_range[2], self.attack_range[3])
            draw_rectangle(self.hitBox[0], self.hitBox[1], self.hitBox[2], self.hitBox[3])

    def eventHandler(self, e):
        # 죽은 상태일 경우 키입력 무시
        if self.hp <= 0:
            return

        # 점프
        if (e.key, e.type) == (SDLK_c, SDL_KEYDOWN) and self.state not in JUMP_EXCEPTION and self.subState == 'none':
            self.state = 'idle'
            self.subState = 'jump'
            self.frame, self.timer = 0, 0
            self.y, self.dy = self.y + 10, 6
            self.dx = 0

        # 더블점프
        elif (e.key, e.type) == (SDLK_c, SDL_KEYDOWN) and self.subState == 'jump':
            self.subState = 'jump2'
            self.frame, self.timer = 0, 0
            self.y, self.dy = self.y + 5, 5

        # 삼단점프 :: 윙 부츠
        elif (e.key, e.type) == (SDLK_c, SDL_KEYDOWN) and self.subState == 'jump2':
            for r in self.relic:
                if r.id == 303:
                    self.subState = 'jump3'
                    self.frame, self.timer = 0, 0
                    self.y, self.dy = self.y + 5, 5
                    break

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

        # 슬라이딩
        elif (e.key, e.type) == (SDLK_SPACE, SDL_KEYDOWN) and self.state not in SLIDE_EXCEPTION and 'jump' not in self.subState:
            if self.leftKeyDown:
                self.state = 'slide'
                self.frame, self.timer = 0, 0
                self.dir = 'LEFT'
                self.dx = -5
            elif self.rightKeyDown:
                self.state = 'slide'
                self.frame, self.timer = 0, 0
                self.dir = 'RIGHT'
                self.dx = 5

        # 상호작용
        elif (e.key, e.type) == (SDLK_z, SDL_KEYDOWN) and (self.state == 'idle'):
            interaction_result = self.interactionCheck()
            if interaction_result != -1:
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
        elif (e.key, e.type) == (SDLK_x, SDL_KEYDOWN) and 'jump' in self.subState:
            self.state, self.subState = 'air_attack1', 'none'
            self.frame, self.dx, self.dy = 0, 0, -4
            self.attackKeyDown = True

        # 공격키업
        if (e.key, e.type) == (SDLK_x, SDL_KEYUP):
            self.attackKeyDown = False

    def interaction_handler(self, type):
        objType, pos = (type[0], type[1]), (type[2], type[3])

        # 유물 상자
        if objType == (0, 1):
            if (Ingame_state.map.id, *pos) in self.relicGainPos:
                UI.addString([self.x, self.y], '상자가 비어있습니다.', (255, 255, 255), 1, 0.1, 12)
            else:
                self.relicGainPos.append((Ingame_state.map.id, *pos))
                Relic.addRandomRelic()
                Relic.updateChrStat()

    def collideCheck(self):
        map = Ingame_state.map
        cLeft  = min(self.hitBox[0], self.hitBox[2])
        cRight = max(self.hitBox[0], self.hitBox[2])
        cTop   = max(self.hitBox[1], self.hitBox[3])
        cBot   = min(self.hitBox[1], self.hitBox[3])

        if self.subState == 'none':
            MOTION_HITBOX = self.MOTION_HITBOX[self.state]
        else:
            MOTION_HITBOX = self.MOTION_HITBOX[self.subState]
        cFront = abs(MOTION_HITBOX[0])
        cBack  = abs(MOTION_HITBOX[2])
        cUp    = abs(MOTION_HITBOX[1])
        cWidth = abs(MOTION_HITBOX[0]) + abs(MOTION_HITBOX[2])

        for tile in map.tileRect:
            RESULT = False, 0, 0, self.dx, self.dy
            tLeft, tTop, tRight, tBot = tile

            # 머리 충돌
            if (tLeft < cLeft < tRight or tLeft < cRight < tRight) and \
                tBot <= cTop + self.dy <= tTop != tBot:
                RESULT = True, RESULT[1], tBot - cUp, RESULT[3], 0

            # 좌측 충돌
            if (tBot < cTop < tTop or tBot < cBot < tTop) and \
                (cLeft + self.dx <= tRight <= cLeft or tLeft < cLeft + self.dx < tRight):
                RESULT = True, tRight + cBack, self.y, 0, RESULT[4]

            # 우측 충돌
            if (tBot < cTop < tTop or tBot < cBot < tTop) and \
                (cRight <= tLeft <= cRight + self.dx or tLeft < cRight + self.dx < tRight):
                RESULT = True, tLeft - cBack, self.y, 0, RESULT[4]

            # 맵 밖으로 못나가게
            if cLeft + self.dx < 0:
                RESULT = True, cBack, RESULT[2], 0, RESULT[4]
            elif cRight + self.dx > map.size[0]:
                RESULT = True, map.size[0] - cBack, RESULT[2], 0, RESULT[4]

            if RESULT[0]:
                return RESULT

        return False, None, None, None, None

    def landingCheck(self):
        map = Ingame_state.map
        cLeft  = min(self.hitBox[0], self.hitBox[2])
        cRight = max(self.hitBox[0], self.hitBox[2])
        cBot   = min(self.hitBox[1], self.hitBox[3])

        for tile in map.tileRect:
            tLeft, tTop, tRight, tBot = tile

            # 바닥 도착 조건
            # 1. 히트박스의 좌, 우 중에 하나라도 해당 지형의 폭 사이에 있어야한다.
            # 2. 히트박스의 하단 + dy <= 지형의 상단 <= 히트박스의 하단이여야한다.
            if (tLeft < cLeft < tRight or tLeft < cRight < tRight) and \
                cBot + self.dy <= tTop <= cBot:
                return True, tTop + abs(self.MOTION_HITBOX[self.state][3])
        return False, None

    def portalCheck(self):
        map = Ingame_state.map
        mob = Ingame_state.mob

        for portal in map.portalRect:
            isCrash = True
            if self.hitBox[2] < portal[0]: isCrash = False
            if self.hitBox[3] > portal[1]: isCrash = False
            if self.hitBox[0] > portal[2]: isCrash = False
            if self.hitBox[1] < portal[3]: isCrash = False
            if isCrash:
                id, x, y = portal[4], portal[5], portal[6]

                # 캐릭터가 도착맵에 있다면
                if map.id == id:
                    self.subState = 'jump2'
                    self.x, self.y = x, y
                    return

                # 맵 이동
                for r in self.relic:
                    # 조개화석
                    if r.id == 108:
                        r.stack = 1
                    # 수리검, 표창
                    elif r.id == 205 or r.id == 206:
                        r.stack = 0

                # 리스트 초기화
                mob.clear()
                map.tileRect.clear()
                map.portalRect.clear()

                # 맵 로드
                map.id = id
                map.load()

                # 캐릭터 세팅
                self.x, self.y, self.dx = x, y, 0
                return

    def interactionCheck(self):
        map = Ingame_state.map
        for obj in map.objectRect:
            if obj[0] <= self.x <= obj[2] and obj[3] <= self.y - 10 <= obj[1]:
                return obj[4], obj[5], (obj[0] + obj[2]) / 2, (obj[1] + obj[3]) / 2
        return -1

    def updatePos(self, delta_time):
        self.frame += 1

        # 대기
        if self.state == 'idle':
            if self.rightKeyDown:
                self.state = 'run'
                self.dir = 'RIGHT'
                self.dx = 2
            elif self.leftKeyDown:
                self.state = 'run'
                self.dir = 'LEFT'
                self.dx = -2

            # Fallen Check
            isLanding, _ = self.landingCheck()
            if not isLanding:
                if self.subState == 'none':
                    self.subState = 'jump'

        # 달리기
        elif self.state == 'run' and self.subState == 'none':
            if self.frame >= self.MOTION_FRAME['run'] * self.MOTION_DELAY['run']:
                self.frame = 0

            # Fallen Check
            isLanding, _ = self.landingCheck()
            if not isLanding:
                self.subState = 'jump'
                self.frame = 0

        # 공중공격
        elif self.state == 'air_attack1':
            self.dy -= 0.05

            # Frame Repeat
            if self.frame >= (self.MOTION_FRAME['air_attack1'] - 1) * self.MOTION_DELAY['air_attack1']:
                self.frame = 0

            # Landing Check
            isLanding, y = self.landingCheck()
            if isLanding:
                self.state = 'air_attack2'
                self.frame, self.dy = 0, 0
                self.y = y

        # 슬라이드
        elif self.state == 'slide':
            # update Cycle
            self.timer += delta_time
            if self.timer > delta_time * 6:
                if self.dir == 'LEFT' and self.dx < 0:
                    self.dx += 1
                elif self.dir == 'RIGHT' and self.dx > 0:
                    self.dx -= 1
                self.timer = 0
            if self.frame >= self.MOTION_FRAME[self.state] * self.MOTION_DELAY[self.state]:
                self.state = 'idle'
                self.frame, self.timer, self.dx = 0, 0, 0

            # Landing Check
            isLanding, _ = self.landingCheck()
            if not isLanding:
                self.state = 'idle'
                self.subState = 'jump'
                self.frame = 0
                self.dx = 0

        # 사망
        elif self.state == 'die':
            if self.frame >= self.MOTION_FRAME['die'] * self.MOTION_DELAY['die']:
                self.frame = (self.MOTION_FRAME['die'] - 1) * self.MOTION_DELAY['die']

        # 그 외
        else:
            if self.frame >= self.MOTION_FRAME[self.state] * self.MOTION_DELAY[self.state]:
                if self.state == 'hit': self.dx = 0
                self.state = 'idle'
                self.frame = 0

        # 점프
        if 'jump' in self.subState:
            # update Cycle
            self.timer += delta_time
            if self.timer > delta_time * 5:
                self.dy -= 2
                self.timer = 0

            # Frame Fix
            if self.frame > (self.MOTION_FRAME['jump'] - 1) * self.MOTION_DELAY['jump']:
                self.frame = (self.MOTION_FRAME['jump'] - 1) * self.MOTION_DELAY['jump']

            # Landing Check
            isLanding, y = self.landingCheck()
            if isLanding:
                self.state = 'idle'
                self.subState = 'none'
                self.frame = 0
                self.dy = 0
                self.y = y
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

        # 충돌 체크
        isCollided, x, y, dx, dy = self.collideCheck()
        if isCollided:
            if x: self.x = x
            if y: self.y = y
            self.dx, self.dy = dx, dy

        # Chr Pos Update
        self.x += self.dx
        self.y += self.dy

    def updateHitbox(self):
        if self.state == 'die': return
        if self.subState == 'none':
            MOTION_HITBOX = self.MOTION_HITBOX[self.state]
        else:
            MOTION_HITBOX = self.MOTION_HITBOX[self.subState]

        if self.dir == 'RIGHT':
            self.hitBox = (self.x - MOTION_HITBOX[0], self.y + MOTION_HITBOX[1],
                           self.x - MOTION_HITBOX[2], self.y + MOTION_HITBOX[3])
        else:
            self.hitBox = (self.x + MOTION_HITBOX[0], self.y + MOTION_HITBOX[1],
                           self.x + MOTION_HITBOX[2], self.y + MOTION_HITBOX[3])

    def updateAttackRange(self):
        self.attack_range = (0, 0, 0, 0)

        if (self.state == 'attack1' and self.MOTION_DELAY[self.state] * 2.5 < self.frame < self.MOTION_DELAY[self.state] * 3) or \
           (self.state == 'attack2' and self.MOTION_DELAY[self.state] * 3   < self.frame < self.MOTION_DELAY[self.state] * 4) or \
           (self.state == 'attack3' and self.MOTION_DELAY['attack3']  * 2    < self.frame < self.MOTION_DELAY['attack3'] * 4) or \
           (self.state == 'air_attack1') or \
           (self.state == 'air_attack2' and self.frame < self.MOTION_DELAY[self.state] * 2):
            if self.dir == 'RIGHT':
                self.attack_range = (self.x + self.MOTION_ATTACK_RANGE[self.state][0], self.y + self.MOTION_ATTACK_RANGE[self.state][1],
                                     self.x + self.MOTION_ATTACK_RANGE[self.state][2], self.y + self.MOTION_ATTACK_RANGE[self.state][3])
            else:
                self.attack_range = (self.x - self.MOTION_ATTACK_RANGE[self.state][0], self.y + self.MOTION_ATTACK_RANGE[self.state][1],
                                     self.x - self.MOTION_ATTACK_RANGE[self.state][2], self.y + self.MOTION_ATTACK_RANGE[self.state][3])

    def update(self, delta_time):
        # 위치 업데이트
        self.updatePos(delta_time)

        # 포탈 체크
        self.portalCheck()

        # 히트박스 업데이트
        self.updateHitbox()

        # 공격범위 업데이트
        self.updateAttackRange()
