# Sudoku-Game-With-Solver
This is my version of a fully-fledged Sudoku game with an inbuilt Sudoku solver AI. 

If you want to run my code, feel free to tweak around.

Requirements to run the code:
Python
Pygame

The rules of the game are simple.
Fill the board with numbers from 1 to 9 such that
i. No two numbers in any row are same
ii. No two numbers in any column are same
iii. No two numbers in any 3x3 grid shown using the dark lines.

Note: I haven't added support for the numpad keys. You can add it easily if you want to.

How to play:

Click on any block on the grid and enter the value you want (from 1 - 9, both inclusive).
Click 0 to clear a block.
Click Enter key after completing the puzzle to check if your solution is correct.
Click spacebar if you want our AI to solve the Sudoku for you using the backtracking algorithm.

Additional Tip: In line 206 and 219, reduce the value inside pygame.time.delay('this value') to make the solving faster and increase those values to make it solve slower 
if you want to observe it while working.

Optimal value: 2 ms for the line 206, and comment out line 219 for a good balance between speed and visuals.
