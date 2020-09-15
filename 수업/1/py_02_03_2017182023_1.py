import turtle

def moveto(x,y):
    turtle.penup()
    turtle.goto(x,y)
    turtle.pendown()

def drawNieun(x,y):
    moveto(x, y)
    turtle.setheading(270)
    turtle.forward(25)
    turtle.left(90)
    turtle.forward(50)

turtle.speed(0)

# ㅇ
moveto(-200,50)
turtle.circle(20)

# ㅜ
moveto(-230,40)
turtle.forward(60)
moveto(-200,40)
turtle.right(90)
turtle.forward(30)

# ㅓ
moveto(-160, 80)
turtle.forward(70)
moveto(-160, 30)
turtle.right(90)
turtle.forward(30)

# ㄴ
drawNieun(-215,20)

# ㅇ
moveto(0,50)
turtle.circle(20)

# ㅠ
moveto(-30,40)
turtle.forward(60)
moveto(-7, 40)
turtle.right(90)
turtle.forward(30)
moveto(7, 40)
turtle.forward(30)

# ㄴ
drawNieun(-22,20)

# ㅅ
moveto(180,80)
turtle.right(60)
turtle.forward(45)
moveto(180,80)
turtle.right(60)
turtle.forward(45)
turtle.left(30)

# ㅣ
moveto(215,90)
turtle.forward(60)

# ㄱ
moveto(215,20)
turtle.forward(30)
moveto(215,20)
turtle.right(90)
turtle.forward(50)

turtle.hideturtle()
turtle.exitonclick()