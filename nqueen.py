#!/usr/bin/python

"""The N-Queens problem. Version 1.2"""

import argparse
import sys

# Constants
# The maximum number of columns on the chessboard.
_MAX_COLUMNS = 20;
# The maximum number of rows on the chessboard.
_MAX_ROWS = 20;
# FYI: There are 39,029,188,884 solutions for 20x20 !

# Globals
# Do we show progress?
show_progress = False
# Do we only show the solution counts?
show_count_only = False
# Do we display node counts?
show_node_count = False
# Do we display total node counts?
show_total_node_count = False

# Actual number of columns on the chessboard.
number_of_columns = 8
# Actual number of rows on the chessboard.
number_of_rows = 8
# The row location of the Queen in a particular column.
# 0 if there is no Queen in that column.
# This 'array' is indexed starting at 1!
# It is actually a list in Python.
queen_location = [0] * (_MAX_COLUMNS+1)
# The next row location to try putting the Queen.
try_row = 1
# The next column to try placing a Queen.
queen_column = 1
# Count the number of nodes visited for one solution.
node_count = 0
# Count the total number of nodes visited.
total_node_count = 0
# A count used to make neat output for the progress functions.
progress_count = 0
# Count the number of solutions when asking for all of them.
solution_count = 0
# Find all solutions?
find_all_solutions = False

def show_advancing():
    """Show that we are advancing in finding a solution"""
    global progress_count

    if (show_progress):
        print("+{}".format(queen_column), end='')
        # This next is to get neat output.
        progress_count += 1
        if (progress_count > 25):
            print()
            progress_count = 0

def show_retreating():
    """Show that we are backtracking"""
    global progress_count

    if (show_progress):
        print("-{}".format(queen_column), end='')
        # This next is to get neat output.
        progress_count += 1
        if (progress_count > 25):
            print()
            progress_count = 0

def show_found_solution():
    """show that we have found a solution"""
    global node_count
    global solution_count

    if (show_progress):
        print("!")
    if (show_node_count):
        print("Searched {}".format(node_count), "nodes.")
    solution_count += 1
    node_count = 0

def show_no_solution():
    """Show that we did not find a solution"""
    if (show_progress):
        print("@")
    if (show_node_count):
        print("Searched {}".format(node_count), "nodes.")

def show_no_more_solutions():
    """Show that we did not find more solutions"""
    global node_count

    if (show_progress):
        print("#")
    if (show_node_count):
        print("Searched {}".format(node_count), "nodes.")
    node_count = 0

def print_solution():
    """print a solution"""
    if (show_count_only):
        return

    for row in range(1, number_of_rows+1):
        for column in range(1, number_of_columns+1):
            if (queen_location[column] == row):
                print("Q", end='')
            else:
                print("-", end='')
        print()
    print("---------------------")

def queen_attacks_square(sx, sy, queen_x, queen_y):
    """Return True if the square (sx, sy) is attacked by the Queen on
       square (queen_x, queen_y). Otherwise return False.
       We consider the square the Queen is on to be attacked.

    """
    if (sx == queen_x):
        return True

    if (sy == queen_y):
        return True;

    if ((sy - queen_y) == (sx - queen_x)):
        return True;

    if ((sy - queen_y) == (queen_x - sx)):
        return True;
	
    return False;

def under_attack(sx, sy):
    """Return True if the square (sx, sy) is under attack by the Queens
       already placed in queen_location. Otherwise return False.

    """
    for column in range(1, number_of_columns+1):
        if (queen_location[column] != 0):
            # We have a Queen placed in this column.
            if (queen_attacks_square(sx, sy, queen_location[column], column)):
                # The Queen is attacking (sx, sy).
                return True
    # No Queen is attacking (sx, sy).
    return False

def retreat():
    """Prepare to try the next location for the previously placed Queen.
       If we cannot retreat, then return False. Otherwise we
       return True and queen_column is the new column to try; starting
       at row try_row.

    """
    global queen_location
    global try_row
    global queen_column

    # We have to go back to the previous column.
    queen_column -= 1
    show_retreating()
    if (queen_column <= 0):
        # Cannot retreat.
        return False
    else:
        # Try the row after the one we tried last.
        try_row = queen_location[queen_column] + 1
        # Remove the Queen from the board.
        queen_location[queen_column] = 0
        return True

def retreat_wrapper(success_flag):
    """A wrapper to handle the different behavior need because of
       adding the ability to find all solutions.
       If success_flag is True then we've found some solution already;
       otherwise we have not.
       The return value is True if the search for solutions should continue
       and False otherwise.
       If we cannot retreat, then return False. Otherwise we
       return True and queen_column is the new column to try; starting
       at row try_row.

    """

    more_to_search = True;
    if (retreat() == False):
        more_to_search = False
        if (find_all_solutions):
            if (success_flag):
                # We already found a solution.
                show_no_more_solutions()
            else:
                # No solution.
                show_no_solution()
        else:
            # No solution.
            show_no_solution()
    else:
        pass
    return more_to_search

def advance():
    """Place the current Queen on the board and prepare to
       try the next column. Return False if all the Queens are
       placed. Otherwise return True.

    """
    global queen_location
    global try_row
    global queen_column
    global node_count
    global total_node_count

    show_advancing()
    queen_location[queen_column] = try_row
    try_row = 1
    queen_column += 1
    node_count += 1
    total_node_count += 1
    if (queen_column > number_of_columns):
        return False
    else:
        return True

