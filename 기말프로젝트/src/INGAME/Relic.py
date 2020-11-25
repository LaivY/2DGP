from INGAME import  Ingame_state, Damage_Parser
import UI
from random import randint

RELIC_INFO = {}

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
    if len(inven) >= 25:
        UI.addString([chr.x, chr.y + 5], '더 이상 획득할 유물이 없습니다.', (255, 255, 255), 1, 0.1)
        return

    # 중복없이 랜덤으로 한 개 획득
    while True:
        Pass = True
        rarity = randint(0, 99)

        if 0 <= rarity < 50:
            _id = randint(100, 108)
        elif 50 <= rarity <= 75:
            _id = randint(200, 208)
        else:
            _id = randint(300, 306)

        for i in inven:
            if i.id == _id:
                Pass = False
                break
        if Pass:
            # 유물 데이터 설정
            r = relic(_id)
            r.name = RELIC_INFO[str(_id)]['NAME']
            r.desc = RELIC_INFO[str(_id)]['DESC']
            r.flavorText = RELIC_INFO[str(_id)]['FLAVOR_TEXT']
            
            # 룬 12면체, 붉은 해골
            if r.id == 101 or r.id == 204:
                r.stack = 0
                r.condition = 1
            # 펜 촉
            elif r.id == 104:
                r.stack = 0
                r.condition = 5
            # 리의 와플, 배, 망고
            elif r.id == 201 or r.id == 203 or r.id == 302:
                r.stack = 1
            # 마트료시카, 도마뱀 꼬리, 조개 화석
            elif r.id == 202 or r.id == 300 or r.id == 304:
                r.stack = 1
                r.condition = 1
            # 수리검, 표창
            elif r.id == 205 or r.id == 206:
                r.stack = 0
                r.condition = 3
            # 음양성
            elif r.id == 207:
                r.stack = 0
                r.condition = 5
            # 향로
            elif r.id == 306:
                r.stack = 0
                r.condition = 6
            
            inven.append(r)
            UI.addString([chr.x, chr.y + 5], str(RELIC_INFO[str(_id)]['NAME']) + '을(를) 획득했습니다!', (255, 255, 255), 1, 0.1, 12)
            break

    # 마트료시카
    for r in chr.relic:
        if r.id == 202 and r.isActive:
            r.stack, r.isActive = 0, False
            addRandomRelic()

    updateChrStat()
    updataRelicStack()

def updateChrStat():
    chr = Ingame_state.chr

    # 계산 전에 캐릭터 스탯 초기화
    chr.maxHp, chr.maxHP = 50, 50
    chr.ad, chr.AS, chr.df, chr.cri, = 5, 0, 0, 5

    # 유물로 인한 스탯 상승
    for r in chr.relic:
        # 금강저
        if r.id == 100:
            chr.ad += 1
        # 룬 12면체
        elif r.id == 101 and r.isActive:
            chr.ad += 2
        # 매끄러운 돌
        elif r.id == 102:
            chr.df += 1
        # 현자의 돌
        elif r.id == 106:
            chr.ad += 2
            chr.df -= 1
        # 닌자 두루마리
        elif r.id == 107:
            chr.AS += 15
        # 도박 칩
        elif r.id == 108:
            chr.cri += 15
        # 리의 와플
        elif r.id == 201:
            chr.maxHP += 12
            if r.stack == 1:
                r.stack = 0
                Damage_Parser.chr_hp_recovery(chr, chr.maxHP)
        # 배
        elif r.id == 203:
            chr.maxHP += 10
            if r.stack == 1:
                r.stack = 0
                Damage_Parser.chr_hp_recovery(chr, 10)
        # 붉은 해골
        elif r.id == 204 and r.isActive:
            chr.ad += 3
        # 수리검
        elif r.id == 205 and r.isActive:
            chr.df += r.stack // 3
        # 표창
        elif r.id == 206 and r.isActive:
            chr.ad += r.stack // 3
        # 음양성
        elif r.id == 207 and r.isActive:
            chr.cri += r.stack
        # 작은 집
        elif r.id == 208:
            chr.ad += 1
            chr.AS += 10
            chr.cri += 10
            chr.df += 1
        # 망고
        elif r.id == 302:
            chr.maxHP += 14
            if r.stack == 1:
                r.stack = 0
                Damage_Parser.chr_hp_recovery(chr, 14)

    # 공격속도 적용
    chr.MOTION_DELAY['attack1'] = int(chr.MOTION_DELAY_ORIGIN['attack1'] * (100 - chr.AS) / 100)
    chr.MOTION_DELAY['attack2'] = int(chr.MOTION_DELAY_ORIGIN['attack2'] * (100 - chr.AS) / 100)
    chr.MOTION_DELAY['attack3'] = int(chr.MOTION_DELAY_ORIGIN['attack3'] * (100 - chr.AS) / 100)
    chr.MOTION_DELAY['air_attack2'] = int(chr.MOTION_DELAY_ORIGIN['air_attack2'] * (100 - chr.AS) / 100)

def updataRelicStack():
    chr = Ingame_state.chr

    for r in chr.relic:
        # 룬 12면체
        if r.id == 101:
            if chr.hp == chr.maxHP:
                r.isActive = True
                r.stack = 1
            else:
                r.isActive = False
                r.stack = 0

        # 고기 덩어리, 붉은 해골
        elif r.id == 200 or r.id == 204:
            if chr.hp <= chr.maxHP / 2:
                r.isActive = True
                r.stack = 1
            else:
                r.isActive = False
                r.stack = 0

        # 나머지
        elif r.stack >= r.condition:
            r.isActive = True
        else:
            r.isActive = False
