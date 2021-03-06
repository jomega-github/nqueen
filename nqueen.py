#!/usr/bin/python

"""The N-Queens problem. Version 2.5"""

import argparse
import sys
import time
# import random

# Constants
# The maximum number of columns on the chessboard.
_MAX_COLUMNS = 20
# The maximum number of rows on the chessboard.
_MAX_ROWS = 20
# FYI: There are 39,029,188,884 solutions for 20x20 !

# Globals
# NB: Everything is initialized in initialize(), so these
#     are sometimes just set to empty values and defaults.

# Do we show progress?
show_progress = False
# Do we print the board solutions?
no_print = False
# Do we display node counts?
show_node_count = False
# Do we display total node counts?
show_total_node_count = False
# Actual number of columns on the chessboard.
number_of_columns = 8
# Actual number of rows on the chessboard.
number_of_rows = 8
# The row location of the Queen in a particular column.
# -1 if there is no Queen in that column.
# This 'array' is indexed starting at 0!
# It is actually a list in Python.
# Will be queen_location = [-1] * number_of_columns
queen_location = []
# The saved search list of admissible rows for a column.
# Will be admissible_rows = [[] for _ in range(number_of_columns)]
# NB: admissible_rows = [] * (number_of_columns) does NOT work; it gives [].
admissible_rows = []
# The next row location to try putting the Queen.
try_row = 0
# The next column to try placing a Queen.
queen_column = 0
# Count the number of nodes visited for one solution.
# We count as a "node" every time we place a Queen on the board.
node_count = 0
# Count the total number of nodes visited.
total_node_count = 0
# A count used to make neat output for the progress functions.
progress_count = 0
# Count the number of solutions when asking for all of them.
solution_count = 0
# Find all solutions?
find_all_solutions = False

# Optimization helper matrices
# These look upside down because in chess the rows are numbered from
# the White side up, while in Python (and Math matrices) the numbering
# of rows is top down!
# slash_code assigns to each square on the board a diagonal number.
# These are positive slope diagonals. "/" oriented; hence the name.
# The values are indices into the "*_lookup" arrays below.
# Will be...
# slash_code = [[0 for _ in range(0, number_of_columns)]
#                for _ in range(0, number_of_rows)]
# backslash_code assigns to each square on the board a diagonal number.
# These are negative slope diagonals. (anti-diagonals in chess programming)
# "\" oriented; hence the name.
# backslash_code = [[0 for _ in range(0, number_of_columns)]
#                    for _ in range(0, number_of_rows)]
slash_code = []
backslash_code = []
# row_lookup records if a row is occupied by some Queen.
# Will be...
# row_lookup = [False] * (number_of_rows)
# slash_code_lookup records if a positive diagonal is occupied by some Queen.
# slash_code_lookup = [False] * (number_of_columns + number_of_rows - 1)
# backslash_code_lookup records if a negative diagonal is occupied.
# backslash_code_lookup = [False] * (number_of_columns + number_of_rows - 1)
row_lookup = []
slash_code_lookup = []
backslash_code_lookup = []
# row_indices caches the entire list of row numbers for efficiency.
# Will be row_indices = list(range(0,number_of_rows))
row_indices = []


def show_advancing():
    """Show that we are advancing in finding a solution"""
    global progress_count

    if show_progress:
        print("+{}".format(queen_column), end='')
        # This next is to get neat output.
        progress_count += 1
        if progress_count > 25:
            print()
            progress_count = 0


def show_retreating():
    """Show that we are backtracking"""
    global progress_count

    if show_progress:
        print("-{}".format(queen_column), end='')
        # This next is to get neat output.
        progress_count += 1
        if progress_count > 25:
            print()
            progress_count = 0


def show_found_solution():
    """Show that we have found a solution"""

    if show_progress:
        print("!")
    if show_node_count:
        print("Searched {}".format(node_count), "nodes.")


