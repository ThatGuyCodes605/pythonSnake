import tkinter
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * ROWS
WINDOW_HEIGHT = TILE_SIZE * COLS

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg = "black", width = WINDOW_WIDTH, height = WINDOW_HEIGHT, borderwidth=1, highlightthickness=1)
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
velocityX = 0
velocityY = 0
game_over = False
score = 0

def change_direction(e):
    #print(e.keysym)
    global velocityX, velocityY, game_over
    if (game_over):
        return


    if (e.keysym == "Up" and velocityY != 1):
        velocityX = 0
        velocityY = -1
    elif (e.keysym == "Down"and velocityY != -1):
         velocityX = 0
         velocityY = 1
    elif (e.keysym == "Left"and velocityX != 1):
         velocityX = -1
         velocityY = 0
    elif (e.keysym == "Right"and velocityX != -1):
         velocityX = 1
         velocityY = 0

def move():
    global snake, snake_body, food, game_over, score
    if game_over:
        return
    
    # Check wall collision
    if snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT:
        game_over = True
        return
    
    # Check self collision
    for tile in snake_body:
        if snake.x == tile.x and snake.y == tile.y:
            game_over = True
            return

    # Move body (from tail to head)
    for i in range(len(snake_body) - 1, 0, -1):
        snake_body[i].x = snake_body[i-1].x
        snake_body[i].y = snake_body[i-1].y
    if snake_body:
        snake_body[0].x = snake.x
        snake_body[0].y = snake.y

    # Eat food
    if snake.x == food.x and snake.y == food.y:
        # Add new segment at tail position
        if snake_body:
            last = snake_body[-1]
            snake_body.append(Tile(last.x, last.y))
        else:
            snake_body.append(Tile(snake.x, snake.y))
        
        # Move food to new random location
        food.x = random.randint(0, COLS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE
        score += 1

    # Move head
    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE




def draw():
    global snake, food, snake_body, game_over, score
    move()

    canvas.delete("all")

    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill = "red")    
    
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill = "lime green")

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill="lime green")

    if (game_over):
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font = "Arial 20", text = f"Game Over: {score}", fill = "white")
    else:
        canvas.create_text(30, 20, font = "Arial 10", text = f"Score: {score}", fill= "white" )



    window.after(100, draw)

draw()

def restart_game(e=None):
    global snake, snake_body, velocityX, velocityY, game_over, score, food
    snake.x, snake.y = 5 * TILE_SIZE, 5 * TILE_SIZE
    snake_body.clear()
    velocityX = 0
    velocityY = 0
    game_over = False
    score = 0
    food.x = random.randint(0, COLS - 1) * TILE_SIZE
    food.y = random.randint(0, ROWS - 1) * TILE_SIZE


window.bind("<r>", restart_game) 
window.bind("<R>", restart_game)  

window.bind("<KeyPress>", change_direction)
window.mainloop()