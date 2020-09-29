import time
from pico2d import *
from Character import Character

# Resource Path
PATH = 'res/'
open_canvas()

def eventHandler():
    global running
    for e in get_events():
        # 종료
        if e.type == SDL_QUIT or (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            running = False
        # 캐릭터 이벤트처리
        c.eventHandler(e)

c = Character()
delta_time = 0
last_time = 0

running = True

while running:
    clear_canvas()

    # 반복할때 걸리는 시간
    now = time.time()
    delta_time = now - last_time
    last_time = now

    # 이벤트처리
    eventHandler()

    # 캐릭터
    c.update(delta_time)
    c.draw()

    update_canvas()
    delay(0.01)

close_canvas()