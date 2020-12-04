from pico2d import *
from FRAMEWORK import Base, DataManager
from INGAME import Ingame_state
import Loading_state
import UI

MOUSE_POSITION = [0, 0]
MOUSE_ON_BUTTON = -1
FAST_SCROLL = False
SHOW_TRAVEL_RECORD = False

def enter():
    global bgr, button, button_mouse_over, chr, dot
    global mouseClick, mouseOver, bgm
    global scroll, star, timer1, timer2, frame

    bgr = DataManager.load('res/UI/Main/BACKGROUND0.png'),\
          DataManager.load('res/UI/Main/BACKGROUND1.png'),\
          DataManager.load('res/UI/Main/BACKGROUND2.png')

    button = DataManager.load('res/UI/Main/START_NORMAL.png'),\
             DataManager.load('res/UI/Main/SHOW_RECORD_NORMAL.png'),\
             DataManager.load('res/UI/Main/EXIT_NORMAL.png')

    button_mouse_over = DataManager.load('res/UI/Main/START_MOUSE_OVER.png'),\
                        DataManager.load('res/UI/Main/SHOW_RECORD_MOUSE_OVER.png'),\
                        DataManager.load('res/UI/Main/EXIT_MOUSE_OVER.png')

    chr = DataManager.load('res/Chr/chrSet.png')

    dot = DataManager.load('res/UI/Main/DOT.png')

    mouseClick = DataManager.load('res/Sound/SOTE_SFX_UIClick_1_v2.wav')
    mouseOver  = DataManager.load('res/Sound/SOTE_SFX_UIHover_v2.wav')
    bgm        = DataManager.load('res/Sound/SOTE_Level1_Ambience_v6.mp3')
    bgm.repeat_play()

    scroll, star = -1200, False
    timer1, timer2, frame = 0, 0, 0

def exit():
    DataManager.unload('res/UI/Main/BACKGROUND0.png')
    DataManager.unload('res/UI/Main/BACKGROUND1.png')
    DataManager.unload('res/UI/Main/BACKGROUND2.png')

    DataManager.unload('res/UI/Main/START_NORMAL.png.png')
    DataManager.unload('res/UI/Main/SHOW_RECORD_NORMAL.png')
    DataManager.unload('res/UI/Main/EXIT_NORMAL.png')

    DataManager.unload('res/UI/Main/START_MOUSE_OVER.png')
    DataManager.unload('res/UI/Main/SHOW_RECORD_MOUSE_OVER.png')
    DataManager.unload('res/UI/Main/EXIT_MOUSE_OVER.png.png')

    DataManager.unload('res/Sound/SOTE_SFX_UIClick_1_v2.wav')
    DataManager.unload('res/Sound/SOTE_SFX_UIHover_v2.wav')
    DataManager.unload('res/Sound/SOTE_Level1_Ambience_v6.mp3')

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

    # 도전 기록
    if SHOW_TRAVEL_RECORD:
        showTravelRecord()

def eventHandler(e):
    global MOUSE_POSITION, MOUSE_ON_BUTTON, FAST_SCROLL, SHOW_TRAVEL_RECORD

    if not SHOW_TRAVEL_RECORD:
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

                # 게임시작
                if 295 <= e.y <= 295 + 49:
                    bgm.stop()
                    mouseClick.play()

                    try:
                        if Loading_state.LOADING_END:
                            Base.changeState(Ingame_state)
                        else:
                            Base.changeState(Loading_state)
                    except:
                        pass

                # 도전 기록
                elif 366 <= e.y <= 366 + 49:
                    mouseClick.play()
                    SHOW_TRAVEL_RECORD = True

                # 게임 종료
                elif 436 <= e.y <= 436 + 49:
                    mouseClick.play()
                    Base.running = False
    else:
        if e.type == SDL_QUIT:
            Base.running = False

        elif e.type == SDL_KEYDOWN:
            SHOW_TRAVEL_RECORD = False

def showTravelRecord():
    travelData = None
    try:
        with open('res/Chr/travel.json', 'r', encoding="utf-8") as f:
            travelData = json.load(f)
    except: pass

    # 뒷 배경
    dot.clip_draw_to_origin(0, 0, 1, 1, 0, 0, 800, 600)

    # 모험도전기록
    UI.FONT['24'].draw(340, 550, '모험도전기록', (255, 255, 255))
    UI.FONT['12'].draw(305, 533, '최근 8번의 모험 기록을 볼 수 있습니다.', (255, 255, 255))

    if travelData == None:
        UI.FONT['12'].draw(400, 300, '이전 기록이 없습니다.', (255, 255, 255))
    else:
        # 데이터가 있을 경우
        for i in range(len(travelData)):
            if i >= 8: return

            # 뒷 배경
            dot.clip_draw(0, 0, 1, 1, get_canvas_width() / 2, get_canvas_height() - 120 - 60 * i, 620, 50)

            # 패배/성공
            if travelData[-1 - i]['clear']:
                UI.FONT['24'].draw(100, get_canvas_height() - 120 - 60 * i, '성공', (100, 100, 255))
            else:
                UI.FONT['24'].draw(100, get_canvas_height() - 120 - 60 * i, '실패', (255, 100, 100))

            # 도전 시간
            UI.FONT['12'].draw(150, get_canvas_height() - 114 - 60 * i, travelData[-1 - i]['time'], (255, 255, 255))

            # 죽은 위치
            UI.FONT['12'].draw(150, get_canvas_height() - 126 - 60 * i, '마지막 위치 : ' + travelData[-1 - i]['pos'], (255, 255, 255))

            # 유물
            RelicImage = DataManager.load('res/Item/relic.png')
            for j in range(len(travelData[-1 - i]['relic'])):
                id = travelData[-1 - i]['relic'][j]['id']
                RelicImage.clip_draw(id % 100 * 128, (id // 100 - 1) * 128, 128, 128, 285 + 32 * j, get_canvas_height() - 120 - 60 * i, 64, 64)