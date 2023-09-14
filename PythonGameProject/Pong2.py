# Pong game for beginners
import turtle
import winsound
from random import uniform, choice
import time


def write():
    pen.write("Player A: {} Player B: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))
    info.write("Clear the score - spacebar | Pause for 10s - p", align="center", font=("Courier", 14, "normal"))


def random_starting_ball_speed():
    ball.goto(0, 0)
    if choice([True, False]):
        ball.dx = uniform(0.10, 0.20)
    else:
        ball.dx = uniform(-0.15, -0.10)
    if choice([True, False]):
        ball.dy = uniform(0.10, 0.15)
    else:
        ball.dy = uniform(-0.15, -0.10)


wn = turtle.Screen()
wn.title("Pong by @IwoSzczepaniak")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

# Score
score_a = 0
score_b = 0

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

# BALL
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
random_starting_ball_speed()


# Clearing info
info = turtle.Turtle()
info.speed(0)
info.color("white")
info.penup()
info.hideturtle()
info.goto(0, 220)

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
write()


# move
def paddle_a_up():
    y = paddle_a.ycor()
    if y <= 225: y += 25
    paddle_a.sety(y)

def paddle_a_down():
    y = paddle_a.ycor()
    if y >= -225: y -= 25
    paddle_a.sety(y)

def paddle_b_up():
    y = paddle_b.ycor()
    if y <= 225: y += 25
    paddle_b.sety(y)

def paddle_b_down():
    y = paddle_b.ycor()
    if y >= -225: y -= 25
    paddle_b.sety(y)

def zero_the_score():
    global score_a
    global score_b
    score_a = 0
    score_b = 0
    pen.clear()
    write()


def ball_colliding_with_paddle():
    ball.dx *= -1.1
    ball.dy *= 1.1
    info.clear()
    # winsound.PlaySound('bounce.wav', winsound.SND_ASYNC)

def pause():
    time.sleep(10)


# Keybord binding
wn.listen()
wn.onkeypress(paddle_a_up, "w")
wn.onkeypress(paddle_a_down, "s")
wn.onkeypress(paddle_b_up, "Up")
wn.onkeypress(paddle_b_down, "Down")
wn.onkeypress(zero_the_score, "space")
wn.onkeypress(pause, "p")



# Main game loop
while True:
    wn.update()

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)
    # Borders
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1
    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1


    # Losing point
    if ball.xcor() > 390 or ball.xcor() < -390:
        winsound.Beep(1200, 100)
        if ball.xcor() > 390: score_a += 1
        else: score_b += 1
        random_starting_ball_speed()
        pen.clear()
        write()


    # Paddle and ball collisions
    if 350 > ball.xcor() > 340 and paddle_b.ycor() + 40 > ball.ycor() > paddle_b.ycor() - 40:
        ball.setx(340)
        ball_colliding_with_paddle()
    if -350 < ball.xcor() < -340 and paddle_a.ycor() + 40 > ball.ycor() > paddle_a.ycor() - 40:
        ball.setx(-340)
        ball_colliding_with_paddle()

