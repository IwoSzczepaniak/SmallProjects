# Pong game for beginners
def paddle_b_up():
    y = paddle_b.ycor()
    if y <= 225: y += 25
    paddle_b.sety(y)

def paddle_b_down():
    y = paddle_b.ycor()
    if y >= -225: y -= 25
    paddle_b.sety(y)