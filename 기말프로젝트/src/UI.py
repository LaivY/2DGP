from pico2d import *
from FRAMEWORK import Base, DataManager
from INGAME import Ingame_state

CHR_INFO_IMAGE = {}
MOUSE_POSITION = [0, 0]
STRING_DATA_TO_PRINT = []
FONT = {}

def load():
    global relic_image
    relic_image = DataManager.load('../res/Item/relic.png')
    CHR_INFO_IMAGE['base'] = DataManager.load('../res/UI/Ingame/CHR_INFO_BASE.png')
    CHR_INFO_IMAGE['hpbar'] = DataManager.load('../res/UI/Ingame/CHR_HP_BAR.png')
    CHR_INFO_IMAGE['ad'] = DataManager.load('../res/UI/Ingame/ad.png')
    CHR_INFO_IMAGE['as'] = DataManager.load('../res/UI/Ingame/as.png')
    CHR_INFO_IMAGE['cri'] = DataManager.load('../res/UI/Ingame/cri.png')
    CHR_INFO_IMAGE['df'] = DataManager.load('../res/UI/Ingame/df.png')

def draw():
    drawRelic()
    drawRelicDesc()
    drawChrInfo()
    drawChrInfoDesc()
    printStringData()

def drawRelic():
    chr = Ingame_state.chr
    for i in range(len(chr.relic)):
        relic_image.clip_draw(chr.relic[i].id % 100 * 128, (chr.relic[i].id // 100 - 1) * 128, 128, 128, 20 + 32 * i, 580, 64, 64)
        if chr.relic[i].condition != -1:
            if chr.relic[i].isActive:
                rgb = (50, 255, 50)
            else:
                rgb = (255, 255, 255)
            FONT['12'].draw(26 + 32 * i, 580 - 8, str(chr.relic[i].stack), rgb)

def drawRelicDesc():
    r = Ingame_state.chr.relic
    for i in range(len(r)):
        if 20 + 32 * i - 16 < MOUSE_POSITION[0] < 20 + 32 * i + 16 and \
           580 - 16 < MOUSE_POSITION[1] < 580 + 16:
            FONT['12'].draw(6 + 32 * i, 556, str(r[i].name), (255, 255, 255))
            FONT['12'].draw(6 + 32 * i, 544, str(r[i].desc), (255, 255, 255))
            FONT['12'].draw(6 + 32 * i, 532, str(r[i].flavorText), (150, 150, 150))

def drawChrInfo():
    chr = Ingame_state.chr

    # 체력바
    CHR_INFO_IMAGE['hpbar'].clip_draw_to_origin(0, 0, 154, 12, 12, 37, chr.hp / chr.maxHP * 154, 12)

    # 베이스
    CHR_INFO_IMAGE['base'].draw_to_origin(10, 10, 158, 41)

    # 체력
    FONT['12'].draw(72, 42, str(chr.hp) + ' / ' + str(chr.maxHP), (255, 255, 255))

    # 공격력
    CHR_INFO_IMAGE['ad'].draw(27, 24)
    FONT['12'].draw(38, 23, str(chr.ad), (255, 255, 255))

    # 공격속도
    CHR_INFO_IMAGE['as'].draw(65, 24)
    FONT['12'].draw(76, 23, str(chr.AS), (255, 255, 255))

    # 치명타
    CHR_INFO_IMAGE['cri'].draw(103, 24)
    FONT['12'].draw(114, 23, str(chr.cri), (255, 255, 255))

    # 방어력
    CHR_INFO_IMAGE['df'].draw(141, 24)
    FONT['12'].draw(152, 23, str(chr.df), (255, 255, 255))

def drawChrInfoDesc():
    chr = Ingame_state.chr
    infoX, infoY = 173, 42
    if 12 <= MOUSE_POSITION[0] <= 12 + 154 and 37 <= MOUSE_POSITION[1] <= 37 + 12:
        FONT['12'].draw(infoX, infoY, str('체력'), (244, 41, 65))
        FONT['12'].draw(infoX, infoY - 12, str('0이 되면 캐릭터가 사망합니다.'), (255, 255, 255))
        FONT['12'].draw(infoX, infoY - 24, '[기본 50 + 추가 ' + str(chr.maxHP - 50) + ']', (255, 255, 255))
    elif 25 - 8 <= MOUSE_POSITION[0] <= 25 + 8 and 24 - 8 <= MOUSE_POSITION[1] <= 24 + 8:
        FONT['12'].draw(infoX, infoY, '공격력', (246, 70, 91))
        FONT['12'].draw(infoX, infoY - 12, '공격으로 ' + str(chr.ad) + ' 만큼의 피해를 줍니다.', (255, 255, 255))
        FONT['12'].draw(infoX, infoY - 24, '[기본 5 + 추가 ' + str(chr.ad - 5) + ']', (255, 255, 255))
    elif 64 - 8 <= MOUSE_POSITION[0] <= 64 + 8 and 24 - 8 <= MOUSE_POSITION[1] <= 24 + 8:
        FONT['12'].draw(infoX, infoY, '공격속도', (255, 255, 0))
        FONT['12'].draw(infoX, infoY - 12, '공격 속도가 ' + str(chr.AS) +'% 증가합니다.', (255, 255, 255))
        FONT['12'].draw(infoX, infoY - 24, '[기본 0 + 추가 ' + str(chr.AS) + ']', (255, 255, 255))
    elif 101 - 8 <= MOUSE_POSITION[0] <= 101 + 8 and 24 - 8 <= MOUSE_POSITION[1] <= 24 + 8:
        FONT['12'].draw(infoX, infoY, '치명타 확률', (15, 245, 145))
        FONT['12'].draw(infoX, infoY - 12, str(chr.cri) + '% 확률로 치명타 피해를 입힙니다.', (255, 255, 255))
        FONT['12'].draw(infoX, infoY - 24, '[기본 5 + 추가 ' + str(chr.cri - 5) + ']', (255, 255, 255))
    elif 138 - 8 <= MOUSE_POSITION[0] <= 138 + 8 and 24 - 8 <= MOUSE_POSITION[1] <= 24 + 8:
        FONT['12'].draw(infoX, infoY, '방어력', (82, 219, 255))
        FONT['12'].draw(infoX, infoY - 12, '입는 피해량이 ' + str(chr.df) + ' 감소합니다.', (255, 255, 255))
        FONT['12'].draw(infoX, infoY - 24, '[기본 0 + 추가 ' + str(chr.df) + ']', (255, 255, 255))

def addString(pos, string, color, time, dy, size=12):
    # string : 출력 문자열
    # pos    : 출력 좌표
    # time   : 출력 시간
    # dy     : y축 이동 거리
    STRING_DATA_TO_PRINT.append([pos, string, color, time, dy, size])

def printStringData():
    for i in STRING_DATA_TO_PRINT:
        (x, y), text, color, time, dy, size = i
        cx, cy = get_text_extent(FONT[str(size)], text)

        FONT[str(size)].draw(x - (cx / 5), y + cy, text, color)
        i[0][1] += dy
        i[3]    -= Base.delta_time

        if time <= 0: STRING_DATA_TO_PRINT.remove(i)

def get_text_extent(font, text):
    w, h = c_int(), c_int()
    pico2d.TTF_SizeText(font.font, text.encode('utf-8'), ctypes.byref(w), ctypes.byref(h))
    return w.value, h.value

def eventHandler(e):
    global MOUSE_POSITION
    if e.type == SDL_MOUSEMOTION:
        x, y = e.x, get_canvas_height() - e.y
        MOUSE_POSITION = [x, y]