from pico2d import *
from FRAMEWORK import Base, DataManager
from INGAME import Loading_state

MOUSE_POSITION = [0, 0]
MOUSE_ON_BUTTON = -1
FAST_SCROLL = False

def enter():
    global bgr, button, button_mouse_over, chr
    global mouseClick, mouseOver, bgm
    global scroll, star, timer1, timer2, frame

    bgr = DataManager.load('../res/UI/Main/BACKGROUND0.png'),\
          DataManager.load('../res/UI/Main/BACKGROUND1.png'),\
          DataManager.load('../res/UI/Main/BACKGROUND2.png')

    button = DataManager.load('../res/UI/Main/START_NORMAL.png'),\
             DataManager.load('../res/UI/Main/SHOW_RECORD_NORMAL.png'),\
             DataManager.load('../res/UI/Main/EXIT_NORMAL.png')

    button_mouse_over = DataManager.load('../res/UI/Main/START_MOUSE_OVER.png'),\
                        DataManager.load('../res/UI/Main/SHOW_RECORD_MOUSE_OVER.png'),\
                        DataManager.load('../res/UI/Main/EXIT_MOUSE_OVER.png')

    chr = DataManager.load('../res/Chr/chrSet.png')

    mouseClick = DataManager.load('../res/Sound/SOTE_SFX_UIClick_1_v2.wav')
    mouseOver  = DataManager.load('../res/Sound/SOTE_SFX_UIHover_v2.wav')
    bgm        = DataManager.load('../res/Sound/SOTE_Level1_Ambience_v6.mp3')
    bgm.repeat_play()

    scroll, star = -1200, False
    timer1, timer2, frame = 0, 0, 0

def exit():
    DataManager.unload('../res/UI/Main/BACKGROUND0.png')
    DataManager.unload('../res/UI/Main/BACKGROUND1.png')
    DataManager.unload('../res/UI/Main/BACKGROUND2.png')

    DataManager.unload('../res/UI/Main/START_NORMAL.png.png')
    DataManager.unload('../res/UI/Main/SHOW_RECORD_NORMAL.png')
    DataManager.unload('../res/UI/Main/EXIT_NORMAL.png')

    DataManager.unload('../res/UI/Main/START_MOUSE_OVER.png')
    DataManager.unload('../res/UI/Main/SHOW_RECORD_MOUSE_OVER.png')
    DataManager.unload('../res/UI/Main/EXIT_MOUSE_OVER.png.png')

    DataManager.unload('../res/Sound/SOTE_SFX_UIClick_1_v2.wav')
    DataManager.unload('../res/Sound/SOTE_SFX_UIHover_v2.wav')
    DataManager.unload('../res/Sound/SOTE_Level1_Ambience_v6.mp3')

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

    global MOUSE_ON_BUTTON
    x, y = MOUSE_POSITION

    # 모험시작 버튼
    if 279 <= x <= 520 and 256 <= y <= 304:
        button_mouse_over[0].draw(400, 280)
        if MOUSE_ON_BUTTON != 0:
            MOUSE_ON_BUTTON = 0
            mouseOver.play()
    else:
        button[0].draw(400, 280)

    # 도전기록 버튼
    if 279 <= x <= 520 and 185 <= y <= 234:
        button_mouse_over[1].draw(400, 210)
        if MOUSE_ON_BUTTON != 1:
            MOUSE_ON_BUTTON = 1
            mouseOver.play()
    else:
        button[1].draw(400, 210)

    # 게임종료 버튼
    if 279 <= x <= 520 and 115 <= y <= 164:
        button_mouse_over[2].draw(400, 140)
        if MOUSE_ON_BUTTON != 2:
            MOUSE_ON_BUTTON = 2
            mouseOver.play()
    else:
        button[2].draw(400, 140)

def eventHandler(e):
    global MOUSE_POSITION, MOUSE_ON_BUTTON, FAST_SCROLL
    if e.type == SDL_MOUSEMOTION:
        x, y = e.x, get_canvas_height() - e.y
        MOUSE_POSITION = [x, y]

        if not ((279 <= x <= 520 and 256 <= y <= 304) or
                (279 <= x <= 520 and 185 <= y <= 234) or
                (279 <= x <= 520 and 115 <= y <= 164)):
            MOUSE_ON_BUTTON = -1
    
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
                bgm.stop()
                mouseClick.play()
                Base.changeState(Loading_state)
            elif 366 <= e.y <= 366 + 49:
                mouseClick.play()
            elif 436 <= e.y <= 436 + 49:
                mouseClick.play()
                Base.running = False
