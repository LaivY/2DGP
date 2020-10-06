from pico2d import *

# Map Resource Path
PATH = '../res/'

class Map:
    Id = 0              # 맵코드
    Size = ()           # 맵크기
    TileInfo = []       # 타일종류, 좌표
    TileLand = []       # 타일마다의 판정범위
    TileSet = None      # 타일셋 이미지

    def load_map(self, mapID):
        Map.Id = mapID
        file = open(PATH + mapID + '.txt', 'r')

        # 맵 사이즈
        fLine = file.readline()
        Map.Size = int(fLine.split()[0]), int(fLine.split()[1])

        # 맵 데이터
        Map.TileInfo = file.readlines()
        file.close()

        # 판정범위 생성
        self.createLand()

    def createLand(self):
        for i in Map.TileInfo:
            f = i.split()
            type = (int(f[0]), int(f[1]))
            pos = (int(f[2]), int(f[3]))
            if type == (0, 10) or type == (0, 7):
                Map.TileLand.append((pos[0] - 16, Map.Size[1] - pos[1] + 16, pos[0] + 16, Map.Size[1] - pos[1]))
                Map.TileLand.append((pos[0], Map.Size[1] - pos[1] + 16, pos[0] - 16, Map.Size[1] - pos[1] - 16))
            elif type == (1, 10) or type == (1, 7):
                Map.TileLand.append((pos[0] - 16, Map.Size[1] - pos[1] + 16, pos[0] + 16, Map.Size[1] - pos[1]))
            elif type == (2, 10) or type == (2, 7):
                Map.TileLand.append((pos[0] - 16, Map.Size[1] - pos[1] + 16, pos[0] + 16, Map.Size[1] - pos[1]))
                Map.TileLand.append((pos[0], Map.Size[1] - pos[1] + 16, pos[0] + 16, Map.Size[1] - pos[1] - 16))
            elif type == (0, 9) or type == (0, 6):
                Map.TileLand.append((pos[0] - 16, Map.Size[1] - pos[1] + 16, pos[0], Map.Size[1] - pos[1] - 16))
            elif type == (2, 9) or type == (2, 6):
                Map.TileLand.append((pos[0], Map.Size[1] - pos[1] + 16, pos[0] + 16, Map.Size[1] - pos[1] - 16))
            elif type == (0, 8) or type == (0, 5):
                Map.TileLand.append((pos[0] - 16, Map.Size[1] - pos[1] + 16, pos[0], Map.Size[1] - pos[1] - 16))
                Map.TileLand.append((pos[0] - 16, Map.Size[1] - pos[1], pos[0] + 16, Map.Size[1] - pos[1] - 16))
            elif type == (1, 8) or type == (1, 5):
                Map.TileLand.append((pos[0] - 16, Map.Size[1] - pos[1], pos[0] + 16, Map.Size[1] - pos[1] - 16))
            elif type == (2, 8) or type == (2, 5):
                Map.TileLand.append((pos[0], Map.Size[1] - pos[1] + 16, pos[0] + 16, Map.Size[1] - pos[1] - 16))
                Map.TileLand.append((pos[0] - 16, Map.Size[1] - pos[1], pos[0] + 16, Map.Size[1] - pos[1] - 16))
            elif type == (6, 10) or type == (5, 9) or type == (6, 9) or type == (7, 9):
                Map.TileLand.append((pos[0] - 16, Map.Size[1] - pos[1], pos[0] + 16, Map.Size[1] - pos[1]))
            elif type == (5, 7) or type == (6, 7) or type == (7, 7):
                Map.TileLand.append(((pos[0] - 16, Map.Size[1] - pos[1] + 16, pos[0] + 16, Map.Size[1] - pos[1] + 16)))
            elif type == (3, 10) or type == (3, 7):
                Map.TileLand.append((pos[0], Map.Size[1] - pos[1], pos[0] + 16, Map.Size[1] - pos[1] - 16))
            elif type == (4, 10) or type == (4, 7):
                Map.TileLand.append((pos[0] - 16, Map.Size[1] - pos[1], pos[0], Map.Size[1] - pos[1] - 16))
            elif type == (3, 9) or type == (3, 6):
                Map.TileLand.append((pos[0], Map.Size[1] - pos[1] + 16, pos[0] + 16, Map.Size[1] - pos[1]))
            elif type == (4, 9) or type == (4, 6):
                Map.TileLand.append((pos[0] - 16, Map.Size[1] - pos[1] + 16, pos[0], Map.Size[1] - pos[1]))

    def draw(self):
        # 타일셋 로드
        if Map.TileSet == None:
            Map.TileSet = load_image(PATH + 'Space_Cave_Tileset.png')
        else:
            for i in Map.TileInfo:
                temp = i.split()
                Map.TileSet.clip_draw(16 * int(temp[0]), 16 * int(temp[1]), 16, 16, int(temp[2]), Map.Size[1] - int(temp[3]), 32, 32)
            # 디버그 :: 바닥판정 그리기
            for i in Map.TileLand:
                draw_rectangle(i[0], i[1], i[2], i[3])

    def isLanded(self, xChr, yChr, dyChr):
        for i in Map.TileLand:
            if i[0] <= xChr <= i[2] and yChr - 37 / 2 >= i[1] and yChr + dyChr - 37 / 2 <= i[1]:
                return True, i[1] + 37 / 2
        return False, 0

    def isCrashed(self, hitBox, dxChr, dyChr):
        for i in Map.TileLand:
            result = isOverlaped(i, hitBox, dxChr, dyChr)
            if result:
                return True, result[1], result[2]
        return False, 0, 0

