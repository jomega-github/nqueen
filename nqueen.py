#!/usr/bin/python

"""The N-Queens problem. Version 1.0"""

import argparse
import sys

# Constants
# Do we show progress?
_SHOW_PROGRESS = True
# The maximum number of columns on the chessboard.
_MAX_COLUMNS = 20;
# The maximum number of rows on the chessboard.
_MAX_ROWS = 20;

# Globals
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

# Count the number of nodes visited.
node_count = 0

# A count used to make neat output for the progress functions.
progress_count = 0

def show_advancing():
    """Show that we are advancing in finding a solution"""
    global progress_count

    if (_SHOW_PROGRESS):
        print("+{}".format(queen_column), end='')
        # This next is to get neat output.
        progress_count += 1
        if (progress_count > 25):
            print()
            progress_count = 0

def show_retreating():
    """Show that we are backtracking"""
    global progress_count

    if (_SHOW_PROGRESS):
        print("-{}".format(queen_column), end='')
        # This next is to get neat output.
        progress_count += 1
        if (progress_count > 25):
            print()
            progress_count = 0

def show_found_solution():
    """show that we have found a solution"""
    if (_SHOW_PROGRESS):
        print("!")

def show_no_solution():
    """Show that we did not find a solution"""
    if (_SHOW_PROGRESS):
        print("@")

def print_solution():
    """print a solution"""
    for row in range(1, number_of_rows+1):
        for column in range(1, number_of_columns+1):
            if (queen_location[column] == row):
                print("Q", end='')
            else:
                print("-", end='')
        print()

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

def advance():
    """Place the current Queen on the board and prepare to
       try the next column. Return False if all the Queens are
       placed. Otherwise return True.

    """
    global queen_location
    global try_row
    global queen_column
    global node_count

    show_advancing()
    queen_location[queen_column] = try_row
    try_row = 1
    queen_column += 1
    node_count += 1
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
    global queen_column
    global try_row

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
            # Store the info and see if we are done.
            if (advance() == False):
                # We found a solution.
                show_found_solution()
                success_flag = True
                more_to_search = False
            else:
                pass
        else:
            # We could not place the current Queen.
            # Try to back out the last Queen assigment and prepare
            # to try the next possibility.
            if (retreat() == False):
                # No solution.
                show_no_solution()
                success_flag = False
                more_to_search = False
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
        print('error: {}'.fromat(number_of_problems), ' is not a number.')
        sys.exit(1)

    if (start <= 0):
        print('error: starting value must be greater than 0')
        sys.exit(1)

    if (number_of_problems <= 1):
        print('error: number of problem sizes must be greater than 1')
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
    global progress_count
    
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
    progress_count = 0

def run(args):
    """run the program with args already parsed."""

    sanity_check_args(args.start, args.number_of_problems)
    start = int(args.start)
    number_of_problems = int(args.number_of_problems)
    #print("start =", start)
    #print("number_of_problems =", number_of_problems)

    for size in range(start, start+number_of_problems):
        initialize(size)
        print("Looking for a solution to the {}".format(size),
              "Queen problem.")
        if (search()):
            # Got a solution.
            print_solution()
        else:
            # No solution.
            print("No solution!")

        print("Searched {}".format(node_count), "nodes.")
        print("----------------------------------------")

def main():
    """main code with command line parser"""
    parser = argparse.ArgumentParser(description="Solve N-queen problems")
    parser.add_argument('start',
                        help='miniumn board starting size')
    parser.add_argument('number_of_problems',
                        help='number of problems sizes to do')
    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
