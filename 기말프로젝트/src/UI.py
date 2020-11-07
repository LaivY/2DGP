import Ingame_state
import Framework
from pico2d import *
import ctypes

Relic = None
Font = None
stringData = [];

def load():
    global Relic, Font
    Relic = load_image('../res/Item/relic.png')
    Font = load_font('../res/UI/모리스9.ttf', 12)

def addString(pos, string, color, time, dy):
    # string : 출력 문자열
    # pos    : 출력 좌표
    # time   : 출력 시간
    # dy     : y축 이동 거리
    stringData.append([pos, string, color, time, dy])

def drawRelic():
    for i in range(len(Ingame_state.chr.relic)):
        Relic.clip_draw(Ingame_state.chr.relic[i] % 100 * 128, (Ingame_state.chr.relic[i] // 100 - 1) * 128, 128, 128, 20 + 32 * i, 600 - (Ingame_state.chr.relic[i] // 100) * 20, 64, 64)

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