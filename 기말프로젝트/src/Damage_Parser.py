import UI
import Relic

def chr_attack_mob(mob, chr, dmg):
    _dmg = dmg

    # 유물 :: 펜 촉
    for r in chr.relic:
        if r.id == 105:
            if r.isActive:
                r.stack, r.isActive = 0, False
                _dmg *= 2
            else:
                r.stack += 1

    mob.dx = 0
    mob.hitBy = chr.state
    mob.hp -= max(_dmg - mob.df, 0)
    UI.addString([mob.x, mob.y], str(max(_dmg - mob.df, 0)), (255, 255, 255), 0.6, 0.1)

    if mob.state != 'attack':
        mob.state = 'hit'
        mob.frame = 0

    if mob.hp <= 0:
        mob.state = 'die'
        mob.order = 'none'
        mob.frame = 0

        # 유물 :: 피가 담긴 병
        for r in chr.relic:
            if r.id == 104:
                chr_hp_recovery(chr, 2)

    Relic.updataRelicStack()

def mob_attack_chr(mob, chr):
    _dmg = mob.ad - chr.df

    # 유물 :: 조개화석, 향로
    for r in chr.relic:
        if r.id == 108 and r.isActive:
            r.stack, _dmg = 0, 0
            break
        elif r.id == 109:
            if r.isActive:
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
    UI.addString([chr.x, chr.y], str(max(_dmg, 0)), (255, 50, 50), 0.5, 0.1)

    # 유물 :: 청동 비늘
    for r in chr.relic:
        if r.id == 103:
            chr_attack_mob(mob, chr, 3)

    if chr.hp <= 0:
        chr.state = 'die'
        chr.dx = 0

    Relic.updataRelicStack()

def chr_hp_recovery(chr, amount):
    _amount = amount
    
    # 유물 :: 마법 꽃
    if 106 in chr.relicIdList:
        _amount *= 1.5
    chr.hp += round(_amount)
    UI.addString([chr.x, chr.y], str(round(_amount)), (50, 255, 50), 0.5, 0.1)