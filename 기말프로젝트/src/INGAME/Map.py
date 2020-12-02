from pico2d import *
from INGAME import Ingame_state
from INGAME.Monster import Mob, Boss
from FRAMEWORK import DataManager
import UI
debug = False

class Map:
    TileSet = None      # 타일셋 이미지

    def __init__(self):
        self.id = -1            # 맵코드
        self.size = ()          # 맵크기
        self.tileInfo = []      # 타일종류, 좌표
        self.tileRect = []      # 타일 판정범위
        self.portalRect = []    # 포탈 판정범위
        self.objectRect = []    # 상호작용 오브젝트 판정범위

    def load(self):
        # TileSet load
        if Map.TileSet is None:
            Map.TileSet = load_image('../res/Map/tileSet.png')

        # Start map
        if self.id == -1:
            self.id = 100
        self.enterEvent()

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
            type = (int(f[1]), int(f[2]))
            pos = (int(f[3]), int(f[4]))

            # Add Monster
            if f[0] == 'm':
                mobId = 100 * (type[1] + 1) + type[0]
                if mobId == 200:
                    Ingame_state.mob.append(Boss(mobId, *pos))
                else:
                    Ingame_state.mob.append(Mob(mobId, *pos))

                for i in Ingame_state.mob:
                    i.load()

            # Add tileRect
            if type in [(0, 10), (0, 7), (2, 10), (2, 7), (0, 5), (0, 8), (2, 5), (2, 8)]:
                self.tileRect.append((pos[0] - 16, pos[1] + 16, pos[0] + 16, pos[1] - 16))

            elif type == (1, 10) or type == (1, 7):
                self.tileRect.append((pos[0] - 16, pos[1] + 16, pos[0] + 16, pos[1]))
            elif type == (0, 9) or type == (0, 6):
                self.tileRect.append((pos[0] - 16, pos[1] + 16, pos[0], pos[1] - 16))
            elif type == (2, 9) or type == (2, 6):
                self.tileRect.append((pos[0], pos[1] + 16, pos[0] + 16, pos[1] - 16))
            elif type == (1, 8) or type == (1, 5):
                self.tileRect.append((pos[0] - 16, pos[1], pos[0] + 16, pos[1] - 16))
            elif type == (6, 10) or type == (5, 9) or type == (6, 9) or type == (7, 9):
                self.tileRect.append((pos[0] - 16, pos[1], pos[0] + 16, pos[1]))
            elif type == (5, 7) or type == (6, 7) or type == (7, 7):
                self.tileRect.append((pos[0] - 16, pos[1] + 16, pos[0] + 16, pos[1] + 16))
            elif type == (3, 10) or type == (3, 7):
                self.tileRect.append((pos[0], pos[1], pos[0] + 16, pos[1] - 16))
            elif type == (4, 10) or type == (4, 7):
                self.tileRect.append((pos[0] - 16, pos[1], pos[0], pos[1] - 16))
            elif type == (3, 9) or type == (3, 6):
                self.tileRect.append((pos[0], pos[1] + 16, pos[0] + 16, pos[1]))
            elif type == (4, 9) or type == (4, 6):
                self.tileRect.append((pos[0] - 16, pos[1] + 16, pos[0], pos[1]))

            # Add portalRect
            elif type == (9, 0):
                des, desX, desY = int(f[5]), int(f[6]), int(f[7])
                self.portalRect.append((pos[0] - 16, pos[1] + 16, pos[0], pos[1] - 16, des, desX, desY))
            elif type == (10, 0):
                des, desX, desY = int(f[5]), int(f[6]), int(f[7])
                self.portalRect.append((pos[0] - 16, pos[1], pos[0] + 16, pos[1] - 16, des, desX, desY))
            elif type == (11, 0):
                des, desX, desY = int(f[5]), int(f[6]), int(f[7])
                self.portalRect.append((pos[0], pos[1] + 16, pos[0] + 16, pos[1] - 16, des, desX, desY))
            elif type == (10, 1):
                des, desX, desY = int(f[5]), int(f[6]), int(f[7])
                self.portalRect.append((pos[0] - 16, pos[1] + 16, pos[0] + 16, pos[1], des, desX, desY))

            # Add objectRect
            if type == (0, 1):
                self.objectRect.append((type[0], type[1], pos[0] - 8, pos[1], pos[0] + 10, pos[1] - 16))
            elif type == (1, 0):
                text = ''
                for j in range(len(f)):
                    if j <= 4: continue
                    text += f[j] + ' '
                self.objectRect.append((type[0], type[1], pos[0] - 8, pos[1], pos[0] + 10, pos[1] - 16, text))

    def draw(self):
        for i in self.tileInfo:
            temp = i.split()
            if temp[0] == 't' and (int(temp[1]), int(temp[2])) in [(9, 0), (10, 0), (10, 1), (11, 0)]: continue

            elif temp[0] == 't':
                Map.TileSet.clip_draw(16 * int(temp[1]), 16 * int(temp[2]), 16, 16, int(temp[3]), int(temp[4]), 32, 32)

        # 튜토리얼 설명
        self.drawTutorialText()

        if debug:
            for i in self.portalRect:
                draw_rectangle(i[0], i[1], i[2], i[3])

            for i in self.tileRect:
                draw_rectangle(i[0], i[1], i[2], i[3])

            for i in self.objectRect:
                draw_rectangle(i[0], i[1], i[2], i[3])

    def enterEvent(self):
        chr = Ingame_state.chr
        # 맵 입장 시 좌표 기억
        if chr.onlyOnce.get(str(self.id)) == None:
            chr.onlyOnce.update( { str(self.id) : (chr.x, chr.y) } )

        # 지하 N층 표시
        if chr.onlyOnce.get(str(self.id // 100) + 'Floor') == None:
            chr.onlyOnce.update({str(self.id // 100) + 'Floor': True})
            UI.addString([400, 300], '지하' + str(self.id // 100) + '층', (255, 100, 100), 3, 0.05, 24)

        # 보스맵 배경음 변경
        if self.id == 400:
            Ingame_state.changeBGM('../res/Sound/STS_Boss4_v6.mp3')

    def drawTutorialText(self):
        if self.id == 100:
            UI.FONT['12'].draw(80, 212, '← ↑ ↓ → 방향키로 움직일 수 있습니다.', (255, 255, 255))
            UI.FONT['12'].draw(80, 200, '오른쪽으로 계속 가볼까요?', (255, 255, 255))
        elif self.id == 101:
            UI.FONT['12'].draw(30, 252, 'C키로 점프할 수 있습니다.', (255, 255, 255))
            UI.FONT['12'].draw(30, 240, '앞의 벽 위에 올라가보세요!', (255, 255, 255))
            UI.FONT['12'].draw(200, 352, '공중에서 C키를 한 번 더 누르면', (255, 255, 255))
            UI.FONT['12'].draw(200, 340, '2단 점프할 수 있습니다.', (255, 255, 255))
            UI.FONT['12'].draw(600, 200, '계속해서 오른쪽으로 가보죠!', (255, 255, 255))
        elif self.id == 102:
            UI.FONT['12'].draw(30, 200, '저기 상자가 있어요! 확인해보러 갑시다!', (255, 255, 255))
            UI.FONT['12'].draw(450, 550, 'Z키로 상자를 열 수 있어요.', (255, 255, 255))
        elif self.id == 103:
            UI.FONT['12'].draw(20, 212, '저기 몬스터가 있네요. 가서 처치해봅시다.', (255, 255, 255))
            UI.FONT['12'].draw(20, 200, 'X키로 공격할 수 있어요.', (255, 255, 255))
            UI.FONT['12'].draw(450, 300, '공중에서 X키를 누르면 낙하 공격을 합니다.', (255, 255, 255))
            UI.FONT['12'].draw(450, 288, '스페이스바 키로 모션을 캔슬하고 슬라이딩할 수 있습니다.', (255, 255, 255))
        elif self.id == 104:
            UI.FONT['12'].draw(80, 282, '길이 위 아래로 나뉘었어요.', (255, 255, 255))
            UI.FONT['12'].draw(80, 270, '이제부터는 여러분만의 모험을 해보세요!', (255, 255, 255))
            UI.FONT['12'].draw(400, 230, '만약 캐릭터가 버그가 걸렸다면 R키를 눌러서 위치를 재조정할 수 있습니다.', (255, 255, 255))
            UI.FONT['12'].draw(400, 218, '하지만 각 방마다 단 한 번만 사용할 수 있습니다.', (255, 255, 255))