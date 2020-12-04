from pico2d import *
from FRAMEWORK import Base, DataManager
from INGAME import Relic, Ingame_state
import Main_state
import UI

LOADING_END = False

FILES = [
    "res/Chr/chrSet.png",
    "res/Mob/100/sheet.png",
    "res/Mob/101/sheet.png",
    "res/Mob/102/sheet.png",
    "res/Mob/103/sheet.png",
    "res/Map/tileSet.png",
    "res/Item/relic.png",
    "res/UI/Ingame/ad.png",
    "res/UI/Ingame/as.png",
    "res/UI/Ingame/cri.png",
    "res/UI/Ingame/df.png",
    "res/UI/Ingame/CHR_HP_BAR.png",
    "res/UI/Ingame/CHR_INFO_BASE.png",
    "res/UI/Main/BACKGROUND0.png",
    "res/UI/Main/BACKGROUND1.png",
    "res/UI/Main/BACKGROUND2.png",
    "res/UI/Main/START_NORMAL.png",
    "res/UI/Main/SHOW_RECORD_NORMAL.png",
    "res/UI/Main/EXIT_NORMAL.png",
    "res/UI/Main/START_MOUSE_OVER.png",
    "res/UI/Main/SHOW_RECORD_MOUSE_OVER.png",
    "res/UI/Main/EXIT_MOUSE_OVER.png",
    "res/Sound/SOTE_SFX_UIClick_1_v2.wav",
    "res/Sound/SOTE_SFX_UIHover_v2.wav",
    "res/Sound/SOTE_Level1_Ambience_v6.mp3",
    "res/Sound/SOTE_SFX_DropRelic_Rocky.wav",
    "res/Sound/SOTE_SFX_FastAtk_v2.wav",
    "res/Sound/SOTE_SFX_HealShort_1_v2.wav",
    "res/Sound/STS_Level1_NewMix_v1.mp3",
    "res/Sound/STS_BossVictoryStinger_4_v3_MUSIC.wav",
    "res/Sound/STS_BossVictoryStinger_1_v3_SFX.wav"
]

# 불
for i in range(119 + 1):
    FILES.append('res/Effect/Fire/1_' + str(i) + '.png')

# 불꽃
for i in range(32 + 1):
    FILES.append('res/Effect/Frames/1_' + str(i) + '.png')

# 번개
for i in range(6 + 1):
    FILES.append('res/Effect/Thunder/' + str(i) + '.png')

# 파이어볼
for i in range(60 + 1):
    FILES.append('res/Effect/Fireball/1_' + str(i) + '.png')

JSON_FILES = [
    "res/Chr/info.json",
    "res/Item/relic_info.json",
    "res/Mob/100/info.json",
    "res/Mob/101/info.json",
    "res/Mob/102/info.json",
    "res/Mob/103/info.json",
]

def enter():
    global FPS, index, bgr
    UI.FONT['12'] = load_font('res/UI/모리스9.ttf', 12)
    UI.FONT['24'] = load_font('res/UI/모리스9.ttf', 24)
    bgr = load_image('res/UI/Ingame/black.png')

    FPS = Base.FPS
    Base.FPS = 0

    index = 0

def exit():
    global FPS, bgr
    del bgr
    Base.FPS = FPS

def update():
    global index, display, LOADING_END
    if index < len(FILES):
        display = 'Loading...' + str(int(index / (len(FILES) + len(JSON_FILES)) * 100)) + '%'
        DataManager.load(FILES[index])
        index += 1
    elif len(FILES) <= index < len(FILES) + len(JSON_FILES):
        display = 'Loading...' + str(int(index / (len(FILES) + len(JSON_FILES)) * 100)) + '%'
        loadJSONFile(index - len(FILES))
        index += 1
    else:
        LOADING_END = True

def draw():
    global display
    bgr.clip_draw_to_origin(0, 0, get_canvas_width(), get_canvas_height(), 0, 0)

    if LOADING_END:
        display = '로딩 완료!'
        display2 = '모험을 시작하려면 아무 키나 눌러주세요!'
        sx, sy = UI.get_text_extent(UI.FONT['12'], display)
        _sx, _sy = UI.get_text_extent(UI.FONT['12'], display2)
        UI.FONT['12'].draw(400 - (sx / 5), 300 + (sy / 2) + 6, display, (255, 255, 255))
        UI.FONT['12'].draw(400 - (_sx / 5), 300 + (_sy / 2) - 6, display2, (255, 255, 255))
    else:
        sx, sy = UI.get_text_extent(UI.FONT['12'], display)
        UI.FONT['12'].draw(400 - (sx / 2), 300 + (sy / 2), display, (255, 255, 255))

def eventHandler(e):
    if e.type == SDL_QUIT or (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
        Base.running = False

    if LOADING_END and e.type == SDL_KEYDOWN:
        Base.Frame_interval = FPS
        Base.changeState(Main_state)
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

        id = str(JSON_FILES[i]).split('/')[2]
        Ingame_state.Monster.MOB_MOTION_DATA[id] = {
            'INFO'        : MOTION_INFO,
            'YSHEET'      : MOTION_YSHEET,
            'DELAY'       : MOTION_DELAY,
            'FRAME'       : MOTION_FRAME,
            'HITBOX'      : MOTION_HITBOX,
            'ATTACK_RANGE': MOTION_ATTACK_RANGE,
        }
