from pico2d import *
PATH = 'res/'

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
        if self.state2 is 'none':
            if self.state is 'idle':
                if self.dir is 'RIGHT':
                    self.image.clip_draw(self.frame // 15 * 50, 555, 50, 37, self.x, self.y)
                elif self.dir is 'LEFT':
                    self.image.clip_composite_draw(self.frame // 15 * 50, 37 * 15, 50, 37, 0, 'h', self.x, self.y, 50, 37)
            elif self.state is 'run':
                if self.dir is 'RIGHT':
                    self.image.clip_draw(self.frame // 10 * 50 + 50, 37 * 14, 50, 37, self.x, self.y)
                elif self.dir is 'LEFT':
                    self.image.clip_composite_draw(self.frame // 10 * 50 + 50, 37 * 14, 50, 37, 0, 'h', self.x, self.y, 50, 37)
            elif self.state is 'attack1':
                if self.dir is 'RIGHT':
                    self.image.clip_draw(self.frame // 20 * 50, 37 * 9, 50, 37, self.x, self.y)
                elif self.dir == 'LEFT':
                    self.image.clip_composite_draw(self.frame // 20 * 50, 37 * 9, 50, 37, 0, 'h', self.x, self.y, 50, 37)
            elif self.state is 'attack2':
                if self.dir is 'RIGHT':
                    if self.frame // 15 < 4:
                        self.image.clip_draw(self.frame // 15 * 50 + 50 * 3, 37 * 9, 50, 37, self.x, self.y)
                    else:
                        self.image.clip_draw((self.frame // 15 - 4) * 50, 37 * 8, 50, 37, self.x, self.y)

        else:
            if self.state2 is 'jump':
                if self.dir is 'RIGHT':
                    self.image.clip_draw(self.frame2 // 5 % 7 * 50, 37 * 13 - (self.frame2 // 5 // 7 * 37), 50, 37, self.x, self.y)
                elif self.dir is 'LEFT':
                    self.image.clip_composite_draw(self.frame2 // 5 % 7 * 50, 37 * 13 - (self.frame2 // 5 // 7 * 37), 50, 37, 0, 'h', self.x, self.y, 50, 37)
            elif self.state2 is 'jump2':
                if self.dir is 'RIGHT':
                    self.image.clip_draw(self.frame2 // 5 % 7 * 50, 37 * 13 - (self.frame2 // 5 // 7 * 37), 50, 37, self.x, self.y)
                elif self.dir is 'LEFT':
                    self.image.clip_composite_draw(self.frame2 // 5 % 7 * 50, 37 * 13 - (self.frame2 // 5 // 7 * 37), 50, 37, 0, 'h', self.x, self.y, 50, 37)

    def update(self, delta_time):
        # 대기
        if self.state is 'idle':
            if self.rightKeyDown is True:
                self.dir = 'RIGHT'
                self.state = 'run'
                self.dx = 2
            elif self.leftKeyDown is True:
                self.dir = 'LEFT'
                self.state = 'run'
                self.dx = -2
            else:
                self.frame += 1
                if self.frame >= 4 * 15:
                    self.frame = 0

        # 달리기
        elif self.state is 'run':
            self.frame += 1
            if self.frame >= 6 * 10:
                self.frame = 0

        # 점프
        if self.state2 is 'jump' or 'jump2':
            self.frame2 += 1

            # update Cycle
            self.timer += delta_time
            if self.timer > 0.08:
                self.dy -= 2
                self.timer = 0

            # Frame Fix
            if self.frame2 > 9 * 5:
                self.frame2 = 9 * 5

            # Landing Check
            if self.y + self.dy < 100:
                self.state2 = 'none'
                self.frame2 = 0
                self.dy = 0
                self.y = 100

        # 공격
        if self.state is 'attack1':
            self.frame += 1
            if self.frame >= 3 * 20:
                self.frame = 0
                self.state = 'idle'
        elif self.state is 'attack2':
            self.frame += 1
            if self.frame >= 8 * 15:
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
        if (e.key, e.type) == (SDLK_x, SDL_KEYDOWN) and self.state != 'attack1' and self.state2 != 'jump' and self.state2 != 'jump2':
            self.state = 'attack1'
            self.frame = 0
            self.timer = 0
            self.dx = 0

        # 기본공격 2타
        elif (e.key, e.type) == (SDLK_x, SDL_KEYDOWN) and self.state == 'attack1' and 25 <= self.frame:
            self.state = 'attack2'
            self.frame = 0
            self.timer = 0
            self.dx = 0