def admissible():
    """Return True if (try_row, queen_column) is an admissible location
       for the current Queen. Otherwise return False.

    """

    if (under_attack(try_row, queen_column)):
        return False
    else:
        return True

def seek_another_segment():
    """Return True if we can find a place to put the current Queen.
       In that case (try_row, queen_column) is the place to put her.
       Otherwise return False.

    """
    global try_row

    seek_flag = False
    while ((try_row <= number_of_rows) and (seek_flag == False)):
        if (admissible()):
            seek_flag = True
        else:
            try_row += 1
    return seek_flag

def search():
    """search for a solution and return True if found else False"""
    global queen_location
    global queen_column
    global try_row
    global node_count

    # Return value.
    # True if we find a solution; False otherwise.
    success_flag = False;

    # First queen is not placed yet.
    queen_column = 1
    # Start at row 1.
    try_row = 1;

    more_to_search = True;
    while (more_to_search):
        if (seek_another_segment()):
            # We found a place to put the Queen. (try_row, queen_column).
            # Store the info and see if we have a solution.
            # Note: After calling advance() we have
            #       queen_location[queen_column] = try_row
            #       try_row = 1
            #       queen_column += 1
            if (advance() == False):
                # We found a solution. NB: queen_column = number_of_columns+1
                show_found_solution()
                print_solution()
                success_flag = True
                if (find_all_solutions):
                    # A way to break into the debugger.
                    # import pdb; pdb.set_trace()
                    more_to_search = retreat_wrapper(success_flag)
                else:
                    more_to_search = False
            else:
                # queen_column <= number_of_columns
                pass
        else:
            # We could not place the current Queen.
            # Try to back out the last Queen assigment and prepare
            # to try the next possibility.
            # Note: After calling retreat_wrapper() we have
            #       queen_column -= 1
            #       As long as queen_column > 0 we have
            #       try_row = queen_location[queen_column] + 1
            #       queen_location[queen_column] = 0
            more_to_search = retreat_wrapper(success_flag)
    return success_flag

def check_num(s):
    """check that a string is an integer"""
    try:
        int(s)
        return True
    except:
        return False

def sanity_check_args(start, number_of_problems):
    """sanity check the users arguments"""

    if (check_num(start)):
        start = int(start)
    else:
        print('error: {}'.format(start), ' is not a number.')
        sys.exit(1)

    if (check_num(number_of_problems)):
        number_of_problems = int(number_of_problems)
    else:
        print('error: {}'.format(number_of_problems), ' is not a number.')
        sys.exit(1)

    if (start <= 0):
        print('error: starting value must be greater than 0')
        sys.exit(1)

    if (number_of_problems < 1):
        print('error: number of problem sizes must be greater than 0')
        sys.exit(1)

    if (((start + number_of_problems) - 1) > _MAX_COLUMNS):
        print('error: Sorry. Limit is {} columns'.format(_MAX_COLUMNS))
        sys.exit(1)

def initialize(size):
    global queen_location
    global try_row
    global queen_column
    global number_of_columns
    global number_of_rows
    global node_count
    global total_node_count
    global progress_count
    global solution_count
    
    # Zero the Queen locations.
    for column in range(1, _MAX_COLUMNS+1):
        queen_location[column] = 0
	
    # The next row location to try putting the Queen.
    try_row = 1
    # The next column to try placing a Queen.
    queen_column = 1
    # Set the size of the chessboard.
    number_of_columns = size
    number_of_rows = size
	
    # Set our counters and such.
    node_count = 0
    total_node_count = 0
    progress_count = 0
    solution_count = 0

def run(args):
    """run the program with args already parsed."""
    global find_all_solutions
    global show_progress
    global show_count_only
    global show_node_count
    global show_total_node_count

    sanity_check_args(args.start, args.number_of_problems)
    start = int(args.start)
    number_of_problems = int(args.number_of_problems)
    if (args.all):
        find_all_solutions = True
    if (args.show_progress):
        show_progress = True
    if (args.show_count_only):
        show_count_only = True
    if (args.show_node_count):
        show_node_count = True
    if (args.show_total_node_count):
        show_total_node_count = True
    if (args.show_count_only):
        show_count_only = True
        show_node_count = False
        show_total_node_count = False

    for size in range(start, start+number_of_problems):
        initialize(size)
        if (find_all_solutions):
            print("Looking for all solutions to the {}".format(size),
                  "Queens problem.")
        else:
            print("Looking for a solution to the {}".format(size),
                  "Queens problem.")
        if (search()):
            # Got at least one solution.
            if (find_all_solutions):
                print("All solutions found.")
            else:
                pass
        else:
            # No solution.
            print("No solution!")

        if (find_all_solutions):
            print("Total solutions found {}".format(solution_count))
        if (show_total_node_count):
            print("Searched {}".format(total_node_count), "total nodes.")
        print("----------------------------------------")

def main():
    """main code with command line parser"""
    parser = argparse.ArgumentParser(description="Solve N-queen problems")
    parser.add_argument('start', type=int,
                        help='miniumn board starting size')
    parser.add_argument('number_of_problems', type=int,
                        help='number of problems sizes to do')
    parser.add_argument('--all', action='store_true',
                        help="print all solutions")
    parser.add_argument('--show_progress', action='store_true',
                        help="show progess")
    parser.add_argument('--show_node_count', action='store_true',
                        help="show node counts")
    parser.add_argument('--show_total_node_count', action='store_true',
                        help="show total node counts")
    parser.add_argument('--show_count_only', action='store_true',
                        help="show solution counts only")
    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
