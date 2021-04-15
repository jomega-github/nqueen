#!/usr/bin/python

"""The N-Queens problem. Version 2.1"""

import argparse
import sys
import time
import logging

logging.basicConfig(
    format='%(levelname)s:%(funcName)s:%(lineno)d:%(message)s',
    level=logging.DEBUG)
#    level=logging.ERROR) # if not debugging. Or use -O python option.
#    logging.debug(" = %s", )

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
# -1 if there is no Queen in that column.
# This 'array' is indexed starting at 0!
# It is actually a list in Python.
# Will be queen_location = [-1] * number_of_columns
queen_location = []
# The saved search list of admissible rows.
# Will be admissible_rows = [[] for _ in range(number_of_columns)]
# NB: admissible_rows = [] * (number_of_columns) does NOT work; it gives [].
admissible_rows = []
# The next row location to try putting the Queen.
try_row = 0
# The next column to try placing a Queen.
queen_column = 0
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

# Optimization helper matrices
# Will be...
# slash_code = [[0 for _ in range(0, number_of_columns)]
#                for _ in range(0, number_of_rows)]
# backslash_code = [[0 for _ in range(0, number_of_columns)]
#                    for _ in range(0, number_of_rows)]
slash_code = []
backslash_code = []
# Will be...
# row_lookup = [False] * (number_of_rows)
# slash_code_lookup = [False] * (number_of_columns + number_of_rows - 1)
# backslash_code_lookup = [False] * (number_of_columns + number_of_rows - 1)
row_lookup = []
slash_code_lookup = []
backslash_code_lookup = []
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
    if show_count_only:
        return

    for row in range(0, number_of_rows):
        for column in range(0, number_of_columns):
            if queen_location[column] == row:
                print("Q", end='')
            else:
                print("-", end='')
        print()
    print("---------------------")


def retreat():
    """Prepare to try the next location for the previously placed Queen.
       If we cannot retreat, then return False. Otherwise we
       return True and queen_column is the new column to try; starting
       at row try_row.

    """
    global queen_column
    global try_row
    global admissible_rows
    global row_lookup
    global slash_code_lookup
    global backslash_code_lookup
    global queen_location

    # We have to go back to the previous column.
    queen_column -= 1
    if __debug__:
        # noinspection PyUnreachableCode
        logging.debug("We have to go back to column %s", queen_column)
    show_retreating()
    if queen_column > -1:
        # Try the next admissible row after the one we tried last.
        search_list = admissible_rows[queen_column]
        if search_list:
            # More to try.
            if __debug__:
                logging.debug("More to try in column %s", queen_column)
            try_row = search_list.pop(0)
            admissible_rows[queen_column] = search_list
            if __debug__:
                logging.debug("try_row = %s", try_row)
                logging.debug("admissible_rows = %s", admissible_rows)
        else:
            # Stop the searching.
            try_row = number_of_rows
            if __debug__:
                logging.debug("Stop searching for column %s", queen_column)
                logging.debug("try_row = %s", try_row)
        # Remove the Queen from the board.
        queen_row = queen_location[queen_column]
        row_lookup[queen_row] = False
        slash_code_lookup[slash_code[queen_row][queen_column]] = False
        backslash_code_lookup[backslash_code[queen_row][queen_column]] = False
        queen_location[queen_column] = -1
        if __debug__:
            logging.debug("Remove the queen from column %s", queen_column)
            logging.debug("row_lookup = %s", row_lookup)
            logging.debug("slash_code_lookup = %s", slash_code_lookup)
            logging.debug("backslash_code_lookup = %s", backslash_code_lookup)
            logging.debug("queen_location = %s", queen_location)
        return True
    else:
        # Cannot retreat.
        if __debug__:
            logging.debug("Cannot retreat.")
        return False


