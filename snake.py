import tkinter
import random

ROWS = 23
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS

window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

canvas = tkinter.Canvas(window, bg="black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
canvas.pack()
window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

snake = Tile(5*TILE_SIZE, 5*TILE_SIZE)
food = Tile(10*TILE_SIZE, 10*TILE_SIZE)
snake_body = []
velocity_x = 0
velocity_y = 0
game_over = False
score = 0

def start_game():
    global snake, snake_body, food, velocity_x, velocity_y, game_over, score
    snake = Tile(5*TILE_SIZE, 5*TILE_SIZE)
    food = Tile(10*TILE_SIZE, 10*TILE_SIZE)
    snake_body = []
    velocity_x = 0
    velocity_y = 0
    game_over = False
    score = 0
    draw()

def change_direction(e):
    global velocity_x, velocity_y, game_over

    if game_over:
        return

    if e.keysym == "Up" and velocity_y != 1:
        velocity_x = 0
        velocity_y = -1
    elif e.keysym == "Down" and velocity_y != -1:
        velocity_x = 0
        velocity_y = 1
    elif e.keysym == "Left" and velocity_x != 1:
        velocity_x = -1
        velocity_y = 0
    elif e.keysym == "Right" and velocity_x != -1:
        velocity_x = 1
        velocity_y = 0

def move():
    global snake, snake_body, food, game_over, score
    if game_over:
        return
    if snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT:
        game_over = True
        return

    for tile in snake_body:
        if snake.x == tile.x and snake.y == tile.y:
            game_over = True
            return

    if snake.x == food.x and snake.y == food.y:
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLS-1) * TILE_SIZE
        food.y = random.randint(0, ROWS-1) * TILE_SIZE
        score += 1

    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if i == 0:
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y

    snake.x += velocity_x * TILE_SIZE
    snake.y += velocity_y * TILE_SIZE

def draw():
    global snake, food, snake_body, game_over, score
    move()

    canvas.delete("all")

    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill="red", outline="yellow", width=2)
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill="green", outline="white", width=2)

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill="green", outline="white", width=2)

    if game_over:
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font="Arial 20 bold", text=f"Game Over: {score}", fill="white")
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 40, font="Arial 15", text="Press 'R' to Restart", fill="white")
    else:
        canvas.create_text(60, 20, font="Arial 15", text=f"Score: {score}", fill="white")

    window.after(100, draw)

def restart_game(e):
    if game_over and e.keysym == "r":
        start_game()

start_game()

window.bind("<KeyRelease>", change_direction)
window.bind("<KeyPress-r>", restart_game)
window.mainloop()