def show_no_solution():
    """Show that we did not find a solution"""

    if show_progress:
        print("@")
    if show_node_count:
        print("Searched {}".format(node_count), "nodes.")


def show_no_more_solutions():
    """Show that we did not find more solutions"""

    if show_progress:
        print("#")
    if show_node_count:
        print("Searched {}".format(node_count), "nodes.")


def print_solution():
    """Print a solution"""

    if no_print:
        return

    for row in range(0, number_of_rows):
        for column in range(0, number_of_columns):
            if queen_location[column] == row:
                print("Q", end='')
            else:
                print("-", end='')
        print()
    print("---------------------")


def retreat(success_flag):
    """retreat() backs up the search tree looking for a "previous column"
       with rows that have not been tried. This previous column might be
       the last column on the board if a solution was just found!

       If retreat() ever finds that it cannot back up any further then it
       notifies of either no solution, or no more solutions if one had
       already been found so indicated by success_flag, and returns False.

       Otherwise as long as retreat() is searching, it first removes the Queen
       and associated attacking information for further tries.

       If a new column and row to try are found then queen_column contains
       the column number, try_row the row to try and True is returned. In
       that case, admissible_rows[] for that column is also
       updated.

       show_retreating() is called for every queen_column decrement.

       Note: success_flag is passed in True if we've found some solution
       already; otherwise it is False.

       retreat() is complicated by handling different behavior needed
       because of adding the ability to find all solutions, and for
       performance.
    """

    global queen_column
    global try_row
    global admissible_rows
    global row_lookup
    global slash_code_lookup
    global backslash_code_lookup
    global queen_location

    # We have to go back to the "previous column"; which may be the final
    # column on the board.
    queen_column -= 1
    show_retreating()
    while queen_column > -1:
        # Can retreat.
        # Remove the Queen from the board.
        queen_row = queen_location[queen_column]
        row_lookup[queen_row] = False
        slash_code_lookup[slash_code[queen_row][queen_column]] = False
        backslash_code_lookup[backslash_code[queen_row][queen_column]] = False
        queen_location[queen_column] = -1

        # Try the next admissible row after the one we tried last.
        search_list = admissible_rows[queen_column]
        if search_list:
            # More to try.
            # Get the next try_row. NB: This also changes
            # admissible_rows[queen_column] since search_list is a
            # reference!
            try_row = search_list.pop(0)
            return True
        else:
            queen_column -= 1            
            show_retreating()

    # Cannot retreat.
    if find_all_solutions:
        if success_flag:
            # We already found a solution.
            show_no_more_solutions()
        else:
            # No solution.
            show_no_solution()
    else:
        # No solution.
        show_no_solution()

    return False


def get_search_list_2():
    """Get the admissible rows by filtering several functions
       iteratively and short circuiting early if none free.
    """

    def row_check(sr):
        return not row_lookup[sr]

    def slash_check(sr):
        return not slash_code_lookup[slash_code[sr][queen_column]]

    def backslash_check(sr):
        return not backslash_code_lookup[backslash_code[sr][queen_column]]

    empty_list = []
    search_list = list(filter(row_check, row_indices))
    if search_list:
        # Got free ones so far.
        search_list = list(filter(slash_check, search_list))
        if search_list:
            # Got free ones so far.
            search_list = list(filter(backslash_check, search_list))
            if search_list:
                # Got non empty search_list.
                return search_list
            else:
                # Nothing free.
                return empty_list
        else:
            # Nothing free.
            return empty_list
    else:
        # Nothing free.
        return empty_list


def get_search_list_1():
    """Get the admissible rows by filtering a function over the
       row_indices checking for freedom in all directions at once.
    """

    def free_row(sr):
        return not (slash_code_lookup[slash_code[sr][queen_column]]
                    or backslash_code_lookup[backslash_code[sr][queen_column]]
                    or row_lookup[sr])

    # Get all the remaining admissible rows for queen_column; if any.
    search_list = list(filter(free_row, row_indices))
    return search_list


