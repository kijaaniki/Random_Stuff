import curses
import random

# Initialize the curses screen
screen = curses.initscr()
# No echoing of keys
curses.noecho()
# React to keys instantly, without waiting for Enter key
curses.cbreak()
# Enable keypad mode
screen.keypad(True)

# Define the snake game parameters
sh, sw = screen.getmaxyx()
w = curses.newwin(sh, sw, 0, 0)
w.keypad(True)
w.timeout(100)

# Initial position of the snake
snk_x = sw//4
snk_y = sh//2
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x-1],
    [snk_y, snk_x-2]
]

# Food for the snake
food = [sh//2, sw//2]
w.addch(food[0], food[1], curses.ACS_PI)

# Initial direction
key = curses.KEY_RIGHT

# Main loop
while True:
    next_key = w.getch()
    key = key if next_key == -1 else next_key

    # Calculate new head position
    if key == curses.KEY_DOWN:
        new_head = [snake[0][0] + 1, snake[0][1]]
    if key == curses.KEY_UP:
        new_head = [snake[0][0] - 1, snake[0][1]]
    if key == curses.KEY_LEFT:
        new_head = [snake[0][0], snake[0][1] - 1]
    if key == curses.KEY_RIGHT:
        new_head = [snake[0][0], snake[0][1] + 1]

    # Insert new head
    snake.insert(0, new_head)

    # Check if snake hits the border or itself
    if (snake[0][0] in [0, sh] or
        snake[0][1] in [0, sw] or
        snake[0] in snake[1:]):
        curses.endwin()
        quit()

    # Check if snake eats the food
    if snake[0] == food:
        food = None
        while food is None:
            nf = [
                random.randint(1, sh-1),
                random.randint(1, sw-1)
            ]
            food = nf if nf not in snake else None
        w.addch(food[0], food[1], curses.ACS_PI)
    else:
        # Remove last part of snake (tail)
        tail = snake.pop()
        w.addch(tail[0], tail[1], ' ')

    # Add new head of snake
    w.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)

curses.endwin()
