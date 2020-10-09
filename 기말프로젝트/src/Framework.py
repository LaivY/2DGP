import time
from pico2d import *

GameState = []
delta_time = 0
running = True
def run(state):
    global GameState, running, delta_time
    GameState = [state]
    last_time = time.time()

    open_canvas()
    state.enter()
    while running:
        clear_canvas()

        # Calculate delta_time
        now = time.time()
        delta_time = now - last_time
        last_time = now

        # Event Handling
        evts = get_events()
        for e in evts: GameState[-1].eventHandler(e)

        # Update
        GameState[-1].update()

        # Rendering
        GameState[-1].draw()

        update_canvas()
        delay(0.01)

    close_canvas()

def quit():
    global running
    running = False

def changeState(new_state):
    global GameState
    if(len(GameState) > 0):
        GameState.pop().exit
    GameState.append(new_state)
    new_state.enter()

def push(new_state):
    global GameState
    size = len(GameState)
    if size == 1: quit()
    elif size > 1:
        GameState[-1].exit()
        GameState.pop()
        GameState[-1].resume()