def initialize_admissible_rows():
    """For the current number_of_rows and queen_column, finds all the
       admissible rows. Then if there are any such rows, pop the first
       admissible row into try_row and save the remainder in
       admissible_rows[queen_column]; return True. Otherwise, return
       False.
    """
    global try_row
    global admissible_rows

    # Get all the remaining admissible rows for queen_column; if any.
    search_list = get_search_list_1()
    # random.shuffle(search_list)

    if search_list:
        # Set the next row location to try putting the Queen.
        # Last or first; doesn't seem to matter in finding all solutions.
        # try_row = search_list.pop()
        try_row = search_list.pop(0)
        # Save the remaining admissible rows if any.
        admissible_rows[queen_column] = search_list
        return True
    else:
        # No admissible rows.
        return False


def store_and_check_for_solution():
    """Place the current Queen on the board. If this is a solution
       return True; otherwise return False
    """
    global queen_location
    global row_lookup
    global slash_code_lookup
    global backslash_code_lookup
    global queen_column
    global node_count
    global total_node_count

    show_advancing()
    queen_location[queen_column] = try_row
    row_lookup[try_row] = True
    slash_code_lookup[slash_code[try_row][queen_column]] = True
    backslash_code_lookup[backslash_code[try_row][queen_column]] = True
    queen_column += 1
    node_count += 1
    total_node_count += 1

    if queen_column <= number_of_columns - 1:
        # No solution yet.
        return False
    else:
        # We have a solution.
        return True


def search():
    """Search for a solution and return True if found else False"""
    global solution_count
    global node_count

    # Return value.
    # True if we find a solution; False otherwise.
    success_flag = False

    more_to_search = True
    while more_to_search:
        assert try_row <= number_of_rows - 1
        # Store the info and see if we have a solution.
        if not store_and_check_for_solution():
            # No solution yet.
            if initialize_admissible_rows():
                pass
            else:
                # We could not place the next Queen anywhere.
                # Try to back out the last Queen assignment and prepare
                # to try the next possibility.
                more_to_search = retreat(success_flag)
        else:
            # We found a solution.
            success_flag = True
            show_found_solution()
            print_solution()
            solution_count += 1
            node_count = 0
            if find_all_solutions:
                more_to_search = retreat(success_flag)
            else:
                more_to_search = False
    return success_flag


def initialize(size):
    """Initialize for the next problem of a given size"""
    global number_of_columns
    global number_of_rows
    global queen_location
    global admissible_rows
    global queen_column
    global node_count
    global total_node_count
    global progress_count
    global solution_count
    global slash_code
    global backslash_code
    global slash_code_lookup
    global backslash_code_lookup
    global row_indices
    global row_lookup
    global try_row
    
    # Set the size of the chessboard.
    number_of_columns = size
    number_of_rows = size

    # Empty the Queen locations.
    queen_location = [-1] * number_of_columns

    # Empty the admissible rows.
    admissible_rows = [[] for _ in range(number_of_columns)]

    # The next column to try placing a Queen.
    queen_column = 0

    # Set our counters and such.
    node_count = 0
    total_node_count = 0
    progress_count = 0
    solution_count = 0

    # Set our helper matrices for optimization.
    slash_code = [[0 for _ in range(0, number_of_columns)]
                  for _ in range(0, number_of_rows)]
    backslash_code = [[0 for _ in range(0, number_of_columns)]
                      for _ in range(0, number_of_rows)]
    for r in range(0, number_of_rows):
        for c in range(0, number_of_columns):
            slash_code[r][c] = r + c
            backslash_code[r][c] = r - c + number_of_columns - 1

    slash_code_lookup = [False] * (number_of_columns + number_of_rows - 1)
    backslash_code_lookup = [False] * (number_of_columns + number_of_rows - 1)
    row_lookup = [False] * number_of_rows
    row_indices = list(range(0, number_of_rows))

    # Initialize admissible_rows and try_row.
    if not initialize_admissible_rows():
        print("Error: initialization fail!!")
    

