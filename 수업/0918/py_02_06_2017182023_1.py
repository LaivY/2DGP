from helper import *
from pico2d import *

# 리소스 경로설정
MYDIR = '../res/'

# 클래스
class BOY:
    def __init__(self):
        self.state = 'wait'         # 상태
        self.frame = 0              # 프레임
        self.speed = 1              # 속도
        self.targets = []           # 목적지
        self.x, self.y = 100, 100   # 위치
        self.image = load_image(MYDIR + 'run_animation.png')

    def draw(self):
        if(self.state == 'wait'):
            self.frame = 0
            self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)
        elif(self.state == 'move'):
            dx, dy = delta((self.x, self.y), (self.targets[0]), self.speed)
            (self.x, self.y), done = move_toward((self.x, self.y), (dx, dy), (self.targets[0]))
            self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)
            self.frame = (self.frame + 1) % 8

            # 도착하거나 연속적으로 목적지가 동일한 경우
            if done == True or (self.x, self.y) == self.targets[0]:
                del self.targets[0]
                self.state = 'wait'
                self.speed = 1

    def addTarget(self, x, y):
        self.targets.append((x, y))

    def update(self):
        if self.state == 'wait' and len(boy.targets) != 0:
            self.state = 'move'

def handle_events():
    global running, boy
    for e in get_events():
        # 종료
        if e.type == SDL_QUIT or (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            running = False
            return

        # 목적지 확인
        if (e.type, e.key) == (SDL_KEYDOWN, SDLK_l):
            print(boy.targets)

        # 목적지 추가
        if (e.type, e.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
            boy.addTarget(e.x, get_canvas_height() - e.y)

        # 속도 증가
        if boy.state == 'move' and (e.type, e.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
            boy.speed += 1

# 선언
open_canvas()
boy = BOY()
running = True

while running:
    clear_canvas()

    # 업데이트/그리기
    boy.update()
    boy.draw()
    update_canvas()

    # 이벤트처리
    handle_events()
    delay(0.01)

close_canvas()