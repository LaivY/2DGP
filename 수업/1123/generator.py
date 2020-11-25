from pico2d import *
import gfw
from missile import *
import random

# 미사일 생성 갯수
MISSILE_COUNT = 10

# 아이템 생성 갯수
ITEM_COUNT = 2

def init():
    pass

def update(s):
    global score
    score = s
    max_missile_count = MISSILE_COUNT + score // 10
    while gfw.world.count_at(gfw.layer.missile) < max_missile_count:
        generate_missile()
    while gfw.world.count_at(gfw.layer.item) < ITEM_COUNT:
        generate_item()

def generate_missile():
    x, y, dx, dy = get_coords()

    m = Missile((x, y), (dx, dy))
    gfw.world.add(gfw.layer.missile, m)

def generate_item():
    x, y, dx, dy = get_coords()
    item = random.choice([PresentItem, CoinItem])
    i = item((x, y), (dx, dy))
    gfw.world.add(gfw.layer.item, i)

def get_coords():
    x = random.randrange(get_canvas_width())
    y = random.randrange(get_canvas_height())

    # 두 값 사이의 랜덤한 실수값
    dx = random.random()
    dy = random.random()
    if dx < 0.5: dx -= 1
    if dy < 0.5: dy -= 1

    # 스피드 설정
    speed = 1 + score / 60
    dx *= speed
    dy *= speed

    # 어느쪽 면에서 생성될 지
    side = random.randint(1, 4)

    if side == 1: # 왼쪽
        x = 0
    elif side == 2: # 아래
        y = 0
    elif side == 3: # 오른쪽
        x = get_canvas_width()
    else: # 위
        y = get_canvas_height()

    return x, y, dx, dy
