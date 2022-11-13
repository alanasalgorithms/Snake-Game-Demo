#Alana Burrell, Gabriela Ortega, and Lauren Waller
#SCIS 346
#Prof. Lawrence
#6 Novemeber 2022
#Group Project Demo Program
#Language: Python

print("🐍Game Rules🐍\n+1 Point: 🍖\n+1 Point: 🍒\n+1 Point: 💘\n+5 Points: 💰\n-3 Points: ⚡\nESC: End Game\nHitting the Border: Lose Game\n\n\nTo begin, press ENTER")

def get_high_score():
    # Default high score
    high_score = 0
 
    # Try to read the high score from a file
    try:
        high_score_file = open("high_score.txt", "r")
        high_score = int(high_score_file.read())
        high_score_file.close()
        print("High Score =", high_score)
    except IOError:
        # Error reading file, no high score
        print("There is no high score yet.")
    except ValueError:
        # There's a file there, but we don't understand the number.
        print("There is no previous high score.")
 
    return high_score
 
 
def save_high_score(new_high_score):
    try:
        # Write the file to disk
        high_score_file = open("high_score.txt", "w")
        high_score_file.write(str(new_high_score))
        high_score_file.close()
    except IOError:
        # Hm, can't write it.
        print("Unable to save the high score.")


      



#Imports - using curses allows us to take input from the keyboard as controls inside of our game
#Using randint from random will allow for use to later use randomized integers 
import curses 
from random import randint

#constants
#Border - these lengths decide how big our game board will be. Right now it is 20 x 60.
WINDOW_WIDTH = 60  # number of columns of window box 
WINDOW_HEIGHT = 20 # number of rows of window box 
'''
Number of blocks in window per line = WINDOW_WIDTH -2. 
Block x index ranges from 1 to WINDOW_WIDTH -2.
Number of blocks in window per column = WINDOW_HEIGHT -2. 
Block y index ranges from 1 to WINDOW_HEIGHT -2.
'''


# Setting up the window for the game to be played in
curses.initscr()
win = curses.newwin(WINDOW_HEIGHT, WINDOW_WIDTH, 0, 0) # rows, columns
# rows or y, columns or x (this is the opposite of a regular x,y coordinate plane)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
#Here, we don't wait for the next user input, the loop continues whether the players makes input or not keeping the snake in motion
win.nodelay(1) # -1

#To initialize the position for our snake and our snake's food using a tuple because tuples are immutable
snake = [(4, 4), (4, 3), (4, 2)]
food = (11, 10)
cherry = (10, 35)
heart = (12,45)
money = (1,55)
lightning = (12, 40)
lightning1 = (10, 5)
lightning2 = (5, 26)

win.addch(food[0], food[1], "🍖")
win.addch(cherry[0], cherry[1], "🍒")
win.addch(heart[0], heart[1], "💘")
win.addch(money[0], money[1], "💰")
win.addch(lightning[0], lightning[1], "⚡")
win.addch(lightning1[0], lightning1[1], "⚡")
win.addch(lightning2[0], lightning2[1], "⚡")


# game logic
#initialize the game score to be 0
score = 0
ESC = 27
ENTER = 10
key = curses.KEY_RIGHT

while key != ESC:
    win.addstr(0, 2, 'Score ' + str(score) + ' ')
    win.timeout(150 - (len(snake)) // 5 + len(snake)//10 % 120) 
#increases the snake's speed
    prev_key = key
    event = win.getch()
    key = event if event != -1 else prev_key

#checks for the input from the user. If the user doesn't use one of these keys, we continue to pass the previous key for the snake's movement
    if key not in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN, ESC]:
        key = prev_key

# Once the snake eats the food, we need to recalculate the next coordinates of the food item
# intial coordinates for our snake's head
    y = snake[0][0]
    x = snake[0][1]
#Here we decide what happens when different keystrokes are passed from the user. This changes the coordinates of the snake head on the gameboard.
#Changes directions in the vertical direction
    if key == curses.KEY_DOWN:
        y += 1
    if key == curses.KEY_UP:
        y -= 1
#Changes directions in the horizontal direction
    if key == curses.KEY_LEFT:
        x -= 1
    if key == curses.KEY_RIGHT:
        x += 1

    snake.insert(0, (y, x)) # append O(n)
