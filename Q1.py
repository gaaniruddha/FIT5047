import argparse as ap
import re
import platform
# To use functions that work on iterators
import itertools


######## RUNNING THE CODE ####################################################

#   You can run this code from terminal by executing the following command

#   python planpath.py <INPUT/input#.txt> <OUTPUT/output#.txt> <flag>

#   for example: python planpath.py INPUT/input2.txt OUTPUT/output2.txt 0

#   NOTE: THIS IS JUST ONE EXAMPLE INPUT DATA

###############################################################################


################## YOUR CODE GOES HERE ########################################
# Creating a class Node
class Node():
    # Global variable counter, in order to name the Node
    count_value = itertools.count()

    # For creating instance variables parent and position
    def __init__(self, node_parent=None, node_position=None):

        # Creating the Node components as per the document specification
        # Node's parent
        self.node_parent = node_parent

        # Node's current position in terms of 0s and 1s
        self.node_position = node_position

        # Cost g of reaching that Node
        self.g = 0

        # Heuristic Value h
        self.h = 0

        # Value f, where f=g+h
        self.f = 0

        # Node Identifier
        self.node_id = "N" + str(next(self.count_value))

        # Node's current move
        # For Start Position, move = S, Goal Position, move = G
        # By Default, it would be blank
        self.move = ""
        # Order of expansion, by Default 0
        self.expansion_order = 0

    def __str__(self):
        if self.move == "S":
            return "S"
        else:
            path = self.get_path_value()
            return path

    # For checking the positions of the two nodes
    def __eq__(self, other):
        return self.node_position == other.node_position

    # For determining the path of the Node
    def get_path_value(self):
        path_list = []
        temp_node = self
        while temp_node is not None:
            # Append the current node's move value to path
            path_list.append(temp_node.move)
            # Go back to the parent node
            temp_node = temp_node.node_parent

        # Returning the reverse list
        final_path_list = "-".join(path_list[::-1])
        return final_path_list

# End of Class Node

def graphsearch(map, flag):
    # Popping out the first element, which also gives us number of rows and columns
    map.pop(0)[0]

    # This map only has the contents of the tiles
    final_map = []

    # To keep a tab of all the blocks which have mountains
    mountain_blocks = []

    # By default, as per the question, let us assign the top-left corner as the starting position
    start = (0, 0)

    # To iterate through the map and determine the start and goal positions
    for x, rows in enumerate(map):

        rows.pop()
        # Locating start, goal and mountain blocks
        for y, block in enumerate(rows):
            if block == "S":
                start = (x, y)
            elif block == "G":
                end = (x, y)
            elif block == "X":
                mountain_blocks.append((x, y))

        # Appending rows to the final map
        final_map.append(rows)

    # Creating the class Node object - start_node
    # Parent = None, Position = start
    starting_node = Node(None, start)
    starting_node.g = 0
    starting_node.h = 0
    starting_node.f = 0
    starting_node.move = "S"

    # Creating the class Node object - start_node
    # Parent = None, Position = end
    goal_node = Node(None, end)
    goal_node.g = 0
    goal_node.h = 0
    goal_node.f = 0
    goal_node.move = "G"

    # Open list will contain the children of the Node
    # This list contains the nodes which are still remaining to be searched
    open_list = []

    # Closed list will contain the Node and it's ancestors
    # This list contains the nodes which have been searched
    closed_list = []

    # Assigning expansion the value 1 to begin with
    expansion = 1

    # Appending the starting node to the open list
    open_list.append(starting_node)

    # We iterate through the open list to find the goal node
    while len(open_list) > 0:

        # Accessing the first value in the open list and assigning it to current node
        current_node = open_list[0]
        current_index_value = 0

        # Checking if the current node if the most efficient node or not by comparing the f values
        for i, node in enumerate(open_list):
            if node.f < current_node.f:
                current_node = node
                current_index_value = i

        # Updating the expansion order
        current_node.expansion_order = expansion

        # Popping off the current node from the open list
        open_list.pop(current_index_value)

        # Adding the current node to the closed list
        closed_list.append(current_node)

        # Checking if we have reached the Goal or not
        if current_node == goal_node:
            # return the final path value

        # For storing thr children of a given node
        node_children = []

        # For removing the children of nodes that cannot be accessed because of mountain nodes
        children_to_be_removed = []

        for new_node_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:

            # Get node position
            new_node_position = (current_node.node_position[0] + new_node_position[0], current_node.node_position[1] + new_node_position[1])

            # Checking if the blocks can be travelled or not
            if new_node_position in [(0, 1), (1, 0), (-1, 0), (0, -1)]:

                # If the node contains a mountain, that node needs to be removed
                if new_node_position in mountain_blocks:
                    children_to_be_removed.append(new_node_position)

                    # When we encounter a mountain node, as per the given conditions, we need to remove other nodes too
                    # Mountain present on right, remove bottom right and top right blocks
                    if new_node_position == (0, 1):
                        children_to_be_removed.append((new_node_position[0] + 1, new_node_position[1]))
                        children_to_be_removed.append((new_node_position[0] - 1, new_node_position[1]))

                    # Mountain present on left, remove bottom left and bottom right blocks
                    elif new_node_position == (1, 0):
                        children_to_be_removed.append((new_node_position[0], new_node_position[1] - 1))
                        children_to_be_removed.append((new_node_position[0], new_node_position[1] + 1))

                    # Mountain present on top, remove top left and top right blocks
                    elif new_node_position == (-1, 0):
                        children_to_be_removed.append((new_node_position[0], new_node_position[1] + 1))
                        children_to_be_removed.append((new_node_position[0], new_node_position[1] - 1))

                    # Mountain present at the bottom, remove bottom left and bottom right blocks
                    elif new_node_position == (0, -1):
                        children_to_be_removed.append((new_node_position[0] + 1, new_node_position[1]))
                        children_to_be_removed.append((new_node_position[0] - 1, new_node_position[1]))

        # Calculating the g, h and f values
        for every_child in node_children:

            # Given that cost of the move other than the diagonal move is 2
            if every_child.move in ["L", "R", "U", "D"]:
                every_child.g = current_node.g + 2

            # Given that cost of diagonal move is 1
            elif every_child.move in ["LU", "RU", "LD", "RD"]:
                every_child.g = current_node.g + 1

            # Calculating h value
            every_child.h = ((every_child.node_position[0] - goal_node.node_position[0]) ** 2) + \
                            ((every_child.node_position[1] - goal_node.node_position[1]) ** 2)

            # Given that f = g + h
            every_child.f = every_child.g + every_child.h

            # Adding the child to the open list
            open_list.append(every_child)

            # We need to find the best minimal path possible, hence we consider the nodes with the lowest g value
            for open_node in open_list:
                if every_child == open_node and every_child.g > open_node.g:
                    open_list.remove(every_child)

        expansion += 1

    return "NO-PATH"


