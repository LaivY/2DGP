from pico2d import *
from FRAMEWORK import Base
from INGAME.Map import Map
from INGAME.Monster import Monster, Boss, Mob
from INGAME.Character import Character
import UI

# 선언
mob = []
map = Map()
chr = Character()

def eventHandler(e):
    if e.type == SDL_QUIT or (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
        Base.running = False

    # 캐릭터 이벤트처리
    chr.eventHandler(e)

    # UI 이벤트처리
    UI.eventHandler(e)

def update():
    chr.update(Base.delta_time)
    for i in mob:
        if chr.state == 'idle':
            i.hitBy = 'none'
        i.update(Base.delta_time)

def draw():
    map.draw()
    for i in mob:
        i.draw()
    chr.draw()
    UI.draw()

def enter():
    map.load()
    chr.load()
    UI.load()
