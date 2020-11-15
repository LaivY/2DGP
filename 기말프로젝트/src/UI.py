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

    chr_info_image['base'] = load_image('../res/UI/CHR_INFO_UI_BASE.png')
    chr_info_image['hpbar'] = load_image('../res/UI/CHR_HP_BAR.png')
    chr_info_image['ad'] = load_image('../res/UI/ad.png')
    chr_info_image['as'] = load_image('../res/UI/as.png')
    chr_info_image['df'] = load_image('../res/UI/df.png')
    chr_info_image['sp'] = load_image('../res/UI/speed.png')

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
        relic_image.clip_draw(chr.relic[i].id % 100 * 128, (chr.relic[i].id // 100 - 1) * 128, 128, 128, 20 + 32 * i, 600 - (chr.relic[i].id // 100) * 20, 64, 64)
        if chr.relic[i].stack != -1:
            if chr.relic[i].isActive:
                rgb = (50, 255, 50)
            else:
                rgb = (255, 255, 255)
            Font12.draw(26 + 32 * i, 600 - (chr.relic[i].id // 100) * 20 - 8, str(chr.relic[i].stack), rgb)

def drawRelicDesc():
    r = Ingame_state.chr.relic
    for i in range(len(r)):
        if 20 + 32 * i - 16 < mPos[0] < 20 + 32 * i + 16 and \
           580 - 16 < mPos[1] < 580 + 16:
            Font12.draw(6 + 32 * i, 556, str(r[i].name), (255, 255, 255))
            Font12.draw(6 + 32 * i, 544, str(r[i].desc), (255, 255, 255))
            Font12.draw(6 + 32 * i, 532, str(r[i].flavorText), (150, 150, 150))

def drawChrInfo():
    chr = Ingame_state.chr

    # 체력바
    chr_info_image['hpbar'].clip_draw_to_origin(0, 0, 154, 12, 12, 37, chr.hp / chr.localMaxHP * 154, 12)

    # 베이스
    chr_info_image['base'].draw_to_origin(10, 10, 158, 41)

    # 체력
    Font12.draw(72, 42, str(chr.hp) + ' / ' + str(chr.localMaxHP), (255, 255, 255))

    # 공격력
    chr_info_image['ad'].clip_draw(0, 0, 72, 72, 25 + 2, 24, 16, 16)
    Font12.draw(37, 23, str(chr.ad), (255, 255, 255))

    # 공격속도
    chr_info_image['as'].clip_draw(0, 0, 72, 72, 62 + 2, 24, 16, 16)
    Font12.draw(74, 23, str(chr.AS), (255, 255, 255))

    # 방어력
    chr_info_image['df'].clip_draw(0, 0, 72, 72, 99 + 2, 24, 16, 16)
    Font12.draw(111, 23, str(chr.df), (255, 255, 255))

    # 이동속도
    chr_info_image['sp'].clip_draw(0, 0, 72, 72, 136 + 2, 24, 16, 16)
    Font12.draw(148, 23, str(chr.speed), (255, 255, 255))

def drawChrInfoDesc():
    chr = Ingame_state.chr
    infoX, infoY = 173, 42
    if 12 <= mPos[0] <= 12 + 154 and 37 <= mPos[1] <= 37 + 12:
        Font12.draw(infoX, infoY, str('체력'), (244, 41, 65))
        Font12.draw(infoX, infoY - 12, str('0이 되면 캐릭터가 사망합니다.'), (255, 255, 255))
        Font12.draw(infoX, infoY - 24, '[기본 50 + 추가 ' + str(chr.localMaxHP - 50) + ']', (255, 255, 255))
    elif 25 - 8 <= mPos[0] <= 25 + 8 and 24 - 8 <= mPos[1] <= 24 + 8:
        Font12.draw(infoX, infoY, '공격력', (246, 70, 91))
        Font12.draw(infoX, infoY - 12, '공격으로 ' + str(chr.ad) + ' 만큼의 피해를 줍니다.', (255, 255, 255))
        Font12.draw(infoX, infoY - 24, '[기본 5 + 추가 ' + str(chr.ad - 5) + ']', (255, 255, 255))
    elif 64 - 8 <= mPos[0] <= 64 + 8 and 24 - 8 <= mPos[1] <= 24 + 8:
        Font12.draw(infoX, infoY, '공격속도', (255, 255, 0))
        Font12.draw(infoX, infoY - 12, '공격 속도가 ' + str(chr.AS) +'% 증가합니다.', (255, 255, 255))
        Font12.draw(infoX, infoY - 24, '[기본 0 + 추가 ' + str(chr.AS) + ']', (255, 255, 255))
    elif 101 - 8 <= mPos[0] <= 101 + 8 and 24 - 8 <= mPos[1] <= 24 + 8:
        Font12.draw(infoX, infoY, '방어력', (15, 245, 145))
        Font12.draw(infoX, infoY - 12, '입는 피해량이 ' + str(chr.df) + ' 감소합니다.', (255, 255, 255))
        Font12.draw(infoX, infoY - 24, '[기본 0 + 추가 ' + str(chr.df) + ']', (255, 255, 255))
    elif 138 - 8 <= mPos[0] <= 138 + 8 and 24 - 8 <= mPos[1] <= 24 + 8:
        Font12.draw(infoX, infoY, '이동속도', (82, 219, 255))
        Font12.draw(infoX, infoY - 12, '이동하는 속도가 ' + str(chr.speed) + '% 증가합니다.', (255, 255, 255))
        Font12.draw(infoX, infoY - 24, '[기본 0 + 추가 ' + str(chr.speed) + ']', (255, 255, 255))

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
    drawRelicDesc()
    drawChrInfo()
    drawChrInfoDesc()
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