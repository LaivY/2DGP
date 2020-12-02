import ini
from pico2d import *

Canvas_WIDTH = ini.MAP_WIDTH + 192 * 2
Canvas_HEIGHT = clamp(176 * 2, ini.MAP_HEIGHT, 9999)
SELECT_TYPE = None

def eventHandler():
    global running
    for e in get_events():
        # Exit
        if e.type == SDL_QUIT or (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            running = False
        # Draw selection
        elif e.type == SDL_MOUSEMOTION:
            ini.mPos = e.x + 16, e.y + 16
        # Tile select and add data
        elif (e.type, e.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
            addData(e.x, e.y)
        # Release selection
        elif (e.type, e.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_RIGHT):
            ini.selection = None
        # Print mouse position
        elif (e.type, e.key) == (SDL_KEYDOWN, SDLK_a):
            print(ini.mPos[0], Canvas_HEIGHT - ini.mPos[1])
        # Save
        elif (e.type, e.key) == (SDL_KEYDOWN, SDLK_s):
            saveData()

def drawTileSet():
    for i in range(12):
        for j in range(11):
            tile.clip_draw(16 * i, 16 * j, 16, 16,
                           ini.MAP_WIDTH + 16 + 32 * i, Canvas_HEIGHT - 176 * 2 + 16 + 32 * j, 32, 32)
            draw_rectangle(ini.MAP_WIDTH + 16 + 32 * i - 16, Canvas_HEIGHT - 176 * 2 + 16 + 32 * j - 16,
                           ini.MAP_WIDTH + 16 + 32 * i + 16, Canvas_HEIGHT - 176 * 2 + 16 + 32 * j + 16)

def drawMobSet():
    for i in range(4):
        for j in range(1):
            mob.clip_draw(32 * i, 32 * j, 32, 32, ini.MAP_WIDTH + 16 + 32 * i, Canvas_HEIGHT - 176 * 2 - 16)
            draw_rectangle(ini.MAP_WIDTH + 32 * i, Canvas_HEIGHT - 176 * 2, ini.MAP_WIDTH + 32 * i + 32, Canvas_HEIGHT - 176 * 2 - 32)

def drawSelection():
    global SELECT_TYPE
    if ini.selection is not None:
        if SELECT_TYPE == 'tile':
            tile.clip_draw(16 * ini.selection[0], 16 * ini.selection[1], 16, 16,
                           ini.mPos[0] // 32 * 32, ini.MAP_HEIGHT - (ini.mPos[1] // 32 * 32), 32, 32)
        elif SELECT_TYPE == 'mob':
            mob.clip_draw(32 * ini.selection[0], 32 * ini.selection[1], 32, 32,
                           ini.mPos[0] // 32 * 32, ini.MAP_HEIGHT - (ini.mPos[1] // 32 * 32))

def drawMap():
    for i in ini.DATA:
        if i[0] == 't':
            tile.clip_draw(16 * i[1][0], 16 * i[1][1], 16, 16, i[2], i[3], 32, 32)
        elif i[0] == 'm':
            mob.clip_draw(32 * i[1][0], 32 * i[1][1], 32, 32, i[2], i[3])
    draw_rectangle(0, Canvas_HEIGHT - 1, ini.MAP_WIDTH, Canvas_HEIGHT - ini.MAP_HEIGHT)

def addData(x, y):
    global SELECT_TYPE

    # Tile Select
    for i in range(12):
        for j in range(11):
            if 32 * i + ini.MAP_WIDTH <= x <= 32 * i + 32 + ini.MAP_WIDTH and \
               32 * j + ini.MAP_HEIGHT - 176 * 2 <= ini.MAP_HEIGHT - y <= 32 * j + 32 + ini.MAP_HEIGHT - 176 * 2:
                ini.selection = (i, j)
                SELECT_TYPE = 'tile'
    # Mob Select
    for i in range(4):
        for j in range(1):
            if 32 * i + ini.MAP_WIDTH <= x <= 32 * i + 32 + ini.MAP_WIDTH and \
                0 <= ini.MAP_HEIGHT - y <= ini.MAP_HEIGHT - 176 * 2:
                ini.selection = (i, j)
                SELECT_TYPE = 'mob'
                print(i, j, SELECT_TYPE)

    # Add
    if 0 <= x <= ini.MAP_WIDTH and 0 <= y <= ini.MAP_HEIGHT and ini.selection is not None:
        if SELECT_TYPE == 'tile':
            # Portal
            if ini.selection in [(9, 0), (10, 0), (10, 1), (11, 0)]:
                des = input('Destination : ')

                if ini.selection == (9, 0):
                    xPos = ini.MAP_WIDTH  - (x + 16) // 32 * 32 - 10
                    yPos = ini.MAP_HEIGHT - (y + 16) // 32 * 32
                    print('왼쪽', xPos, yPos)

                elif ini.selection == (10, 0):
                    xPos = (x + 16) // 32 * 32
                    yPos = (y + 16) // 32 * 32
                    print('아래', xPos, yPos)

                elif ini.selection == (10, 1):
                    xPos = (x + 16) // 32 * 32
                    yPos = (y + 16) // 32 * 32 + 10
                    print('위', xPos, yPos)

                elif ini.selection == (11, 0):
                    xPos = ini.MAP_WIDTH  - (x + 16) // 32 * 32 + 10
                    yPos = ini.MAP_HEIGHT - (y + 16) // 32 * 32
                    print('오른쪽', xPos, yPos)

                ini.DATA.append(('t', ini.selection, (x + 16) // 32 * 32, ini.MAP_HEIGHT - (y + 16) // 32 * 32, des, xPos, yPos))
                
            # 표지판
            elif ini.selection == (1, 0):
                text = input('내용 : ')
                ini.DATA.append(('t', ini.selection, (x + 16) // 32 * 32, ini.MAP_HEIGHT - (y + 16) // 32 * 32, text))
            
            # Normal
            else:
                ini.DATA.append(('t', ini.selection, (x + 16) // 32 * 32, ini.MAP_HEIGHT - (y + 16) // 32 * 32))
        elif SELECT_TYPE == 'mob':
            ini.DATA.append(('m', ini.selection, (x + 16) // 32 * 32, ini.MAP_HEIGHT - (y + 16) // 32 * 32))

def saveData():
    f = open(str(ini.MAPID) + '.txt', 'w')
    f.write(str(ini.MAP_WIDTH) + ' ' + str(ini.MAP_HEIGHT) + '\n')
    for data in ini.DATA:
        Category     = data[0]
        Type1, Type2 = data[1]
        xPos, yPos   = data[2], data[3]

        if Category == 't' and (Type1, Type2) in [(11, 0), (10, 0), (9, 0), (10, 1)]:
            f.write(str(Category) + ' ' + str(Type1) + ' ' + str(Type2) + ' ' + str(xPos) + ' ' + str(yPos) + ' ' + str(data[4]) + ' ' + str(data[5]) + ' ' + str(data[6]) + '\n')
        elif Category == 't' and (Type1, Type2) == (1, 0):
            text = ''
            for i in range(len(data)):
                if i <= 3: continue
                text += data[i]
            f.write(str(Category) + ' ' + str(Type1) + ' ' + str(Type2) + ' ' + str(xPos) + ' ' + str(yPos) + ' ' + text + '\n')
        else:
            f.write(str(Category) + ' ' + str(Type1) + ' ' + str(Type2) + ' ' + str(xPos) + ' ' + str(yPos) + '\n')
    f.close()
    print('저장완료')

running = True
open_canvas(Canvas_WIDTH, Canvas_HEIGHT)
tile = load_image(ini.path + 'tileSet.png')
mob = load_image('mob_sheet.png')
while running:
    clear_canvas()

    drawMap()
    drawTileSet()
    drawMobSet()
    drawSelection()
    eventHandler()

    update_canvas()
close_canvas()
