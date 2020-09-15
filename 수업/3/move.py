from pico2d import *

open_canvas()
CHR = load_image('../rsrc/character.png')
GRA = load_image('../rsrc/grass.png')

for x in range(0, 800, 2):
    clear_canvas()
    GRA.draw(400, 30)
    CHR.draw(x, 85)
    update_canvas()
    get_events()
    delay(0.01)
    
delay(1)
close_canvas()