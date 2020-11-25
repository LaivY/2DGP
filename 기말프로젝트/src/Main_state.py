from pico2d import *
from FRAMEWORK import Base, Image
from INGAME import Loading_state

MOUSE_POSITION = [0, 0]
FAST_SCROLL = False

def enter():
    global bgr, button, button_mouse_over, scroll, chr, star, timer1, timer2, frame

    bgr = Image.load('../res/UI/Main/BACKGROUND0.png'),\
          Image.load('../res/UI/Main/BACKGROUND1.png'),\
          Image.load('../res/UI/Main/BACKGROUND2.png')

    button = Image.load('../res/UI/Main/START_NORMAL.png'),\
             Image.load('../res/UI/Main/SHOW_RECORD_NORMAL.png'),\
             Image.load('../res/UI/Main/EXIT_NORMAL.png')

    button_mouse_over = Image.load('../res/UI/Main/START_MOUSE_OVER.png'),\
                        Image.load('../res/UI/Main/SHOW_RECORD_MOUSE_OVER.png'),\
                        Image.load('../res/UI/Main/EXIT_MOUSE_OVER.png')

    chr = Image.load('../res/Chr/chrSet.png')
    scroll, star = -1200, False
    timer1, timer2, frame = 0, 0, 0

def exit():
    Image.unload('../res/UI/Main/BACKGROUND0.png')
    Image.unload('../res/UI/Main/BACKGROUND1.png')
    Image.unload('../res/UI/Main/BACKGROUND2.png')

    Image.unload('../res/UI/Main/START_NORMAL.png.png')
    Image.unload('../res/UI/Main/SHOW_RECORD_NORMAL.png')
    Image.unload('../res/UI/Main/EXIT_NORMAL.png')

    Image.unload('../res/UI/Main/START_MOUSE_OVER.png')
    Image.unload('../res/UI/Main/SHOW_RECORD_MOUSE_OVER.png')
    Image.unload('../res/UI/Main/EXIT_MOUSE_OVER.png.png')

def update():
    global scroll, star, timer1, timer2, frame

    if FAST_SCROLL:
        scroll -= 5
    else:
        scroll -= 0.5
    timer1 += Base.delta_time
    timer2 += Base.delta_time

    if scroll < -bgr[0].h:
        scroll = 0
    if timer1 > 1:
        timer1 = 0
        star = not star
    if timer2 > 0.2:
        timer2 = 0
        frame += 1

    frame = frame % 4

def draw():
    # 배경 수직스크롤
    global star
    if star: tbgr = bgr[1]
    else:    tbgr = bgr[0]
    tbgr.draw_to_origin(0, 0 + scroll)
    if abs(scroll - get_canvas_height()) > tbgr.h:
        tbgr.draw_to_origin(0, (scroll - get_canvas_height()) % get_canvas_height())

    # 캐릭터
    chr.clip_draw_to_origin(frame * 50, 37 * 3, 50, 32, 100, 80, 50, 37)

    # 배경
    bgr[2].draw(bgr[2].w / 2, bgr[2].h / 2)
    
    # 모험시작 버튼
    x, y = MOUSE_POSITION
    if 279 <= x <= 520 and 256 <= y <= 304:
        button_mouse_over[0].draw(400, 280)
    else:
        button[0].draw(400, 280)

    # 도전기록 버튼
    if 279 <= x <= 520 and 185 <= y <= 234:
        button_mouse_over[1].draw(400, 210)
    else:
        button[1].draw(400, 210)

    # 게임종료 버튼
    if 279 <= x <= 520 and 115 <= y <= 164:
        button_mouse_over[2].draw(400, 140)
    else:
        button[2].draw(400, 140)

def eventHandler(e):
    global MOUSE_POSITION, FAST_SCROLL
    if e.type == SDL_MOUSEMOTION:
        x, y = e.x, get_canvas_height() - e.y
        MOUSE_POSITION = [x, y]
    
    elif e.type == SDL_QUIT or (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
        Base.running = False

    elif (e.type, e.key) == (SDL_KEYDOWN, SDLK_SPACE):
        FAST_SCROLL = True

    elif (e.type, e.key) == (SDL_KEYUP, SDLK_SPACE):
        FAST_SCROLL = False

    elif (e.type, e.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
        # 241 x 49
        if 800 / 2 - 241 / 2 <= e.x <= 800 / 2 + 241 / 2:
            if 295 <= e.y <= 295 + 49:
                Base.changeState(Loading_state)
            elif 366 <= e.y <= 366 + 49:
                pass
            elif 436 <= e.y <= 436 + 49:
                Base.running = False
