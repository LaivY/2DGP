from pico2d import *
PATH = 'res/'

# 모션별 딜레이
MOTION_DELAY = {
    'idle': 15,
    'run': 10,
    'jump': 5,
    'attack1': 12,
    'attack2': 10,
    'attack3': 10
}

# 모션별 프레임 수
MOTION_FRAME = {
    'idle': 4,
    'run': 6,
    'jump': 10,
    'attack1': 3,
    'attack2': 8,
    'attack3': 6
}

class Character:
    # 50x37
    def __init__(self):
        # 디버그
        self.leftKeyDown = False
        self.rightKeyDown = False

        self.state = 'idle'             # 상태
        self.state2 = 'none'            # 2번째 상태
        self.frame = 0                  # 프레임
        self.frame2 = 0                 # 2번째 프레임
        self.timer = 0                  # 프레임 최신화 주기
        self.dir = 'RIGHT'              # 좌우
        self.x, self.y = 400, 100       # 좌표
        self.dx, self. dy = 0, 0        # 움직이는 속도
        self.image = load_image(PATH + 'adventurer-v1.5-Sheet.png')

    def draw(self):
        # 점프
        if self.state2 == 'jump' or self.state2 == 'jump2':
            if self.dir == 'RIGHT':
                self.image.clip_draw(self.frame2 // 5 % 7 * 50, 37 * 13 - (self.frame2 // 5 // 7 * 37), 50, 37, self.x, self.y)
            elif self.dir == 'LEFT':
                self.image.clip_composite_draw(self.frame2 // 5 % 7 * 50, 37 * 13 - (self.frame2 // 5 // 7 * 37), 50, 37, 0, 'h', self.x, self.y, 50, 37)
        # 대기
        elif self.state == 'idle':
            if self.dir == 'RIGHT':
                self.image.clip_draw(self.frame // MOTION_DELAY['idle'] * 50, 555, 50, 37, self.x, self.y)
            elif self.dir == 'LEFT':
                self.image.clip_composite_draw(self.frame // MOTION_DELAY['idle'] * 50, 37 * 15, 50, 37, 0, 'h', self.x, self.y, 50, 37)
        # 달리기
        elif self.state == 'run':
            if self.dir == 'RIGHT':
                self.image.clip_draw(self.frame // MOTION_DELAY['run'] * 50 + 50, 37 * 14, 50, 37, self.x, self.y)
            elif self.dir == 'LEFT':
                self.image.clip_composite_draw(self.frame // MOTION_DELAY['run'] * 50 + 50, 37 * 14, 50, 37, 0, 'h', self.x, self.y, 50, 37)
        # 일반공격1
        elif self.state == 'attack1':
            if self.dir == 'RIGHT':
                self.image.clip_draw(self.frame // MOTION_DELAY['attack1'] * 50, 37 * 9, 50, 37, self.x, self.y)
            elif self.dir == 'LEFT':
                self.image.clip_composite_draw(self.frame // MOTION_DELAY['attack1'] * 50, 37 * 9, 50, 37, 0, 'h', self.x, self.y, 50, 37)
        # 일반공격2
        elif self.state == 'attack2':
            if self.dir == 'RIGHT':
                if self.frame // MOTION_DELAY['attack2'] < 4:
                    self.image.clip_draw(self.frame // MOTION_DELAY['attack2'] * 50 + 50 * 3, 37 * 9, 50, 37, self.x, self.y)
                else:
                    self.image.clip_draw((self.frame // MOTION_DELAY['attack2'] - 4) * 50, 37 * 8, 50, 37, self.x, self.y)
            elif self.dir == 'LEFT':
                if self.frame // MOTION_DELAY['attack2'] < 4:
                    self.image.clip_composite_draw(self.frame // MOTION_DELAY['attack2'] * 50 + 50 * 3, 37 * 9, 50, 37, 0, 'h', self.x, self.y, 50, 37)
                else:
                    self.image.clip_composite_draw((self.frame // MOTION_DELAY['attack2'] - 4) * 50, 37 * 8, 50, 37, 0, 'h', self.x, self.y, 50, 37)
        # 일반공격3
        elif self.state == 'attack3':
            if self.dir == 'RIGHT':
                if self.frame // MOTION_DELAY['attack3'] < 3:
                    self.image.clip_draw(self.frame // MOTION_DELAY['attack3'] * 50 + 50 * 4, 37 * 8, 50, 37, self.x, self.y)
                else:
                    self.image.clip_draw((self.frame // MOTION_DELAY['attack3'] - 3) * 50, 37 * 7, 50, 37, self.x, self.y)
            elif self.dir == 'LEFT':
                if self.frame // MOTION_DELAY['attack3'] < 3:
                    self.image.clip_composite_draw(self.frame // MOTION_DELAY['attack3'] * 50 + 50 * 4, 37 * 8, 50, 37, 0, 'h', self.x, self.y, 50, 37)
                else:
                    self.image.clip_composite_draw((self.frame // MOTION_DELAY['attack3'] - 3) * 50, 37 * 7, 50, 37, 0, 'h', self.x, self.y, 50, 37)

    def update(self, delta_time):
        # 대기
        if self.state == 'idle':
            if self.rightKeyDown:
                self.dir = 'RIGHT'
                self.state = 'run'
                self.dx = 2
            elif self.leftKeyDown:
                self.dir = 'LEFT'
                self.state = 'run'
                self.dx = -2
            else:
                self.frame += 1
                if self.frame >= MOTION_FRAME['idle'] * MOTION_DELAY['idle']:
                    self.frame = 0

        # 달리기
        elif self.state == 'run':
            self.frame += 1
            if self.frame >= MOTION_FRAME['run'] * MOTION_DELAY['run']:
                self.frame = 0

        # 점프
        if self.state2 == 'jump' or self.state2 == 'jump2':
            self.frame2 += 1

            # update Cycle
            self.timer += delta_time
            if self.timer > 0.08:
                self.dy -= 2
                self.timer = 0

            # Frame Fix
            if self.frame2 > (MOTION_FRAME['jump'] - 1) * MOTION_DELAY['jump']:
                self.frame2 = (MOTION_FRAME['jump'] - 1) * MOTION_DELAY['jump']

            # Landing Check
            if self.y + self.dy < 100:
                self.state2 = 'none'
                self.frame2 = 0
                self.dy = 0
                self.y = 100

        # 공격
        if self.state == 'attack1':
            self.frame += 1
            if self.frame >= MOTION_FRAME['attack1'] * MOTION_DELAY['attack1']:
                self.frame = 0
                self.state = 'idle'
        elif self.state == 'attack2':
            self.frame += 1
            if self.frame >= MOTION_FRAME['attack2'] * MOTION_DELAY['attack2']:
                self.frame = 0
                self.state = 'idle'
        elif self.state == 'attack3':
            self.frame += 1
            if self.frame >= MOTION_FRAME['attack3'] * MOTION_DELAY['attack3']:
                self.frame = 0
                self.state = 'idle'

        # Chr Pos Update
        self.x += self.dx
        self.y += self.dy

    def eventHandler(self, e):
        # 왼쪽 달리기
        if (e.key, e.type) == (SDLK_LEFT, SDL_KEYDOWN):
            self.leftKeyDown = True
            if self.state != 'attack1':
                self.dir = 'LEFT'
                self.state = 'run'
                self.dx = -2
        elif (e.key, e.type) == (SDLK_LEFT, SDL_KEYUP):
            self.leftKeyDown = False
            self.state = 'idle'
            self.dx = 0

        # 오른쪽 달리기
        if (e.key, e.type) == (SDLK_RIGHT, SDL_KEYDOWN):
            self.rightKeyDown = True
            if self.state != 'attack1':
                self.dir = 'RIGHT'
                self.state = 'run'
                self.dx = 2
        elif (e.key, e.type) == (SDLK_RIGHT, SDL_KEYUP):
            self.rightKeyDown = False
            self.state = 'idle'
            self.dx = 0

        # 점프
        if (e.key, e.type) == (SDLK_c, SDL_KEYDOWN) and self.state2 != 'jump' and self.state2 != 'jump2':
            self.state2 = 'jump'
            self.frame2 = 0
            self.timer = 0
            self.y += 10
            self.dy = 6

        # 더블점프
        elif (e.key, e.type) == (SDLK_c, SDL_KEYDOWN) and self.state2 == 'jump':
            self.state2 = 'jump2'
            self.frame2 = 0
            self.timer = 0
            self.y += 5
            self.dy = 5

        # 기본공격 1타
        if (e.key, e.type) == (SDLK_x, SDL_KEYDOWN) and self.state != 'attack1' and self.state != 'attack2' and self.state != 'attack3' \
                                                    and self.state2 != 'jump' and self.state2 != 'jump2':
            self.state = 'attack1'
            self.frame = 0
            self.timer = 0
            self.dx = 0

        # 기본공격 2타
        elif (e.key, e.type) == (SDLK_x, SDL_KEYDOWN) and self.state == 'attack1' and self.frame >= (MOTION_FRAME['attack1'] - 2) * MOTION_DELAY['attack1']:
            self.state = 'attack2'
            self.frame = 0
            self.timer = 0
            self.dx = 0

        # 기본공격 3타
        elif (e.key, e.type) == (SDLK_x, SDL_KEYDOWN) and self.state == 'attack2' and self.frame >= (MOTION_FRAME['attack2'] - 2) * MOTION_DELAY['attack2']:
            self.state = 'attack3'
            self.frame = 0
            self.timer = 0
            self.dx = 0
