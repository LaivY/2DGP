import random
from pico2d import *

# 리소스 경로설정
MYDIR = '../rsrc/'

# 클래스
class BOY:
    def __init__(self):
        self.frame = random.randint(0, 8)
        self.x = random.randint(100, 800)
        self.y = random.randint(100, 800)
        self.image = load_image(MYDIR + 'run_animation.png')

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)
        self.frame = (self.frame + 1) % 8

def handle_events():
    global running
    evts = get_events()
    for e in evts:
        if e.type == SDL_QUIT:
            running = False
        elif (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            running = False

# 객체 생성 이전에 캔버스를 열어야함
open_canvas()

# 객체 생성
TEAM = [BOY() for i in range(11)]

# 그리기
running = True
while running:
    # 그리기
    clear_canvas()
    for c in TEAM:
        c.draw()
    update_canvas()

    # 이벤트처리
    get_events()
    handle_events()

    delay(0.01)

close_canvas()