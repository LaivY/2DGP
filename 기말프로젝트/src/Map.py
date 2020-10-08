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
            #for i in Map.TileLand:
            #    draw_rectangle(i[0], i[1], i[2], i[3])

    def chr_Ladning_Check(self, hitBox, dy):
        for i in Map.TileLand:
            # 바닥 도착 조건
            # 1. 히트박스의 좌, 우 중에 하나라도 해당 지형의 폭 사이에 있어야한다.
            # 2. 히트박스의 하단 + dy <= 지형의 상단 <= 히트박스의 하단이여야한다.
            if (i[0] < hitBox[0] < i[2] or i[0] < hitBox[2] < i[2]) and \
                hitBox[3] + dy <= i[1] <= hitBox[3]:
                return True, i[1] + 37 / 2
        return False, 0

    def chr_Collide_Check(self, hitBox, state, subState, dx, dy):
        for i in Map.TileLand:
            RESULT = get_Chr_Collide_Result(i, hitBox, state, subState, dx, dy)
            if RESULT[0]: return RESULT
        return RESULT

def get_Chr_Collide_Result(obj, hitBox, state, subState, dx, dy):
    # x, y, dx, dy
    RESULT = [False, 0, 0, dx, dy]

    # 머리 부딪히는 조건
    # 1. 히트박스의 좌,우 중에 하나라도 해당 지형의 폭 사이에 있어야한다.
    # 2. 히트박스의 상단 + 탐색 범위가 지형의 높이 사이에 있어야한다.
    # 3. 지형의 모양이 사각형이여야한다.
    # 4. 캐릭터가 위로 점프 중이여야한다.
    if (obj[0] < hitBox[0] < obj[2] or obj[0] < hitBox[2] < obj[2]) and \
        obj[3] <= hitBox[1] + dy <= obj[1] and \
        obj[1] != obj[3] and dy > 0:
        RESULT = [True, RESULT[1], RESULT[2] + obj[3] - (abs(hitBox[1] - hitBox[3]) / 2), RESULT[3], 0]

    # 좌측 부딪히는 조건
    # 1. 히트박스의 상, 하 중에 하나라도 해당 지형의 높이 사이에 있어야한다.
    # 2. 히트박스의 좌측 + 탐색 범위가 지형의 오른쪽끝보다 왼쪽에 있고,
    #    히트박스의 좌측이 지형의 오른쪽 끝보단 오른쪽에 있어야한다.
    # 3. 또는 히트박스의 우측이 지형의 폭 사이에 있어야한다.
    # 4. 캐릭터가 좌측으로 이동 중이여야한다.
    elif (obj[3] < hitBox[1] < obj[1] or obj[3] < hitBox[3] < obj[1]) and \
       (min(hitBox[0], hitBox[2]) + dx <= obj[2] <= min(hitBox[0], hitBox[2]) or
        obj[0] < min(hitBox[0], hitBox[2]) + dx < obj[2]) and dx < 0:
        if state == 'run' and subState == 'none':
            RESULT = [True, RESULT[1] + obj[2] + abs(hitBox[0] - hitBox[2]) - dx, RESULT[2], RESULT[3], RESULT[4]]
        else:
            RESULT = [True, RESULT[1] + obj[2] + abs(hitBox[0] - hitBox[2]) + dx, RESULT[2], RESULT[3], RESULT[4]]

    # 우측 부딪히는 조건 :: 좌측과 같음
    elif (obj[3] < hitBox[1] < obj[1] or obj[3] < hitBox[3] < obj[1]) and \
       (max(hitBox[0], hitBox[2]) <= obj[0] <= max(hitBox[0], hitBox[2]) + dx or
        obj[0] < max(hitBox[0], hitBox[2]) + dx < obj[2]) and dx > 0:
        if state == 'run' and subState == 'none':
            RESULT = [True, RESULT[1] + obj[0] - abs(hitBox[0] - hitBox[2]) - dx, RESULT[2], RESULT[3], RESULT[4]]
        else:
            RESULT = [True, RESULT[1] + obj[0] - abs(hitBox[0] - hitBox[2]) + dx, RESULT[2], RESULT[3], RESULT[4]]

    return RESULT