from pico2d import *
import gfw
import player

def collides_distance(player, missile):
    px, py = player.pos
    mx, my = missile.pos

    # 플레이어와 미사일 사이의 거리의 제곱
    dis = (px - mx) ** 2 + (py - my) ** 2

    # 플레이어와 미사일의 반지름의 합의 제곱
    sum_of_radius = (player.radius + missile.radius) ** 2
    return dis < sum_of_radius

def check_collision():
    dead, full = False, False
    for m in gfw.world.objects_at(gfw.layer.missile):
        if collides_distance(player, m):
            gfw.world.remove(m)
            dead = player.decrease_life()

    for i in gfw.world.objects_at(gfw.layer.item):
        if collides_distance(player, i):
            gfw.world.remove(i)
            full = player.increase_life()

    return dead, full