# This checks if the snake has hit the border in any direction. If so, the program will break and the game will end.
    if y == 0: 
      break
    if y == WINDOW_HEIGHT-1: 
      break
    if x == 0: 
      break
    if x == WINDOW_WIDTH -1: 
      break
#We also need to check when the snake hits the food. If the snake gets into the same coordinate as the food. We need to relocate the food AND increase the score by one.  
#while food equals our empty tuple we need to reassign the coordinate of food to produce a new food.
#this gives our food new coordinates that doesn't hit the wall and gives the snake a fair chance since it's at least 2 spaces away from the wall.
    if snake[0] == food:
        # eat the food
        score += 1
        food = ()
          #this prevents the new food from generating inside of the snake/ snake's coordinates.
        while food == ():
            food = (randint(2,WINDOW_HEIGHT-3), randint(2,WINDOW_WIDTH-3))
            if food in snake:
                food = ()
        win.addch(food[0], food[1], "🍖")


                  
                  
    if snake[0] == cherry:
        score += 1
        cherry = ()
          #this prevents the new food from generating inside of the snake/ snake's coordinates.
        while cherry == ():
            cherry = (randint(1,WINDOW_HEIGHT-2), randint(1,WINDOW_WIDTH-2))
            if cherry in snake:
                cherry = ()
        win.addch(cherry[0], cherry[1], "🍒")


                  
    if snake[0] == heart:
        score += 1
        heart = ()
          #this prevents the new food from generating inside of the snake/ snake's coordinates.
        while heart == ():
            heart = (randint(1,WINDOW_HEIGHT-3), randint(1,WINDOW_WIDTH-3))
            if heart in snake:
                heart = ()
        win.addch(heart[0], heart[1], "💘")      


    if snake[0] == money:
        score += 5
        money = ()
          #this prevents the new food from generating inside of the snake/ snake's coordinates.
        while money == ():
            money = (randint(1,WINDOW_HEIGHT-3), randint(1,WINDOW_WIDTH-3))
            if money in snake:
                money = ()
        win.addch(money[0], money[1], "💰")  


    if snake[0] == lightning:
        score -= 3
        lightning = ()
          #this prevents the new food from generating inside of the snake/ snake's coordinates.
        while lightning == ():
            lightning = (randint(1,WINDOW_HEIGHT-3), randint(1,WINDOW_WIDTH-3))
            if lightning in snake:
                lightning = ()
        win.addch(lightning[0], lightning[1], "⚡")

                  
    if snake[0] == lightning1:
        score -= 3
        lightning1 = ()
          #this prevents the new food from generating inside of the snake/ snake's coordinates.
        while lightning1 == ():
            lightning1 = (randint(1,WINDOW_HEIGHT-3), randint(1,WINDOW_WIDTH-3))
            if lightning1 in snake:
                lightning1 = ()
        win.addch(lightning1[0], lightning1[1], "⚡")
                  
    if snake[0] == lightning2:
        score -= 3
        lightning2 = ()
          #this prevents the new food from generating inside of the snake/ snake's coordinates.
        while lightning2 == ():
            lightning2 = (randint(1,WINDOW_HEIGHT-3), randint(1,WINDOW_WIDTH-3))
            if lightning2 in snake:
                lightning2 = ()
        win.addch(lightning2[0], lightning2[1], "⚡")
                  
                  
    else:
      #move snake
        last = snake.pop()
        win.addch(last[0], last[1], ' ')
#this gives the new precision of our snake
    win.addch(snake[0][0], snake[0][1], '*')

curses.endwin()
print(f"Your score = {score}")
def main():
    """ Main program is here. """
    # Get the high score
    high_score = get_high_score()
 
    # Get the score from the current game
    current_score = score
    try:
        # Ask the user for his/her score
        current_score = score
    except ValueError:
        # Error, can't turn what they typed into a number
        print("I don't understand what you typed.")
 
    # See if we have a new high score
    if current_score > high_score:
        # We do! Save to disk
        print("You set a NEW RECORD! \n\n\n\n\nYou dropped this, Queen 🏆")
        save_high_score(current_score)
    elif current_score == high_score:
        print("You almost beat the high score! Play again 🐍")
    else:
        print("Better luck next time 🐍")
 
# Call the main function, start up the game
if __name__ == "__main__":
    main()