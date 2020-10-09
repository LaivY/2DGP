import Framework
import Ingame_state
from pico2d import *

def eventHandler(e):
    if e.type == SDL_QUIT or (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
        Framework.running = False
    elif (e.type, e.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
        # 241 x 49
        if 800 / 2 - 241 / 2 <= e.x <= 800 / 2 + 241 / 2:
            if 295 <= e.y <= 295 + 49:
                Framework.changeState(Ingame_state)
            elif 366 <= e.y <= 366 + 49:
                pass
            elif 436 <= e.y <= 436 + 49:
                Framework.running = False

def update():
    pass

def draw():
    bgr.draw(bgr.w / 2, bgr.h / 2)
    for i in range(len(button)):
        button[i].draw(800 / 2, 600 / 2 - 20 - 70 * i)


def enter():
    global bgr, button
    bgr = load_image('../res/UI/Main/bgr.png')
    button = load_image('../res/UI/Main/button_start.png'), load_image('../res/UI/Main/button_continue.png'), load_image('../res/UI/Main/button_exit.png')

def exit():
    del bgr, button
