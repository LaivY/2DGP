import turtle

def moveto(pos):
    turtle.penup()
    turtle.goto(pos[0], pos[1])
    turtle.pendown()

def drawRect():
    for i in range(4):
        turtle.forward(100)
        turtle.left(90)

turtle.speed(0)
for i in range(5):
    for j in range(5):
        pos = i * 100, j * 100
        moveto(pos)
        drawRect()
moveto((0,0))
turtle.exitonclick()