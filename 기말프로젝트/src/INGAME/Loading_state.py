from pico2d import *
from FRAMEWORK import Base, Image
from INGAME import Relic, Ingame_state
import UI

FILES = [
    "../res/Chr/chrSet.png",
    "../res/Mob/100/sheet.png",
    "../res/Mob/101/sheet.png",
    "../res/Mob/102/sheet.png",
    "../res/Map/tileSet.png",
    "../res/Item/relic.png",
    "../res/UI/Ingame/ad.png",
    "../res/UI/Ingame/as.png",
    "../res/UI/Ingame/cri.png",
    "../res/UI/Ingame/df.png",
    "../res/UI/Ingame/CHR_HP_BAR.png",
    "../res/UI/Ingame/CHR_INFO_BASE.png"
]

JSON_FILES = [
    "../res/Chr/info.json",
    "../res/Item/relic_info.json",
    "../res/Mob/100/info.json",
    "../res/Mob/101/info.json",
    "../res/Mob/102/info.json",
]

def enter():
    global frame_interval, index, bgr, end
    UI.Font12 = load_font('../res/UI/모리스9.ttf', 12)
    UI.Font24 = load_font('../res/UI/모리스9.ttf', 24)
    bgr = load_image('../res/UI/Ingame/black.png')
    end = False

    frame_interval = Base.Frame_interval
    Base.Frame_interval = 0

    index = 0

def exit():
    global frame_interval, bgr
    del bgr
    Base.Frame_interval = frame_interval

def update():
    global index, display, end
    if index < len(FILES):
        display = 'Loading...' + str(int(index / (len(FILES) + len(JSON_FILES)) * 100)) + '%'
        Image.load(FILES[index])
        index += 1
    elif len(FILES) <= index < len(FILES) + len(JSON_FILES):
        display = 'Loading...' + str(int(index / (len(FILES) + len(JSON_FILES)) * 100)) + '%'
        loadJSONFile(index - len(FILES))
        index += 1
    else:
        end = True

def draw():
    global display
    bgr.clip_draw_to_origin(0, 0, get_canvas_width(), get_canvas_height(), 0, 0)

    if end:
        display = '로딩 완료!'
        display2 = '모험을 시작하려면 아무 키나 눌러주세요!'
        sx, sy = UI.get_text_extent(UI.Font12, display)
        _sx, _sy = UI.get_text_extent(UI.Font12, display2)
        UI.Font12.draw(400 - (sx / 5), 300 + (sy / 2) + 6, display, (255, 255, 255))
        UI.Font12.draw(400 - (_sx / 5), 300 + (_sy / 2) - 6, display2, (255, 255, 255))
    else:
        sx, sy = UI.get_text_extent(UI.Font12, display)
        UI.Font12.draw(400 - (sx / 2), 300 + (sy / 2), display, (255, 255, 255))

def eventHandler(e):
    if e.type == SDL_QUIT or (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
        Base.running = False

    if end and e.type == SDL_KEYDOWN:
        Base.Frame_interval = frame_interval
        Base.changeState(Ingame_state)
        return

def loadJSONFile(i):
    with open(JSON_FILES[i]) as f:
        data = json.load(f)

    if i == 0:
        chr = Ingame_state.chr
        for d in data:
            if d['TYPE'] == 'YSHEET':
                chr.MOTION_YSHEET = dict(d)
            elif d['TYPE'] == 'MOTION_DELAY':
                chr.MOTION_DELAY = dict(d)
                chr.MOTION_DELAY_ORIGIN = dict(d)
            elif d['TYPE'] == 'MOTION_FRAME':
                chr.MOTION_FRAME = dict(d)
            elif d['TYPE'] == 'MOTION_HITBOX':
                chr.MOTION_HITBOX = dict(d)
            elif d['TYPE'] == 'MOTION_ATTACK_RANGE':
                chr.MOTION_ATTACK_RANGE = dict(d)
    elif i == 1:
        for d in data:
            id = d['ID']
            Relic.RELIC_INFO[str(id)] = dict(d)
    else:
        MOTION_INFO   = {}
        MOTION_YSHEET = {}
        MOTION_DELAY  = {}
        MOTION_FRAME  = {}
        MOTION_HITBOX = {}
        MOTION_ATTACK_RANGE = {}

        for d in data:
            if d['TYPE'] == 'INFO':
                MOTION_INFO = dict(d)
                del MOTION_INFO['TYPE']

            elif d['TYPE'] == 'YSHEET':
               MOTION_YSHEET = dict(d)
               del MOTION_YSHEET['TYPE']

            elif d['TYPE'] == 'MOTION_DELAY':
                MOTION_DELAY = dict(d)
                del MOTION_DELAY['TYPE']

            elif d['TYPE'] == 'MOTION_FRAME':
                MOTION_FRAME = dict(d)
                del MOTION_FRAME['TYPE']

            elif d['TYPE'] == 'MOTION_HITBOX':
                MOTION_HITBOX = dict(d)
                del MOTION_HITBOX['TYPE']

            elif d['TYPE'] == 'MOTION_ATTACK_RANGE':
                MOTION_ATTACK_RANGE = dict(d)
                del MOTION_ATTACK_RANGE['TYPE']

        id = str(JSON_FILES[i]).split('/')[3]
        Ingame_state.Mob.MOB_MOTION_DATA[id] = {
            'INFO'        : MOTION_INFO,
            'YSHEET'      : MOTION_YSHEET,
            'DELAY'       : MOTION_DELAY,
            'FRAME'       : MOTION_FRAME,
            'HITBOX'      : MOTION_HITBOX,
            'ATTACK_RANGE': MOTION_ATTACK_RANGE,
        }
