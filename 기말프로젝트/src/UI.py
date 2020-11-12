import Ingame_state
import Framework
import Relic
from pico2d import *
import ctypes

Font12 = None
stringData = []
relic_image = None
chr_info_image = {}
mPos = [0, 0]

def load():
    global Font12, relic_image
    Font12 = load_font('../res/UI/모리스9.ttf', 12)
    relic_image = load_image('../res/Item/relic.png')


    chr_info_image['ad'] = load_image('../res/UI/ad.png')


    Relic.loadRelicData()

def eventHandler(event):
    global mPos
    if event.type == SDL_MOUSEMOTION:
        x, y = event.x, 600 - event.y
        mPos = [x, y]

def addString(pos, string, color, time, dy):
    # string : 출력 문자열
    # pos    : 출력 좌표
    # time   : 출력 시간
    # dy     : y축 이동 거리
    stringData.append([pos, string, color, time, dy])

def drawRelic():
    chr = Ingame_state.chr
    for i in range(len(chr.relic)):
        #draw_rectangle(20 + 32 * i - 16, 580 - 16, 20 + 32 * i + 16, 580 + 16)
        relic_image.clip_draw(chr.relic[i].id % 100 * 128, (chr.relic[i].id // 100 - 1) * 128, 128, 128, 20 + 32 * i, 600 - (chr.relic[i].id // 100) * 20, 64, 64)
        if chr.relic[i].stack != -1:
            if chr.relic[i].isActive:
                rgb = (50, 255, 50)
            else:
                rgb = (255, 255, 255)
            Font12.draw(26 + 32 * i, 600 - (chr.relic[i].id // 100) * 20 - 8, str(chr.relic[i].stack), rgb)

def drawRelicInfo():
    r = Ingame_state.chr.relic
    for i in range(len(r)):
        if 20 + 32 * i - 16 <= mPos[0] <= 20 + 32 * i + 16 and \
           580 - 16 <= mPos[1] <= 580 + 16:
            Font12.draw(mPos[0], mPos[1] - 32, str(r[i].name), (255, 255, 255))
            Font12.draw(mPos[0], mPos[1] - 44, str(r[i].desc), (255, 255, 255))
            Font12.draw(mPos[0], mPos[1] - 56, str(r[i].flavorText), (150, 150, 150))

def drawChrInfo():
    chr = Ingame_state.chr

    # 공격력
    chr_info_image['ad'].clip_draw(0, 0, 72, 72, 400, 30, 16, 16)
    Font12.draw(416, 30, str(chr.ad), (255, 255, 255))

    # 공격속도
    chr_info_image['as'].clip_draw(0, 0, 72, 72, 400, 30, 16, 16)
    Font12.draw(416, 30, str(chr.AS), (255, 255, 255))

   Font12.draw(400, 16, str(chr.hp) + '/' + str(chr.localMaxHP), (255, 255, 255))


def printStringData():
    for i in stringData:
        cx, cy = GetTextDimensions(i[1], 7, '모리스9')

        Font12.draw(i[0][0] - cx, i[0][1] + cy + 5, i[1], i[2])
        i[3] -= Framework.delta_time
        i[0][1] += i[4]
        if i[3] <= 0:
            stringData.remove(i)

def draw():
    drawRelic()
    drawRelicInfo()
    drawChrInfo()
    printStringData()

def GetTextDimensions(text, points, font):
    # 문자열 길이 반환 함수
    class SIZE(ctypes.Structure):
        _fields_ = [("cx", ctypes.c_long), ("cy", ctypes.c_long)]

    hdc = ctypes.windll.user32.GetDC(0)
    hfont = ctypes.windll.gdi32.CreateFontA(points, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, font)
    hfont_old = ctypes.windll.gdi32.SelectObject(hdc, hfont)

    size = SIZE(0, 0)
    ctypes.windll.gdi32.GetTextExtentPoint32W(hdc, text, len(text), ctypes.byref(size))

    ctypes.windll.gdi32.SelectObject(hdc, hfont_old)
    ctypes.windll.gdi32.DeleteObject(hfont)
    return (size.cx, size.cy)