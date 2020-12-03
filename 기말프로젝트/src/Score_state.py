from pico2d import *
from FRAMEWORK import Base
import Main_state, UI

travelData = None

def enter():
    global travelData
    UI.FONT['12'] = load_font('../res/UI/모리스9.ttf', 12)

    try:
        with open('../res/Chr/travel.json', 'r', encoding="utf-8") as f:
            travelData = json.load(f)
    except: pass

def exit():
    pass

def update():
    pass

def draw():
    printTravelData()

def eventHandler(e):
    if (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
        Base.changeState(Main_state)

def printTravelData():
    if travelData == None:
        UI.FONT['12'].draw(400, 300, '이전 기록이 없습니다.', (255, 255, 255))
    else:
        for i in range(len(travelData)):
            UI.FONT['12'].draw(0, 300 + i * 12, str(travelData[i]), (255, 50, 50))