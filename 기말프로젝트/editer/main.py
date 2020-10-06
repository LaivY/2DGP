from pico2d import *
# 수동설정
MAPID = 200
MAP_WIDTH = 800
MAP_HEIGHT = 600
open_canvas(MAP_WIDTH + 192 * 2, MAP_HEIGHT)

# 타일셋 로드
PATH = '../res/'
tile = load_image(PATH + 'Space_Cave_Tileset.png')

# 현재 선택한 타일셋
Selection = None

# 저장될 데이터
DATA = []

# 배경 타일
BGR = (11, 10)

# 마우스 좌표
mPos = (0, 0)

def eventHandler():
    global running, Selection, DATA, mPos
    for e in get_events():
        # 종료
        if e.type == SDL_QUIT or (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            running = False
        # 선택한 타일 그리기    
        elif e.type == SDL_MOUSEMOTION:
            if Selection is not None:
                tile.clip_draw(16 * Selection[0], 16 * Selection[1], 16, 16, e.x // 32 * 32, MAP_HEIGHT - (e.y // 32 * 32), 32, 32)
                mPos = e.x, e.y
        # 타일 선택, 타일 저장
        elif (e.type, e.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
            for i in range(12):
                for j in range(11):
                    if 32 * i + MAP_WIDTH <= e.x <= 32 * i + 32 + MAP_WIDTH and \
                       32 * j + MAP_HEIGHT - 176 * 2 <= MAP_HEIGHT - e.y <= 32 * j + 32 + MAP_HEIGHT - 176 * 2:
                        Selection = (i, j)
            if 0 <= e.x <= MAP_WIDTH and 0 <= e.y <= MAP_HEIGHT and Selection is not None:
                DATA.append((Selection, e.x // 32 * 32, e.y // 32 * 32))
        # 타일 선택 해제
        elif (e.type, e.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_RIGHT):
            Selection = None
        # 저장
        elif (e.type, e.key) == (SDL_KEYDOWN, SDLK_s):
            saveDATA()
            print('저장완료')

def drawTileSet():
    for i in range(12):
        for j in range(11):
            tile.clip_draw(16 * i, 16 * j, 16, 16,
                           32 * i + 16 + MAP_WIDTH, 32 * j + 16 + MAP_HEIGHT - 176 * 2, 32, 32)
            draw_rectangle(32 * i + MAP_WIDTH, 32 * j + MAP_HEIGHT - 176 * 2, 32 * i + 32 + MAP_WIDTH, 32 * j + 32 + MAP_HEIGHT - 176 * 2)

def drawSelection():
    if Selection != None:
        tile.clip_draw(16 * Selection[0], 16 * Selection[1], 16, 16,
                       mPos[0] // 32 * 32, MAP_HEIGHT - (mPos[1] // 32 * 32), 32, 32)

def drawMap():
    for i in DATA:
        tile.clip_draw(16 * i[0][0], 16 * i[0][1], 16, 16,
                       i[1], MAP_HEIGHT - i[2], 32, 32)
    draw_rectangle(0, 0, MAP_WIDTH, MAP_HEIGHT)

def setBGR():
    for i in range(MAP_WIDTH // 32 + 1):
        for j in range(MAP_HEIGHT // 32 + 2):
            DATA.append((BGR, i * 32, j * 32))

def saveDATA():
    f = open(str(MAPID) + '.txt', 'w')
    f.write(str(MAP_WIDTH) + ' ' + str(MAP_HEIGHT) + '\n')
    for i in range(len(DATA)):
        a = DATA[i][0][0]
        b = DATA[i][0][1]
        c = DATA[i][1]
        d = DATA[i][2]
        f.write(str(a) + ' ' + str(b) + ' ' + str(c) + ' ' + str(d) + '\n')
    f.close()

running = True
setBGR()
while running:
    clear_canvas()

    drawMap()
    drawTileSet()
    drawSelection()
    eventHandler()

    update_canvas()
close_canvas()