def check_num(s):
    """Check that a string is an integer."""
    try:
        int(s)
        return True
    except ValueError:
        return False


def sanity_check_args(start, number_of_problems):
    """Sanity check the user arguments."""

    if check_num(start):
        start = int(start)
    else:
        print('error: {}'.format(start), ' is not a number.')
        sys.exit(1)

    if check_num(number_of_problems):
        number_of_problems = int(number_of_problems)
    else:
        print('error: {}'.format(number_of_problems), ' is not a number.')
        sys.exit(1)

    if start <= 0:
        print('error: starting value must be greater than 0')
        sys.exit(1)

    if number_of_problems < 1:
        print('error: number of problem sizes must be greater than 0')
        sys.exit(1)

    if ((start + number_of_problems) - 1) > _MAX_COLUMNS:
        print('error: Sorry. Limit is {} columns'.format(_MAX_COLUMNS))
        sys.exit(1)


# noinspection SpellCheckingInspection
# Previous comment is for IntelliJ to stop complaining.
def run(start=8, number_of_problems=1,
        fas=False,
        sp=False,
        np=False,
        snc=False,
        stnc=False):
    global find_all_solutions
    global show_progress
    global no_print
    global show_node_count
    global show_total_node_count

    find_all_solutions = fas
    show_progress = sp
    no_print = np
    show_node_count = snc
    show_total_node_count = stnc

    start_time = time.time()
    for size in range(start, start + number_of_problems):
        initialize(size)
        if find_all_solutions:
            print("Looking for all solutions "
                  + "to the {}-Queen problem.".format(size))
        else:
            print("Looking for a solution "
                  + "to the {}-Queen problem.".format(size))
        if search():
            # Got at least one solution.
            if find_all_solutions:
                print("Found all solutions to the {}-Queen".format(size),
                      "problem.")
            else:
                pass
        else:
            # No solution.
            print("No solution to the {}-Queen".format(size), "problem.")

        if find_all_solutions:
            print("Total solutions found to the",
                  "{}-Queen problem is".format(size),
                  "{}".format(solution_count))
        if show_total_node_count:
            print("Searched {}".format(total_node_count), "total nodes.")
        print("----------------------------------------")
    end_time = time.time()
    print("Execution time in secs was {}".format(end_time-start_time))


def run_with_args(args):
    """Run the program with args already parsed"""
    global find_all_solutions
    global show_progress
    global no_print
    global show_node_count
    global show_total_node_count

    sanity_check_args(args.start, args.number_of_problems)
    start = int(args.start)
    number_of_problems = int(args.number_of_problems)
    if args.all:
        find_all_solutions = True
    if args.show_progress:
        show_progress = True
    if args.no_print:
        no_print = True
    if args.show_node_count:
        show_node_count = True
    if args.show_total_node_count:
        show_total_node_count = True

    run(start, number_of_problems, find_all_solutions,
        show_progress, no_print, show_node_count,
        show_total_node_count)


def main():
    """Main code with command line parser"""
    parser = argparse.ArgumentParser(description="Solve N-queen problems")
    parser.add_argument('start', type=int,
                        help='minimum board starting size')
    parser.add_argument('number_of_problems', type=int,
                        help='number of problems sizes to do')
    parser.add_argument('--all', action='store_true',
                        help="find all solutions")
    parser.add_argument('--show_progress', action='store_true',
                        help="show progress")
    parser.add_argument('--show_node_count', action='store_true',
                        help="show node counts")
    parser.add_argument('--show_total_node_count', action='store_true',
                        help="show total node counts")
    parser.add_argument('--no_print', action='store_true',
                        help="do not print boards")
    parser.set_defaults(func=run_with_args)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
