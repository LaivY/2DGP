from pico2d import *

debug = True

class Map:
    TileSet = None      # 타일셋 이미지

    def __init__(self):
        self.id = -1            # 맵코드
        self.size = ()          # 맵크기
        self.tileInfo = []      # 타일종류, 좌표
        self.tileRect = []      # 타일 판정범위
        self.portalRect = []    # 포탈 판정범위

    def load_map(self):
        # TileSet load
        if Map.TileSet is None:
            Map.TileSet = load_image('../res/Map/Space_Cave_Tileset.png')

        # Map file load
        file = open('../res/Map/' + str(self.id) + '.txt', 'r')

        # Save map size
        fLine = file.readline()
        self.size = int(fLine.split()[0]), int(fLine.split()[1])

        # Map Data load
        self.tileInfo = file.readlines()
        file.close()

        # 판정범위 생성
        self.createLand()

    def createLand(self):
        for i in self.tileInfo:
            f = i.split()
            if f[0] == 'm': continue
            type = (int(f[1]), int(f[2]))
            pos  = (int(f[3]), int(f[4]))

            # Add tileRect
            if type == (0, 10) or type == (0, 7):
                self.tileRect.append((pos[0] - 16, self.size[1] - pos[1] + 16, pos[0] + 16, self.size[1] - pos[1]))
                self.tileRect.append((pos[0], self.size[1] - pos[1] + 16, pos[0] - 16, self.size[1] - pos[1] - 16))
            elif type == (1, 10) or type == (1, 7):
                self.tileRect.append((pos[0] - 16, self.size[1] - pos[1] + 16, pos[0] + 16, self.size[1] - pos[1]))
            elif type == (2, 10) or type == (2, 7):
                self.tileRect.append((pos[0] - 16, self.size[1] - pos[1] + 16, pos[0] + 16, self.size[1] - pos[1]))
                self.tileRect.append((pos[0], self.size[1] - pos[1] + 16, pos[0] + 16, self.size[1] - pos[1] - 16))
            elif type == (0, 9) or type == (0, 6):
                self.tileRect.append((pos[0] - 16, self.size[1] - pos[1] + 16, pos[0], self.size[1] - pos[1] - 16))
            elif type == (2, 9) or type == (2, 6):
                self.tileRect.append((pos[0], self.size[1] - pos[1] + 16, pos[0] + 16, self.size[1] - pos[1] - 16))
            elif type == (0, 8) or type == (0, 5):
                self.tileRect.append((pos[0] - 16, self.size[1] - pos[1] + 16, pos[0], self.size[1] - pos[1] - 16))
                self.tileRect.append((pos[0] - 16, self.size[1] - pos[1], pos[0] + 16, self.size[1] - pos[1] - 16))
            elif type == (1, 8) or type == (1, 5):
                self.tileRect.append((pos[0] - 16, self.size[1] - pos[1], pos[0] + 16, self.size[1] - pos[1] - 16))
            elif type == (2, 8) or type == (2, 5):
                self.tileRect.append((pos[0], self.size[1] - pos[1] + 16, pos[0] + 16, self.size[1] - pos[1] - 16))
                self.tileRect.append((pos[0] - 16, self.size[1] - pos[1], pos[0] + 16, self.size[1] - pos[1] - 16))
            elif type == (6, 10) or type == (5, 9) or type == (6, 9) or type == (7, 9):
                self.tileRect.append((pos[0] - 16, self.size[1] - pos[1], pos[0] + 16, self.size[1] - pos[1]))
            elif type == (5, 7) or type == (6, 7) or type == (7, 7):
                self.tileRect.append((pos[0] - 16, self.size[1] - pos[1] + 16, pos[0] + 16, self.size[1] - pos[1] + 16))
            elif type == (3, 10) or type == (3, 7):
                self.tileRect.append((pos[0], self.size[1] - pos[1], pos[0] + 16, self.size[1] - pos[1] - 16))
            elif type == (4, 10) or type == (4, 7):
                self.tileRect.append((pos[0] - 16, self.size[1] - pos[1], pos[0], self.size[1] - pos[1] - 16))
            elif type == (3, 9) or type == (3, 6):
                self.tileRect.append((pos[0], self.size[1] - pos[1] + 16, pos[0] + 16, self.size[1] - pos[1]))
            elif type == (4, 9) or type == (4, 6):
                self.tileRect.append((pos[0] - 16, self.size[1] - pos[1] + 16, pos[0], self.size[1] - pos[1]))

            # Add portalRect
            elif type == (9, 0):
                des, desX, desY = int(f[5]), int(f[6]), int(f[7])
                self.portalRect.append((pos[0] - 16, self.size[1] - pos[1] + 16, pos[0], self.size[1] - pos[1] - 16, des, desX, desY))
            elif type == (10, 0):
                des, desX, desY = int(f[5]), int(f[6]), int(f[7])
                self.portalRect.append((pos[0] - 16, self.size[1] - pos[1], pos[0] + 16, self.size[1] - pos[1] - 16, des, desX, desY))
            elif type == (11, 0):
                des, desX, desY = int(f[5]), int(f[6]), int(f[7])
                self.portalRect.append((pos[0], self.size[1] - pos[1] + 16, pos[0] + 16, self.size[1] - pos[1] - 16, des, desX, desY))
            elif type == (10, 1):
                des, desX, desY = int(f[5]), int(f[6]), int(f[7])
                self.portalRect.append((pos[0] - 16, self.size[1] - pos[1] + 16, pos[0] + 16, self.size[1] - pos[1], des, desX, desY))

    def draw(self):
        for i in self.tileInfo:
            temp = i.split()
            if temp[0] == 't' and (int(temp[1]), int(temp[2])) in [(9, 0), (10, 0), (10, 1), (11, 0)]: continue

            elif temp[0] == 't':
                Map.TileSet.clip_draw(16 * int(temp[1]), 16 * int(temp[2]), 16, 16, int(temp[3]), self.size[1] - int(temp[4]), 32, 32)

        if debug:
            for i in self.portalRect:
                draw_rectangle(i[0], i[1], i[2], i[3])

            for i in self.tileRect:
                draw_rectangle(i[0], i[1], i[2], i[3])