def retreat_wrapper(success_flag):
    """A wrapper to handle the different behavior need because of adding the
       ability to find all solutions.
       If success_flag is True then we've found some solution already;
       otherwise we have not.
       The return value is True if the search for solutions should continue
       and False otherwise.
       If we cannot retreat, then return False. Otherwise we
       return True and queen_column is the new column to try; starting
       at row try_row.

    """
    global node_count

    more_to_search = True
    if not retreat():
        more_to_search = False
        if find_all_solutions:
            if success_flag:
                # We already found a solution.
                show_no_more_solutions()
                node_count = 0
            else:
                # No solution.
                show_no_solution()
        else:
            # No solution.
            show_no_solution()
    else:
        pass
    return more_to_search


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
       admissible_rows[queen_column]. Otherwise, set try_row to
       number_of_rows to indicate no more rows to try.

    """
    global try_row
    global admissible_rows

    # Get all the remaining admissible rows for queen_column; if any.
    search_list = get_search_list_1()
    if __debug__:
        logging.debug("search_list = %s", search_list)

    if search_list:
        # Set the next row location to try putting the Queen.
        # Last
        # try_row = search_list.pop()
        # or first doesn't seem to matter in finding all solutions.
        try_row = search_list.pop(0)
        if __debug__:
            logging.debug("try_row = %s", try_row)
    else:
        # Stop the searching.
        try_row = number_of_rows
        if __debug__:
            logging.debug("try_row = %s", try_row)

    # Save the remaining admissible rows if any.
    admissible_rows[queen_column] = search_list
    if __debug__:
        logging.debug("admissible_rows = %s", admissible_rows)


def advance():
    """Place the current Queen on the board and prepare to
       try the next column. Return False if all the Queens are
       placed. Otherwise return True.

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
    if __debug__:
        logging.debug("queen_location = %s", queen_location)
        logging.debug("row_lookup = %s", row_lookup)
        logging.debug("slash_code_lookup = %s", slash_code_lookup)
        logging.debug("backslash_code_lookup = %s", backslash_code_lookup)
        logging.debug("queen_column = %s", queen_column)
        logging.debug("node_count = %s", node_count)
        logging.debug("total_node_count = %s", total_node_count)

    if queen_column <= number_of_columns - 1:
        initialize_admissible_rows()
        return True
    else:
        return False


def search():
    """Search for a solution and return True if found else False"""
    global solution_count
    global node_count

    # Return value.
    # True if we find a solution; False otherwise.
    success_flag = False

    more_to_search = True
    while more_to_search:
        if __debug__:
            logging.debug("try_row = %s, column = %s", try_row, queen_column)
        if try_row <= number_of_rows - 1:
            # Store the info and see if we have a solution.
            # Note: After calling advance() we have
            #       queen_location[queen_column] = try_row
            #       queen_column += 1
            #       try_row = next row to try or number_of_rows
            if __debug__:
                logging.debug("Try advancing.")
            if advance():
                if __debug__:
                    logging.debug("Advancing worked.")
                # queen_column <= number_of_columns - 1
                pass
            else:
                # We found a solution. NB: queen_column = number_of_columns
                if __debug__:
                    logging.debug("Found a solution.")
                show_found_solution()
                solution_count += 1
                node_count = 0
                print_solution()
                success_flag = True
                if find_all_solutions:
                    more_to_search = retreat_wrapper(success_flag)
                else:
                    more_to_search = False
        else:
            if __debug__:
                logging.debug("No more attempts in column %s", queen_column)
            # We could not place the current Queen.
            # Try to back out the last Queen assignment and prepare
            # to try the next possibility.
            # Note: After calling retreat_wrapper() we have
            #       queen_column -= 1
            #       As long as queen_column > -1 we have
            #       try_row = next row to try or number_of_rows
            #       queen_location[queen_column] = -1
            more_to_search = retreat_wrapper(success_flag)
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
    
    if __debug__:
        logging.debug("size = %s", size)

    # Set the size of the chessboard.
    number_of_columns = size
    number_of_rows = size
    if __debug__:
        logging.debug("number_of_rows = %s", number_of_rows)
        logging.debug("number_of_columns = %s", number_of_columns)

    # Empty the Queen locations.
    queen_location = [-1] * number_of_columns
    if __debug__:
        logging.debug("queen_location = %s", queen_location)

    # Empty the admissible rows.
    admissible_rows = [[] for _ in range(number_of_columns)]
    if __debug__:
        logging.debug("admissible_rows = %s", admissible_rows)

    # The next column to try placing a Queen.
    queen_column = 0
    if __debug__:
        logging.debug("queen_column = %s", queen_column)

    # Set our counters and such.
    node_count = 0
    total_node_count = 0
    progress_count = 0
    solution_count = 0
    if __debug__:
        logging.debug("node_count = %s", node_count)
        logging.debug("total_node_count = %s", total_node_count)
        logging.debug("progress_count = %s", progress_count)
        logging.debug("solution_count = %s", solution_count)

    # Set our helper matrices for optimization.
    slash_code = [[0 for _ in range(0, number_of_columns)]
                  for _ in range(0, number_of_rows)]
    backslash_code = [[0 for _ in range(0, number_of_columns)]
                      for _ in range(0, number_of_rows)]
    for r in range(0, number_of_rows):
        for c in range(0, number_of_columns):
            slash_code[r][c] = r + c
            backslash_code[r][c] = r - c + number_of_columns - 1
    if __debug__:
        logging.debug("slash_code = %s", slash_code)
        logging.debug("backslash_code = %s", backslash_code)

    slash_code_lookup = [False] * (number_of_columns + number_of_rows - 1)
    backslash_code_lookup = [False] * (number_of_columns + number_of_rows - 1)
    row_lookup = [False] * number_of_rows
    if __debug__:
        logging.debug("slash_code_lookup = %s", slash_code_lookup)
        logging.debug("backslash_code_lookup = %s", backslash_code_lookup)
        logging.debug("row_lookup = %s", row_lookup)

    row_indices = list(range(0, number_of_rows))

    # Initialize admissible_rows and try_row.
    initialize_admissible_rows()
    if __debug__:
        logging.debug("row_indices = %s", row_indices)
        logging.debug("try_row = %s", try_row)
        logging.debug("admissible_rows = %s", admissible_rows)


