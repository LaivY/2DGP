import Ingame_state
from pico2d import *

img = None

def load():
    global img
    img = load_image('../res/Relic_Set.png')

def draw_relic():
    for i in range(len(Ingame_state.chr.relic)):
        img.clip_draw(Ingame_state.chr.relic[i] % 100 * 128, (Ingame_state.chr.relic[i] // 100 - 1) * 128, 128, 128, 20 + 32 * i, 600 - (Ingame_state.chr.relic[i] // 100) * 20, 64, 64)

def draw():
    draw_relic()