def read_from_file(file_name):
    # You can change the file reading function to suit the way
    # you want to parse the file

    # Reading the file using file pointer file_handle
    file_handle = open(file_name)

    # List to store the map elements
    map_grid = []

    # In order to read the contents line by line
    rows_info = file_handle.readlines()

    # Here enumerate is used to number the rows and create them into a list
    for i, item in enumerate(rows_info):
        map_grid.append(list(item))

    return map_grid


###############################################################################

########### DO NOT CHANGE ANYTHING BELOW ######################################

###############################################################################


def write_to_file(file_name, solution):
    file_handle = open(file_name, 'w')

    file_handle.write(solution)


def main():
    # create a parser object

    parser = ap.ArgumentParser()

    # specify what arguments will be coming from the terminal/commandline

    parser.add_argument("input_file_name", help="specifies the name of the input file", type=str)

    parser.add_argument("output_file_name", help="specifies the name of the output file", type=str)

    parser.add_argument("flag", help="specifies the number of steps that should be printed", type=int)

    # parser.add_argument("procedure_name", help="specifies the type of algorithm to be applied, can be D, A", type=str)

    # get all the arguments

    arguments = parser.parse_args()

    ##############################################################################

    # these print statements are here to check if the arguments are correct.

    #    print("The input_file_name is " + arguments.input_file_name)

    #    print("The output_file_name is " + arguments.output_file_name)

    #    print("The flag is " + str(arguments.flag))

    #    print("The procedure_name is " + arguments.procedure_name)

    ##############################################################################

    # Extract the required arguments

    operating_system = platform.system()

    if operating_system == "Windows":

        input_file_name = arguments.input_file_name

        input_tokens = input_file_name.split("\\")

        if not re.match(r"(INPUT\\input)(\d)(.txt)", input_file_name):
            print("Error: input path should be of the format INPUT\input#.txt")

            return -1

        output_file_name = arguments.output_file_name

        output_tokens = output_file_name.split("\\")

        if not re.match(r"(OUTPUT\\output)(\d)(.txt)", output_file_name):
            print("Error: output path should be of the format OUTPUT\output#.txt")

            return -1

    else:

        input_file_name = arguments.input_file_name

        input_tokens = input_file_name.split("/")

        if not re.match(r"(INPUT/input)(\d)(.txt)", input_file_name):
            print("Error: input path should be of the format INPUT/input#.txt")

            return -1

        output_file_name = arguments.output_file_name

        output_tokens = output_file_name.split("/")

        if not re.match(r"(OUTPUT/output)(\d)(.txt)", output_file_name):
            print("Error: output path should be of the format OUTPUT/output#.txt")

            return -1

    flag = arguments.flag

    # procedure_name = arguments.procedure_name

    try:

        map = read_from_file(input_file_name)  # get the map

    except FileNotFoundError:

        print("input file is not present")

        return -1

    # print(map)

    solution_string = ""  # contains solution

    solution_string = graphsearch(map, flag)

    write_flag = 1

    # call function write to file only in case we have a solution

    if write_flag == 1:
        write_to_file(output_file_name, solution_string)


if __name__ == "__main__":
    main()