def check_num(s):
    """check that a string is an integer"""
    try:
        int(s)
        return True
    except ValueError:
        return False


def sanity_check_args(start, number_of_problems):
    """sanity check the users arguments"""

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


# noinspection PyShadowingNames
def run(start=8, number_of_problems=1,
        all_solutions=False,
        progress=False,
        count_only=False,
        node_count=False,
        total_node_count=False):
    global find_all_solutions
    global show_progress
    global show_count_only
    global show_node_count
    global show_total_node_count

    find_all_solutions = all_solutions
    show_progress = progress
    show_count_only = count_only
    show_node_count = node_count
    show_total_node_count = total_node_count

    start_time = time.time()
    for size in range(start, start+number_of_problems):
        initialize(size)
        if find_all_solutions:
            print("Looking for all solutions "
                  + "to the {}-Queen problem".format(size))
            if __debug__:
                logging.debug("Looking for all solutions to the "
                              + "%s-Queen problem", size)
        else:
            print("Looking for a solution "
                  + "to the {}-Queen problem".format(size))
            if __debug__:
                logging.debug("Looking for a solution to the %s-Queen problem",
                              size)
        if search():
            # Got at least one solution.
            if find_all_solutions:
                print("All solutions found to {}-Queen".format(size))
                if __debug__:
                    logging.debug("All solutions found to size %s", size)
            else:
                pass
        else:
            # No solution.
            print("No solution to {}-Queen".format(size))
            if __debug__:
                logging.debug("No solution to size %s", size)

        if find_all_solutions:
            print("Total solutions found {} ".format(solution_count)
                  + "for {}-Queen".format(size))
        if show_total_node_count:
            print("Searched {}".format(total_node_count), "total nodes.")
        print("----------------------------------------")
    end_time = time.time()
    print("Execution time in secs was {}".format(end_time-start_time))


def run_with_args(args):
    """Run the program with args already parsed"""
    global find_all_solutions
    global show_progress
    global show_count_only
    global show_node_count
    global show_total_node_count

    sanity_check_args(args.start, args.number_of_problems)
    start = int(args.start)
    number_of_problems = int(args.number_of_problems)
    if args.all:
        find_all_solutions = True
    if args.show_progress:
        show_progress = True
    if args.show_count_only:
        show_count_only = True
    if args.show_node_count:
        show_node_count = True
    if args.show_total_node_count:
        show_total_node_count = True
    if args.show_count_only:
        show_count_only = True
        show_node_count = False
        show_total_node_count = False

    run(start, number_of_problems,
        find_all_solutions,
        show_progress,
        show_count_only,
        show_node_count,
        show_total_node_count)


def main():
    """Main code with command line parser"""
    parser = argparse.ArgumentParser(description="Solve N-queen problems")
    parser.add_argument('start', type=int,
                        help='minimum board starting size')
    parser.add_argument('number_of_problems', type=int,
                        help='number of problems sizes to do')
    parser.add_argument('--all', action='store_true',
                        help="print all solutions")
    parser.add_argument('--show_progress', action='store_true',
                        help="show progress")
    parser.add_argument('--show_node_count', action='store_true',
                        help="show node counts")
    parser.add_argument('--show_total_node_count', action='store_true',
                        help="show total node counts")
    parser.add_argument('--show_count_only', action='store_true',
                        help="show solution counts only")
    parser.set_defaults(func=run_with_args)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