# 사각형 겹침 체크 함수
def isOverlaped(obj, hitBox, dx, dy):
    # x, y, dx, dy
    RESULT = [0, 0, 0, 0]

    # 머리 부딪힘
    if (dy > 0):
        if (obj[0] < hitBox[0] < obj[2] or obj[0] < hitBox[2] < obj[2]) and \
                (hitBox[3] <= obj[3] <= hitBox[3] + dy or
                 obj[3] <= max(hitBox[1], hitBox[3]) <= obj[1]) and obj[1] != obj[3]:
            return True, 'y', obj[3] - (abs(hitBox[1] - hitBox[3]) / 2)

    # 왼쪽으로 가다가 부딪힘
    if (obj[3] < hitBox[1] < obj[1] or obj[3] < hitBox[3] < obj[1]) and \
            (min(hitBox[0], hitBox[2]) >= obj[2] >= min(hitBox[0], hitBox[2]) + dx or
             min(hitBox[0], hitBox[2]) <= obj[2] <= max(hitBox[0], hitBox[2])) and obj[1] != obj[3]:
        return True, 'x', obj[2] + abs(hitBox[0] - hitBox[2])

    # 오른쪽으로 가다가 부딪힘
    elif (obj[3] <= hitBox[1] < obj[1] or obj[3] <= hitBox[3] < obj[1]) and \
            (max(hitBox[0], hitBox[2]) <= obj[0] <= max(hitBox[0], hitBox[2]) + dx or
             min(hitBox[0], hitBox[2]) <= obj[0] <= max(hitBox[0], hitBox[2])) and obj[1] != obj[3]:
        return True, 'x', obj[0] - abs(hitBox[0] - hitBox[2])

    # 머리 부딪힘
    if (dy < 0):
        if (obj[0] < hitBox[0] < obj[2] or obj[0] < hitBox[2] < obj[2]) and \
                (hitBox[3] <= obj[3] <= hitBox[3] + dy or
                 obj[3] <= max(hitBox[1], hitBox[3]) <= obj[1]) and obj[1] != obj[3]:
            return True, 'y', obj[3] - (abs(hitBox[1] - hitBox[3]) / 2)

    return False