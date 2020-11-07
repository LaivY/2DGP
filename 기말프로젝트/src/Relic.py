import Ingame_state
from random import randint

class relic:
    image = None
    def __init__(self, _id):
        self.id = _id
        self.stack = -1
        self.condition = -1
        self.isActive = False

def addRandomRelic():
    inven = Ingame_state.chr.relic
    rList = Ingame_state.chr.relicIdList
    # 모든 유물을 갖고있을 경우
    if len(inven) >= 10:
        return

    # 중복없이 랜덤으로 한 개 획득
    while True:
        Pass = True
        _id = randint(100, 109)
        for i in rList:
            if i == _id:
                Pass = False
                break
        if Pass:
            r = relic(_id)
            if _id == 105:
                r.stack = 0
                r.condition = 5
            elif _id == 108:
                r.stack = 1
                r.condition = 1
                r.isActive = True
            elif _id == 109:
                r.stack = 0
                r.condition = 6
            inven.append(r)
            rList.append(_id)
            break

    updateChrStat()

def updateChrStat():
    chr = Ingame_state.chr

    # 계산 전에 캐릭터 스탯 초기화
    chr.maxHp, chr.localMaxHP = 50, 50
    chr.ad, chr.AS, chr.df, chr.speed, = 5, 0, 0, 0

    # 유물로 인한 스탯 상승
    for r in chr.relicIdList:
        if r == 100: # 불타는 혈액
            chr.localMaxHP += 10
        elif r == 101: # 금강저
            chr.ad += 1
        elif r == 102: # 매끄러운 돌
            chr.df += 1

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