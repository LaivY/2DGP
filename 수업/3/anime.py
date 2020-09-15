from pico2d import *

open_canvas()
g = load_image('../rsrc/grass.png')
c = load_image('../rsrc/run_animation.png')

frame = 0
for x in range(0, 800, 2):
    clear_canvas()
    g.draw(400, 30)
    c.clip_draw(frame * 100, 0, 100, 100, x, 85)
    update_canvas()

    frame = (frame + 1) % 8
    get_events()
    delay(0.01)