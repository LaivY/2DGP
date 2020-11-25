from pico2d import *
import gfw
import player

def init():
    global space, stars, life
    space = load_image('res/outerspace.png')
    stars = load_image('res/stars.png')

def update():
    pass

def draw():
    x, y = get_canvas_width() // 2, get_canvas_height() // 2
    
    # 플레이어 위치에 따라 배경이 움직이게
    px, py = player.pos
    dx, dy = px - x, py - y

    space.draw(x + dx * 0.02, y + dy * 0.02)
    stars.draw(x + dx * 0.05, y + dy * 0.05)
