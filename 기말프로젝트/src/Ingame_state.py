import Framework
from pico2d import *
from Map import Map
from Character import Character

# Create
m = Map()
c = Character()

def eventHandler(e):
    if e.type == SDL_QUIT or (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
        Framework.running = False
    # 캐릭터 이벤트처리
    c.eventHandler(e)

def update():
    c.update(Framework.delta_time)

def draw():
    m.draw()
    c.draw()

def enter():
    c.image = load_image('../res/adventurer-v1.5-Sheet.png')
    if m.id == 0: m.id = 100
    m.load_map()

def chr_collide_check():
    for tile in m.tileRect:
        # x, y, dx, dy
        RESULT = [False, 0, 0, c.dx, c.dy]

        # 머리 부딪히는 조건
        # 1. 히트박스의 좌,우 중에 하나라도 해당 지형의 폭 사이에 있어야한다.
        # 2. 히트박스의 상단 + 탐색 범위가 지형의 높이 사이에 있어야한다.
        # 3. 지형의 모양이 사각형이여야한다.
        # 4. 캐릭터가 위로 점프 중이여야한다.
        if (tile[0] < c.hitBox[0] < tile[2] or tile[0] < c.hitBox[2] < tile[2]) and \
            tile[3] <= c.hitBox[1] + c.dy <= tile[1] != tile[3] and c.dy > 0:
            RESULT = [True, RESULT[1], RESULT[2] + tile[3] - (abs(c.hitBox[1] - c.hitBox[3]) / 2), RESULT[3], 0]

        # 좌측 부딪히는 조건
        # 1. 히트박스의 상, 하 중에 하나라도 해당 지형의 높이 사이에 있어야한다.
        # 2. 히트박스의 좌측 + 탐색 범위가 지형의 오른쪽끝보다 왼쪽에 있고,
        #    히트박스의 좌측이 지형의 오른쪽 끝보단 오른쪽에 있어야한다.
        # 3. 또는 히트박스의 우측이 지형의 폭 사이에 있어야한다.
        # 4. 캐릭터가 좌측으로 이동 중이여야한다.
        elif (tile[3] < c.hitBox[1] < tile[1] or tile[3] < c.hitBox[3] < tile[1]) and \
             (min(c.hitBox[0], c.hitBox[2]) + c.dx <= tile[2] <= min(c.hitBox[0], c.hitBox[2]) or
              tile[0] < min(c.hitBox[0], c.hitBox[2]) + c.dx < tile[2]) and c.dx < 0:
            if c.state == 'run' and c.subState == 'none':
                RESULT = [True, RESULT[1] + tile[2] + abs(c.hitBox[0] - c.hitBox[2]) - c.dx, RESULT[2], RESULT[3], RESULT[4]]
            else:
                RESULT = [True, RESULT[1] + tile[2] + abs(c.hitBox[0] - c.hitBox[2]) + c.dx, RESULT[2], RESULT[3], RESULT[4]]

        # 우측 부딪히는 조건 :: 좌측과 같음
        elif (tile[3] < c.hitBox[1] < tile[1] or tile[3] < c.hitBox[3] < tile[1]) and \
             (max(c.hitBox[0], c.hitBox[2]) <= tile[0] <= max(c.hitBox[0], c.hitBox[2]) + c.dx or
              tile[0] < max(c.hitBox[0], c.hitBox[2]) + c.dx < tile[2]) and c.dx > 0:
            if c.state == 'run' and c.subState == 'none':
                RESULT = [True, RESULT[1] + tile[0] - abs(c.hitBox[0] - c.hitBox[2]) - c.dx, RESULT[2], RESULT[3], RESULT[4]]
            else:
                RESULT = [True, RESULT[1] + tile[0] - abs(c.hitBox[0] - c.hitBox[2]) + c.dx, RESULT[2], RESULT[3], RESULT[4]]

        if RESULT[0]: return RESULT
    return [False]

def chr_ladning_check():
    for tile in m.tileRect:
        # 바닥 도착 조건
        # 1. 히트박스의 좌, 우 중에 하나라도 해당 지형의 폭 사이에 있어야한다.
        # 2. 히트박스의 하단 + dy <= 지형의 상단 <= 히트박스의 하단이여야한다.
        if (tile[0] < c.hitBox[0] < tile[2] or tile[0] < c.hitBox[2] < tile[2]) and \
            c.hitBox[3] + c.dy <= tile[1] <= c.hitBox[3]:
            return True, tile[1] + 37 / 2
    return [False]

def chr_portal_check():
    for portal in m.portalRect:
        PASS = False
        if c.hitBox[2] < portal[0]: PASS = True
        if c.hitBox[3] > portal[1]: PASS = True
        if c.hitBox[0] > portal[2]: PASS = True
        if c.hitBox[1] < portal[3]: PASS = True
        if not PASS:
            # if chr is in destination
            if m.id == portal[4]:
                c.subState = 'jump2'
                c.x, c.y = portal[5], portal[6]
                print(c.x, c.y)
            else:
                m.id = portal[4]
                m.tileRect.clear()
                m.portalRect.clear()
                m.load_map()
                c.x, c.y = portal[5], portal[6]
                c.subState = 'jump2'
            return
