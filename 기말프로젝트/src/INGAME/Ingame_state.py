from pico2d import *
from FRAMEWORK import Base, DataManager
from INGAME.Map import Map
from INGAME.Monster import Monster, Boss, Mob
from INGAME.Character import Character
from INGAME import Projectile
import UI

# 선언
mob = []
map = Map()
chr = Character()
BGM = None

def eventHandler(e):
    if e.type == SDL_QUIT or (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
        Base.running = False

    # 캐릭터 이벤트처리
    chr.eventHandler(e)

    # UI 이벤트처리
    UI.eventHandler(e)

def update():
    chr.update(Base.FRAME_SLEEP_TIME)
    for i in mob:
        if chr.state == 'idle':
            i.hitBy = 'none'
        i.update(Base.FRAME_SLEEP_TIME)

def draw():
    map.draw()
    for i in mob:
        i.draw()

    for p in Projectile.Projectiles:
        p.update(chr)
        p.draw()

    chr.draw()
    UI.draw()

def enter():
    global BGM
    BGM = DataManager.load('res/Sound/STS_Level1_NewMix_v1.mp3')
    BGM.repeat_play()

    map.load()
    chr.load()
    UI.load()

def exit():
    global mob, map, chr, BGM
    mob.clear()
    map.tileRect.clear()
    map.portalRect.clear()
    map.objectRect.clear()
    map.id = -1
    Projectile.Projectiles.clear()
    chr.ini()
    BGM = None

def changeBGM(file, roop=True):
    global BGM
    newBGM = DataManager.load(file)
    if BGM == newBGM:
        return
    else:
        BGM.stop()
        BGM = newBGM

        if roop:
            BGM.repeat_play()
        else:
            BGM.play(1)
