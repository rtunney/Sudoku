This repo contains an algorithm to solve a sudoku puzzle.

========================
THE SUDOKU MATRIX
========================
Sudoku matrices are formed by the sudoku_matrix() constructor.

Each sudoku_matrix contains a .matrix attribute that is structured as follows:
•The matrix is a list 
•Each matrix contains nine row lists 
•Each row contains nine box lists
•Each box is a list of values 1-9

The solver eliminates values from a box until only one remains, 
at which point the box is solved. 

========================
ELIMINATION OPERATIONS
========================
The solver implements three basic operations to eliminate values from boxes:
•get_singletons() finds boxes in a row with only one value. 
	clear_singletons() removes these values from all other boxes in the row.
•get_and_clear_uniques finds values that exist in only one box in a row, 
	and then eliminates all other values from that box.
•get_matches finds n boxes in a row containing exactly the same n values.
	clear_matches then removes those values from all other boxes in the row.

========================
TRANSPOSE METHODS
========================
The solver implements two transpose methods. 
The purpose of these methods is to allow the solver to use the row operations
listed above to eliminate values in columns, as well as inthe nine 3x3 grids 
referred to as 'submatrices' in the code. 

•transpose() is an ordinary matrix transpose. Each column is repositioned as 
	the row with the matching index. 
•submatrix_transpose is an unusual 'transpose' that converts each 3x3 submatrix
	into a row. 

Each transpose is its own inverse function (i.e. it is undone by calling the 
transpose again).

========================
SOLVING THE PUZZLE
========================
The solve() method is implemented as follows:

The step() method calls each of the three elimination operations on the rows, 
then columns, then submatrices. 
The hundred_steps() method calls step() 100 times. 

solve() first calls hundred_steps().
This is usually sufficient to solve 'easy' and 'medium' sudoku puzzles.

solve() then enters a loop that copies the sudoku matrix
----If the matrix is unsolved, solve finds an unsolved boxes and randomly clears
----all of its remaining values instead of one. Then hundred_steps is called.

----This random selection/solve attempt is repeated until all boxes have no more
----than one value. 

----If the 'solved' matrix is invalid, the loop is repeated until a valid matrix 
----is found.

========================
PERFORMANCE
========================
The algorithm solves most commercially available sudokus in a second or less.
It solves the "world's hardest sudokus" in a few minutes. 

========================
AREAS FOR IMPROVEMENT
========================
•The solve() function does not remember its own random guesses from failed trials.
•Add more advanced elimination operations to each step.

suggestions? email rtunney3@gmail.com
	





