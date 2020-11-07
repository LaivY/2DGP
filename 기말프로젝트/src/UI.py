import Ingame_state
import Framework
from pico2d import *
import ctypes

Font = None
stringData = []
relic_image = None

def load():
    global Font, relic_image
    Font = load_font('../res/UI/모리스9.ttf', 12)
    relic_image = load_image('../res/Item/relic.png')

def eventHandler(event):
    if event.type == SDL_MOUSEMOTION:
        x, y = event.x, 600 - event.y
        #if

def addString(pos, string, color, time, dy):
    # string : 출력 문자열
    # pos    : 출력 좌표
    # time   : 출력 시간
    # dy     : y축 이동 거리
    stringData.append([pos, string, color, time, dy])

def drawRelic():
    chr = Ingame_state.chr
    for i in range(len(chr.relic)):
        relic_image.clip_draw(chr.relic[i].id % 100 * 128, (chr.relic[i].id // 100 - 1) * 128, 128, 128, 20 + 32 * i, 600 - (chr.relic[i].id // 100) * 20, 64, 64)
        if chr.relic[i].stack != -1:
            if chr.relic[i].isActive:
                rgb = (50, 255, 50)
            else:
                rgb = (255, 255, 255)
            Font.draw(26 + 32 * i, 600 - (chr.relic[i].id // 100) * 20 - 8, str(chr.relic[i].stack), rgb)

def printStringData():
    for i in stringData:
        cx, cy = GetTextDimensions(i[1], 16, '모리스9')
        Font.draw(i[0][0] - cx, i[0][1] + cy + 5, i[1], i[2])
        i[3] -= Framework.delta_time
        i[0][1] += i[4]
        if i[3] <= 0:
            stringData.remove(i)

def draw():
    drawRelic()
    printStringData()

def GetTextDimensions(text, points, font):
    # 문자열 길이 반환 함수
    class SIZE(ctypes.Structure):
        _fields_ = [("cx", ctypes.c_long), ("cy", ctypes.c_long)]

    hdc = ctypes.windll.user32.GetDC(0)
    hfont = ctypes.windll.gdi32.CreateFontA(points, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, font)
    hfont_old = ctypes.windll.gdi32.SelectObject(hdc, hfont)

    size = SIZE(0, 0)
    ctypes.windll.gdi32.GetTextExtentPoint32A(hdc, text, len(text), ctypes.byref(size))

    ctypes.windll.gdi32.SelectObject(hdc, hfont_old)
    ctypes.windll.gdi32.DeleteObject(hfont)
    return (size.cx, size.cy)