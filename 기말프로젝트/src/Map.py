from pico2d import *

# Map Resource Path
PATH = '../res/'

class Map:
    map = 0
    data = []

    def load_map(self, mapID):
        Map.map = mapID
        file = open(PATH + mapID + '.txt', 'r')
        Map.data = file.readlines()
        file.close()

    def draw(self):
        for i in Map.data:
            temp = i.split()
            draw_rectangle(int(temp[0]), int(temp[1]) - 37 / 2, int(temp[2]), int(temp[3]) - 37 / 2)

    def isLanded(self, xChr, yChr, dyChr):
        for i in Map.data:
            temp = i.split()
            if int(temp[0]) <= xChr <= int(temp[2]) and yChr >= int(temp[1]) and yChr + dyChr <= int(temp[1]):
                return True, int(temp[1])
        return False, 0

    def isCrashed(self, xChr, yChr, dxChr):
        for i in Map.data:
            temp = i.split()
            if temp[1] != temp[3] and int(temp[3]) <= yChr <= int(temp[1]):
                if xChr + 10 <= int(temp[0]) and xChr + dxChr + 10 >= int(temp[0]):
                    return True, int(temp[0]) - 10
                if xChr - 10 >= int(temp[2]) and xChr + dxChr - 10 <= int(temp[2]):
                    return True, int(temp[2]) + 10
        return False, 0
