import ini
from pico2d import *

Canvas_WIDTH = ini.MAP_WIDTH + 192 * 2
Canvas_HEIGHT = clamp(176 * 2, ini.MAP_HEIGHT, 9999)

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

def drawSelection():
    if ini.selection is not None:
        tile.clip_draw(16 * ini.selection[0], 16 * ini.selection[1], 16, 16,
                       ini.mPos[0] // 32 * 32, ini.MAP_HEIGHT - (ini.mPos[1] // 32 * 32), 32, 32)

def drawMap():
    for i in ini.DATA:
        tile.clip_draw(16 * i[0][0], 16 * i[0][1], 16, 16,
                       i[1], Canvas_HEIGHT - i[2], 32, 32)
    draw_rectangle(0, Canvas_HEIGHT - 1, ini.MAP_WIDTH, Canvas_HEIGHT - ini.MAP_HEIGHT)

def addData(x, y):
    # Select
    for i in range(12):
        for j in range(11):
            if 32 * i + ini.MAP_WIDTH <= x <= 32 * i + 32 + ini.MAP_WIDTH and \
                    32 * j + ini.MAP_HEIGHT - 176 * 2 <= ini.MAP_HEIGHT - y <= 32 * j + 32 + ini.MAP_HEIGHT - 176 * 2:
                ini.selection = (i, j)
    # Add
    if 0 <= x <= ini.MAP_WIDTH and 0 <= y <= ini.MAP_HEIGHT and ini.selection is not None:
        # Portal
        if ini.selection in [(11, 0), (10, 0), (9, 0), (10, 1)]:
            des = int(input('Destination : '))
            xPos = int(input('x : '))
            yPos = int(input('y : '))
            ini.DATA.append((ini.selection, (x + 16) // 32 * 32, (y + 16) // 32 * 32, des, xPos, yPos))
        # Normal
        else:
            ini.DATA.append((ini.selection, (x + 16) // 32 * 32, (y + 16) // 32 * 32))

def saveData():
    f = open(str(ini.MAPID) + '.txt', 'w')
    f.write(str(ini.MAP_WIDTH) + ' ' + str(ini.MAP_HEIGHT) + '\n')
    for data in ini.DATA:
        a = data[0][0]
        b = data[0][1]
        c = data[1]
        d = data[2]
        if (a, b) in [(11, 0), (10, 0), (9, 0), (10, 1)]:
            f.write(str(a) + ' ' + str(b) + ' ' + str(c) + ' ' + str(d) + ' ' + str(data[3]) + ' ' + str(data[4]) + ' ' + str(data[5]) + '\n')
        else:
            f.write(str(a) + ' ' + str(b) + ' ' + str(c) + ' ' + str(d) + '\n')
    f.close()
    print('저장완료')


running = True
open_canvas(Canvas_WIDTH, Canvas_HEIGHT)
tile = load_image(ini.path + 'Space_Cave_Tileset.png')
while running:
    clear_canvas()

    drawMap()
    drawTileSet()
    drawSelection()
    eventHandler()

    update_canvas()
close_canvas()
