import turtle as t
import random
import time
import os
from pathlib import Path

WIDTH, HEIGHT = 800, 600
STAR_COUNT = 10
SPEED = 15
METEOR_SPEED = 6
LIVES = 3
HIGH_SCORE_FILE = "high_score.txt"

def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, 'r') as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, 'w') as f:
        f.write(str(score))

# Screen setup
screen = t.Screen()
screen.setup(WIDTH, HEIGHT)
screen.title("CodeQuest: Space Adventure")
screen.bgcolor("black")
screen.tracer(0)

# Register shapes
screen.register_shape("src/sprites/ship.gif")
screen.register_shape("src/sprites/meteor.gif")
screen.register_shape("src/sprites/star.gif")

# Player
player = t.Turtle()
player.shape("src/sprites/ship.gif")
player.penup()
player.setheading(90)
player.goto(0, -HEIGHT//2 + 50)

# Score and Lives
score = 0
high_score = load_high_score()
lives = LIVES

score_display = t.Turtle()
score_display.hideturtle()
score_display.color("white")
score_display.penup()
score_display.goto(-WIDTH//2 + 20, HEIGHT//2 - 40)

def update_score_display():
    score_display.clear()
    score_display.write(f"Score: {score} | High Score: {high_score} | Lives: {'❤️' * lives}", 
                       font=("Arial", 18, "bold"))

# Stars
stars = []
for _ in range(STAR_COUNT):
    s = t.Turtle()
    s.shape("src/sprites/star.gif")
    s.penup()
    s.goto(random.randint(-WIDTH//2+20, WIDTH//2-20), 
           random.randint(-HEIGHT//2+20, HEIGHT//2-60))
    stars.append(s)

# Meteor
meteor = t.Turtle()
meteor.shape("src/sprites/meteor.gif")
meteor.penup()
meteor.goto(random.randint(-WIDTH//2+40, WIDTH//2-40), HEIGHT//2 - 80)
meteor.setheading(270)

# Controls
def go_left():
    x = player.xcor() - SPEED
    if x < -WIDTH//2 + 20: x = -WIDTH//2 + 20
    player.setx(x)

def go_right():
    x = player.xcor() + SPEED
    if x > WIDTH//2 - 20: x = WIDTH//2 - 20
    player.setx(x)

def start_game():
    global game_active, score, lives
    game_active = True
    score = 0
    lives = LIVES
    player.goto(0, -HEIGHT//2 + 50)
    meteor.goto(random.randint(-WIDTH//2+40, WIDTH//2-40), HEIGHT//2 - 80)
    update_score_display()
    main_game_loop()

screen.listen()
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")
screen.onkey(start_game, "space")

def collision(a, b, dist=25):
    return a.distance(b) < dist

def show_start_screen():
    start_text = t.Turtle()
    start_text.hideturtle()
    start_text.color("white")
    start_text.penup()
    start_text.write("Press SPACE to Start!", align="center", 
                    font=("Arial", 24, "bold"))

def show_game_over():
    global high_score
    if score > high_score:
        high_score = score
        save_high_score(high_score)
    
    end = t.Turtle()
    end.hideturtle()
    end.color("white")
    end.penup()
    end.write(f"Game Over!\nFinal Score: {score}\nPress SPACE to Play Again", 
              align="center", font=("Arial", 20, "bold"))

def main_game_loop():
    global game_active, score, lives
    
    while game_active and lives > 0:
        # Increase difficulty with score
        current_meteor_speed = METEOR_SPEED + (score // 10)
        
        # Move meteor
        meteor.sety(meteor.ycor() - current_meteor_speed)
        if meteor.ycor() < -HEIGHT//2:
            meteor.goto(random.randint(-WIDTH//2+40, WIDTH//2-40), HEIGHT//2 - 80)

        # Collect stars
        for s in stars:
            if collision(player, s, 20):
                s.goto(random.randint(-WIDTH//2+20, WIDTH//2-20), 
                      random.randint(-HEIGHT//2+20, HEIGHT//2-60))
                score += 1
                update_score_display()

        # Check meteor collision
        if collision(player, meteor, 30):
            lives -= 1
            update_score_display()
            if lives > 0:
                meteor.goto(random.randint(-WIDTH//2+40, WIDTH//2-40), HEIGHT//2 - 80)
                player.goto(0, -HEIGHT//2 + 50)
                time.sleep(1)
            else:
                game_active = False
                show_game_over()

        screen.update()
        time.sleep(0.01)

# Start with the start screen
game_active = False
show_start_screen()
t.done()
