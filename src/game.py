import turtle as t
import random
import os
from pathlib import Path

WIDTH, HEIGHT = 800, 600
STAR_COUNT = 10
SPEED = 15
METEOR_SPEED = 6
LIVES = 3
HIGH_SCORE_FILE = "high_score.txt"
FRAME_DELAY_MS = 10        # time between game-loop ticks
HIT_PAUSE_MS = 1000        # short pause after losing a life

# Game states. A single flag decides what SPACE does and whether the loop runs,
# so pressing SPACE mid-game can no longer start a second, nested game loop.
STATE_START = "start"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"

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
shield_active = False

score_display = t.Turtle()
score_display.hideturtle()
score_display.color("white")
score_display.penup()
score_display.goto(-WIDTH//2 + 20, HEIGHT//2 - 40)

def update_score_display():
    shield_status = "Shield: ON" if shield_active else "Shield: OFF"
    score_display.clear()
    score_display.write(f"Score: {score} | High Score: {high_score} | Lives: {'❤️' * lives} | {shield_status}", 
                       font=("Arial", 16, "bold"))

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

# Shield Power-up
shield = t.Turtle()
shield.shape("circle")
shield.color("blue")
shield.penup()
shield.hideturtle()
shield.goto(0, HEIGHT + 100) # Start off-screen

# On-screen message (start screen / game over). One reusable turtle, so the
# text can be cleared when a new game begins.
message = t.Turtle()
message.hideturtle()
message.color("white")
message.penup()

def show_message(text, size):
    message.clear()
    message.write(text, align="center", font=("Arial", size, "bold"))

def clear_message():
    message.clear()

# Controls
def go_left():
    if game_state != STATE_PLAYING:
        return
    x = player.xcor() - SPEED
    if x < -WIDTH//2 + 20: x = -WIDTH//2 + 20
    player.setx(x)

def go_right():
    if game_state != STATE_PLAYING:
        return
    x = player.xcor() + SPEED
    if x > WIDTH//2 - 20: x = WIDTH//2 - 20
    player.setx(x)

def start_game():
    global game_state, score, lives, shield_active
    if game_state == STATE_PLAYING:
        return  # ignore SPACE while a game is already running
    game_state = STATE_PLAYING
    clear_message()
    score = 0
    lives = LIVES
    shield_active = False
    player.goto(0, -HEIGHT//2 + 50)
    meteor.goto(random.randint(-WIDTH//2+40, WIDTH//2-40), HEIGHT//2 - 80)
    shield.hideturtle()
    shield.goto(0, HEIGHT + 100)
    update_score_display()
    screen.update()
    screen.ontimer(game_tick, FRAME_DELAY_MS)

screen.listen()
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")
screen.onkey(start_game, "space")

def collision(a, b, dist=25):
    return a.distance(b) < dist

def show_start_screen():
    show_message("Press SPACE to Start!", 24)
    screen.update()

def show_game_over():
    global high_score, game_state
    game_state = STATE_GAME_OVER
    if score > high_score:
        high_score = score
        save_high_score(high_score)
        update_score_display()
    
    show_message(f"Game Over!\nFinal Score: {score}\nPress SPACE to Play Again", 20)
    screen.update()

def game_tick():
    """Advance the game by one frame, then schedule the next frame.
    
    Uses screen.ontimer instead of a blocking while-loop, so key presses are
    handled between frames and never re-enter the loop.
    """
    global score, lives, shield_active
        
    if game_state != STATE_PLAYING:
        return

    next_delay = FRAME_DELAY_MS

    # Increase difficulty with score
    current_meteor_speed = METEOR_SPEED + (score // 10)

    # Move meteor
    meteor.sety(meteor.ycor() - current_meteor_speed)
    if meteor.ycor() < -HEIGHT//2:
        meteor.goto(random.randint(-WIDTH//2+40, WIDTH//2-40), HEIGHT//2 - 80)

    # Shield power-up logic
    if score > 0 and score % 2 == 0 and not shield.isvisible() and not shield_active:
        shield.goto(random.randint(-WIDTH//2+20, WIDTH//2-20), 
                    random.randint(-HEIGHT//2+20, HEIGHT//2-60))
        shield.showturtle()

    # Collect shield
    if shield.isvisible() and collision(player, shield, 20):
        shield_active = True
        shield.hideturtle()
        shield.goto(0, HEIGHT + 100)
        update_score_display()

    # Collect stars
    for s in stars:
        if collision(player, s, 20):
            s.goto(random.randint(-WIDTH//2+20, WIDTH//2-20), 
                  random.randint(-HEIGHT//2+20, HEIGHT//2-60))
            score += 1
            update_score_display()

    # Check meteor collision
    if collision(player, meteor, 30):
        if shield_active:
            shield_active = False
            meteor.goto(random.randint(-WIDTH//2+40, WIDTH//2-40), HEIGHT//2 - 80)
            update_score_display()
        else:
            lives -= 1
            update_score_display()
            if lives > 0:
                meteor.goto(random.randint(-WIDTH//2+40, WIDTH//2-40), HEIGHT//2 - 80)
                player.goto(0, -HEIGHT//2 + 50)
                next_delay = HIT_PAUSE_MS
            else:
                show_game_over()
                return

    screen.update()
    screen.ontimer(game_tick, next_delay)


# Start with the start screen
game_state = STATE_START
show_start_screen()
t.done()
