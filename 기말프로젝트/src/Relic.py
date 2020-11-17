import Ingame_state
import UI
import json
from random import randint

relic_data = {}

class relic:
    image = None
    def __init__(self, _id):
        self.id = _id
        self.name = "name"
        self.desc = "desc"
        self.flavorText = "flavorText"
        self.stack = -1
        self.condition = -1
        self.isActive = False

def addRandomRelic():
    chr = Ingame_state.chr
    inven = chr.relic

    # 모든 유물을 갖고있을 경우
    if len(inven) >= 10:
        UI.addString([chr.x, chr.y + 5], '더 이상 획득할 유물이 없습니다.', (255, 255, 255), 1, 0.1)
        return

    # 중복없이 랜덤으로 한 개 획득
    while True:
        Pass = True
        rarity = randint(0, 99)

        if 0 <= rarity < 50:
            _id = randint(100, 106)
        elif 50 <= rarity <= 75:
            _id = randint(200, 206)
        else:
            _id = randint(300, 306)

        for i in inven:
            if i.id == _id:
                Pass = False
                break
        if Pass:
            # 유물 데이터 설정
            r = relic(_id)
            r.name = relic_data[str(_id)]['NAME']
            r.desc = relic_data[str(_id)]['DESC']
            r.flavorText = relic_data[str(_id)]['FLAVOR_TEXT']
            
            if r.name == '룬 12면체':
                r.stack = 0
                r.condition = 1
            elif r.name == '펜 촉':
                r.stack = 0
                r.condition = 5
            elif r.name == '마트료시카':
                r.stack = 1
                r.condition = 1
            elif r.name == '붉은 해골':
                r.stack = 0
                r.condition = 1
            elif r.name == '수리검':
                r.stack = 0
                r.condition = 3
            elif r.name == '표창':
                r.stack = 0
                r.condition = 3
            elif r.name == '도마뱀 꼬리':
                r.stack = 1
                r.condition = 1
            elif r.name == '조개 화석':
                r.stack = 1
                r.condition = 1
            elif r.name == '향로':
                r.stack = 0
                r.condition = 6
            
            inven.append(r)
            UI.addString([chr.x, chr.y + 5], str(relic_data[str(_id)]['NAME']) + '을(를) 획득했습니다!', (255, 255, 255), 1, 0.1)
            break

    updateChrStat()
    updataRelicStack()

def updateChrStat():
    chr = Ingame_state.chr

    # 계산 전에 캐릭터 스탯 초기화
    chr.maxHp, chr.localMaxHP = 50, 50
    chr.ad, chr.AS, chr.df, chr.speed, = 5, 0, 0, 0

    # 유물로 인한 스탯 상승
    for r in chr.relic:
        if r.name == '금강저':
            chr.ad += 1
        elif r.name == '매끄러운 돌':
            chr.df += 1
        elif r.name == '현자의 돌':
            chr.ad += 2
            chr.df -= 1
        elif r.name == '붉은 해골' and chr.hp <= chr.localMaxHP / 2:
            chr.ad += 3
        elif r.name == '수리검' and r.stack // 3 >= 1:
            chr.df += r.stack // 3
        elif r.name == '표창' and r.stack // 3 >= 1:
            chr.ad += r.stack // 3

    # 공격속도 적용
    chr.MOTION_DELAY['attack1'] = int(chr.MOTION_DELAY_ORIGIN['attack1'] * (100 - chr.AS) / 100)
    chr.MOTION_DELAY['attack2'] = int(chr.MOTION_DELAY_ORIGIN['attack2'] * (100 - chr.AS) / 100)
    chr.MOTION_DELAY['attack3'] = int(chr.MOTION_DELAY_ORIGIN['attack3'] * (100 - chr.AS) / 100)
    chr.MOTION_DELAY['air_attack2'] = int(chr.MOTION_DELAY_ORIGIN['air_attack2'] * (100 - chr.AS) / 100)

def updataRelicStack():
    for r in Ingame_state.chr.relic:
        if r.stack >= r.condition:
            r.isActive = True
        else:
            r.isActive = False

def loadRelicData():
    global relic_data
    with open('../res/Item/relic_info.json', 'r') as f:
        data = json.load(f)
    for i in data:
        id = i['ID']
        relic_data[str(id)] = dict(i)