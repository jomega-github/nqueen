# nqueen
The N-Queen problem.

<h1>Background</h1>

This repository is my investigation into a specific algorithm for solving the N-Queen problem.

This was also my first Python coding project. The repo has a complete history of my development of the project from when I started with no knowledge of Python, and using a simple text editor, until later when I was using IntelliJ.
You can follow that history through the comments on the commits.

<h1>The Algorithm</h1>

See the file theory.txt for the original information on the algorithm I'm investigating.

<h2>Version 2.4 Performance</h2>

My version 2.4 on the 8-Queens problem finding all solutions searches 2,056 total nodes to find the 92 solutions. I count as a *node* every time the program places a Queen on the board.

The Wikipedia page on the Eight_queens_puzzle, says that a backtracking depth-first search constructs the search tree by considering one row (column in my program) at a time, eliminating most nonsolution boards at a very early stage in their construction. Rejecting early even on incomplete boards, it says that only 15,720 possible Queen placements are examined. It says a further improvement, which examines only 5,508 possible Queen placements is to combine the permutation method with the early pruning method. The permutations are generated depth-first, and the search space is pruned if the partial permutation produces a diagonal attack. By permutation method it means "One algorithm solves the eight rooks puzzle by generating the permutations of the numbers 1 through 8 (of which there are 8! = 40,320), and uses the elements of each permutation as indices to place a Queen on each row. Then it rejects those boards with diagonal attacking positions."

My version 2.4 does not place a Queen in a column unless it is not attacked by the previously placed Queens in prior columns. Hence, it does not have to remove such a Queen. Furthermore, it figures out all the admissible rows in the current column at once and saves it for use in backtracking.

Looked at as a tree search problem, the tree searched by my program has the depth level corresponding to the column numbers. At depth 0 there is the single root node, which is an empty board. There are eight children of root corresponding to the eight choices for the row to put the Queen in column 1. However, the first child does not have eight children because for the next column, which is column 2, the row choices are 3 to 8. Hence, the algorithm I'm using is depth-first with forward pruning. A child is only visited if it was admissible. A child in the tree may have no children at all.  That's because it might be a solution, or the next column has no admissable placements. My program, which searches only 2,056 nodes, is more efficient than the one described on this part of the Wikipedia page, which it says would try 5,508. Perhaps this is all a matter of definition of what "pruning" means!
