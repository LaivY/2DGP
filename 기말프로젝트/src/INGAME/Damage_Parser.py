import UI
from INGAME import Relic
from random import randint
import FRAMEWORK.DataManager

def chr_attack_mob(mob, chr):
    _dmg = chr.ad

    for r in chr.relic:
        # 펜 촉
        if r.id == 104:
            if r.isActive:
                r.stack, r.isActive = 0, False
                _dmg *= 2
            else:
                r.stack += 1
        # 수리검
        elif r.id == 205:
            r.stack += 1

    # 치명타
    if chr.cri >= randint(0, 99):
        for r in chr.relic:
            # 음양성
            if r.id == 207:
                r.stack = 0
                r.isActive = False
        _dmg *= 2
        UI.addString([mob.x, mob.y], str(max(_dmg - mob.df, 0)), (255, 100, 100), 0.6, 0.1, 24)
    # 일반
    else:
        for r in chr.relic:
            # 음양성
            if r.id == 207:
                r.stack += 5
        UI.addString([mob.x, mob.y], str(max(_dmg - mob.df, 0)), (255, 255, 255), 0.6, 0.1)

    mob.dx = 0
    mob.hitBy = chr.state
    mob.hp -= max(_dmg - mob.df, 0)

    if mob.x < chr.x:
        mob.dir = 'RIGHT'
    else:
        mob.dir = 'LEFT'

    if mob.state != 'attack':
        mob.state = 'hit'
        mob.frame = 0

    if mob.hp <= 0:
        mob.state = 'die'
        mob.order = 'none'
        mob.frame = 0

        for r in chr.relic:
            # 피가 담긴 병
            if r.id == 105:
                chr_hp_recovery(chr, 2)
            # 고기 덩어리
            elif r.id == 200 and r.isActive:
                chr_hp_recovery(chr, 12)

    FRAMEWORK.DataManager.load('../res/Sound/SOTE_SFX_FastAtk_v2.wav').play()
    Relic.updataRelicStack()
    Relic.updateChrStat()

def mob_attack_chr(mob, chr):
    _dmg = mob.ad - chr.df

    for r in chr.relic:
        # 청동 비늘
        if r.id == 103:
            chr_attack_mob(mob, chr, 3)
        # 표창
        elif r.id == 206:
            r.stack += 1
        # 토리이
        elif r.id == 305 and 1 <= _dmg <= 5:
            _dmg = 1
        # 조개 화석
        elif r.id == 304 and r.isActive and _dmg >= 1:
            r.stack, _dmg = 0, 0
        # 향로
        elif r.id == 306:
            if r.isActive and _dmg >= 1:
                r.stack, _dmg = 0, 0
            else:
                r.stack += 1

    if chr.state == 'idle' or chr.state == 'run':
        chr.state = 'hit'
        chr.frame = 0

        if mob.x < chr.x:
            chr.dx = 0.1
            chr.dir = 'LEFT'
        else:
            chr.dx = -0.1
            chr.dir = 'RIGHT'

    chr.invincible_time = 1
    chr.hp -= max(_dmg, 0)
    UI.addString([chr.x, chr.y], str(max(_dmg, 0)), (255, 50, 50), 0.5, 0.1, 12)

    for r in chr.relic:
        # 도마뱀 꼬리
        if r.id == 300 and r.isActive and chr.hp <= 0:
            chr_hp_recovery(chr, chr.maxHP // 2)
            r.stack = 0
            break

    if chr.hp <= 0:
        chr.state = 'die'
        chr.dx = 0

    FRAMEWORK.DataManager.load('../res/Sound/SOTE_SFX_FastAtk_v2.wav').play()
    Relic.updataRelicStack()
    Relic.updateChrStat()

def chr_hp_recovery(chr, amount):
    _amount = amount
    
    # 유물 :: 마법 꽃
    for r in chr.relic:
        if r.id == 301:
            _amount *= 1.5

    chr.hp += round(_amount)
    chr.hp = min(chr.hp, chr.maxHP)
    UI.addString([chr.x, chr.y], str(round(_amount)), (50, 255, 50), 0.5, 0.1, 12)

    FRAMEWORK.DataManager.load('../res/Sound/SOTE_SFX_HealShort_1_v2.wav').play()
    Relic.updataRelicStack()
    Relic.updateChrStat()
