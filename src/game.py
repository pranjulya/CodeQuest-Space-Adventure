import turtle as t
import random
import time

WIDTH, HEIGHT = 800, 600
STAR_COUNT = 10
SPEED = 15
METEOR_SPEED = 6

screen = t.Screen()
screen.setup(WIDTH, HEIGHT)
screen.title("CodeQuest: Space Adventure")
screen.bgcolor("black")
screen.tracer(0)

# Optional: register shapes if you have gifs
# screen.register_shape("sprites/ship.gif")
# screen.register_shape("sprites/meteor.gif")
# screen.register_shape("sprites/star.gif")

# Player
player = t.Turtle()
player.shape("triangle") # or "sprites/ship.gif"
player.color("cyan")
player.penup()
player.setheading(90)
player.goto(0, -HEIGHT//2 + 50)

# Score
score = 0
score_t = t.Turtle()
score_t.hideturtle()
score_t.color("white")
score_t.penup()
score_t.goto(-WIDTH//2 + 20, HEIGHT//2 - 40)

def update_score():
    score_t.clear()
    score_t.write(f"Score: {score}", font=("Arial", 18, "bold"))

# Stars
stars = []
for _ in range(STAR_COUNT):
    s = t.Turtle()
    s.shape("circle") # or "sprites/star.gif"
    s.color("yellow")
    s.shapesize(0.6, 0.6)
    s.penup()
    s.goto(random.randint(-WIDTH//2+20, WIDTH//2-20), random.randint(-HEIGHT//2+20, HEIGHT//2-60))
    stars.append(s)

# Meteor
meteor = t.Turtle()
meteor.shape("square") # or "sprites/meteor.gif"
meteor.color("orange")
meteor.shapesize(1.2, 1.2)
meteor.penup()
meteor.goto(random.randint(-WIDTH//2+40, WIDTH//2-40), HEIGHT//2 - 80)
meteor.setheading(270)

def go_left():
    x = player.xcor() - SPEED
    if x < -WIDTH//2 + 20: x = -WIDTH//2 + 20
    player.setx(x)

def go_right():
    x = player.xcor() + SPEED
    if x > WIDTH//2 - 20: x = WIDTH//2 - 20
    player.setx(x)

screen.listen()
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")

def collision(a, b, dist=25):
    return a.distance(b) < dist

game_over = False
update_score()

while not game_over:
    # meteor falls
    meteor.sety(meteor.ycor() - METEOR_SPEED)
    if meteor.ycor() < -HEIGHT//2:
        meteor.goto(random.randint(-WIDTH//2+40, WIDTH//2-40), HEIGHT//2 - 80)

    # collect stars
    for s in stars:
        if collision(player, s, 20):
            s.goto(random.randint(-WIDTH//2+20, WIDTH//2-20), random.randint(-HEIGHT//2+20, HEIGHT//2-60))
            score += 1
            update_score()

    # hit meteor?
    if collision(player, meteor, 30):
        game_over = True

    screen.update()
    time.sleep(0.01)

# Game over message
end = t.Turtle()
end.hideturtle()
end.color("white")
end.write("Game Over! Thanks for playing 🚀", align="center", font=("Arial", 20, "bold"))
t.done()
