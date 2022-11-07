#Alana Burrell, Gabriela Ortega, and Lauren Waller
#SCIS 346
#Prof. Lawrence
#6 Novemeber 2022
#Group Project Demo Program
#Language: Python

#Imports - using curses allows us to take input from the keyboard as controls inside of our game
#Using randint from random will allow for use to later use randomized integers
import curses
from random import randint

#Border - these lengths decide how big our game board will be. Right now it is 20 x 60.
WINDOW_WIDTH = 60  # number of columns of window box
WINDOW_HEIGHT = 20  # number of rows of window box

# Setting up the window for the game to be played in
curses.initscr()
window = curses.newwin(
  WINDOW_HEIGHT, WINDOW_WIDTH, 0, 0
)  # rows or y, columns or x (this is the opposite of a regular x,y coordinate plane)
window.keypad(1)
curses.noecho()
curses.curs_set(0)
window.border(0)

#Here, we don't wait for the next user input, the loop continues whether the players makes input or not
window.nodelay(1)  # -1

#To initialize the position for our snake and our snake's food using a tuple because tuples are immutable
snake = [(4, 4), (4, 3), (4, 2)]
food = (6, 6)
# cherry = (7, 7)
# heart = (8, 8)
# treasure = (9,9)
# lighting = (4,4)

window.addch(food[0], food[1], "🍖")
# window.addch(cherry[0], cherry[1], "🍒")
# window.addch(heart[0], heart[1], "❤️")
#can use meat, cherry, heart, lightning, coin,
# 🍖 🍒 ❤️ can serve as regular food
# 💰 can be used to add 5 points
# ⚡ can deduct a point

#Initilize the game scoreboard to be 0
score = 0
#Initilize
ESC = 27
key = curses.KEY_RIGHT

#Game Logic / Mechanics
while key != ESC:
  window.addstr(0, 2, 'Score ' + str(score) + " ")
  window.timeout(150 - (len(snake)) // 5 +
                 len(snake) // 10 % 120)  # increase speed

  prev_key = key
  event = window.getch()
  key = event if event != -1 else prev_key

  #checks for the input from the user. If the user doesn't use one of these keys, we continue to pass the previous key for the snake's movement
  if key not in [
      curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN, ESC
  ]:
    key = prev_key

# Once the snake eats the food, we need to recalculate the next coordinates of the food item

# intial coordinates for our snake's head
  y = snake[0][0]
  x = snake[0][1]

  #Here we decide what happens when different keystrokes are passed from the user. This changes the coordinates of the snake head on the gameboard.
  #changes directions in the vertical direction
  if key == curses.KEY_DOWN:
    y += 1  #positive is up
  if key == curses.KEY_UP:
    y -= 1
  #changes directions in the horizontal direction
  if key == curses.KEY_LEFT:
    x -= 1  #negative is left
  if key == curses.KEY_RIGHT:
    x += 1
  snake.insert(0, (y, x))  # append  has an O(n) time but is fine

  # This checks if the snake has hit the border in any direction. If so, the program will break and the game will end.
  if y == 0: break
  if y == WINDOW_HEIGHT - 1: break
  if x == 0: break
  if x == WINDOW_WIDTH - 1: break

  # We also need to check if the snake runs over itself. If so, the game breaks.
  if snake[0] in snake[1:]:
    break
#We also need to check when the snake hits the food. If the snake gets into the same coordinate as the food. We need to relocate the food AND increase the score by one.
  if snake[0] == food:
    score += 1
    #while food equals our empty tuple we need to reassign the coordinate of food to produce a new food.
    food = ()
    while food == ():
      #this gives our food new coordinates that doesn't hit the wall and gives the snake a fair chance since it's at least 2 spaces away from the wall.
      food = (randint(1, WINDOW_HEIGHT - 2), randint(1, WINDOW_WIDTH - 2))

      #this prevents the new food from generating inside of the snake/ snake's coordinates.
      if food in snake:
        food = ()
    window.addch(food[0], food[1], "🍖")
  else:
    # removes the last coordinate on the tail of the snake
    last = snake.pop()
    window.addch(last[0], last[1], " ")
#this gives the new precision of our snake
  window.addch(snake[0][0], snake[0][1], '*')

#Outside of the Loop
curses.endwin()
#prints out the final score that a player has earned during game play
print(f"Final score = {score}")
