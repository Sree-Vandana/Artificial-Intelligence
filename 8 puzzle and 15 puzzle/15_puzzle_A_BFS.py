"""
<!-- Steps to execute the program -->
@ Input:    No need (all values are hard-coded into program)

@ Output:   first it displays the output generated by BFS and then A* output for all three heuristics for all 5 puzzles.

@ To change the puzzle initial state:   To test the algorithm on different start states.
                                        In main function (end of file), all the 5 initial state are written in 4x4 matrix format.
                                        It can be changed before execution.

@ To change the goal state:     goal state is declared as a global variable. (at the top).

Algorithms Implemented
1. BFS - Best First Search
2. A * - A-star

puzzle size: 4 x 4, filled with numbers from [1, 15] the blank space 'b' is represented using '0'
Initial state: the initial 4x4 matrix values is given in main function
                (algorithms run on 5 different start state)
Goal state: the final goal is defined as a global variable --> [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]

"""
goal_state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]  # Goal state


class Puzzle:
    def __init__(self):  # initialize all the variables
        self.node_data = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.h_val = 0
        self.parent = None
        self.depth = 0

    """
    A 4x4 puzzle is created using initial state values
    """

    def create_puzzle(self, initial_state):
        l = len(initial_state)
        for row in range(l):
            for col in range(l):
                self.node_data[row][col] = initial_state[row][col]
        print("--> ", self.node_data, "\n")

    """
    the entire path from initial_state to goal_state is stored in a list
    return: [path_list]
    """

    def solution_path(self, path_list):
        if self.parent is None:
            return path_list
        else:
            path_list.append(self)
            return self.parent.solution_path(path_list)

    """    
    function to find the blank space index value
    return: index's of blank (row, col)
    """

    def find_blank(self, node):
        l = len(node)
        for row in range(l):
            for col in range(l):
                if node[row][col] == 0:
                    return row, col
                else:
                    continue

    """
    function to check if a node is visited/explored or  not
    return: boolean
    """

    def visited(self, nodes, lists):  # To check if the node_data is also visited
        for i in range(len(lists)):
            if lists[i].node_data == nodes.node_data:
                return i
        return -1

    """
    To generate a child node_data, parent node_data is cloned
    return: puzzle object
    """

    def clone(self):
        p = Puzzle()
        p.h_val = 0
        p.parent = self
        p.depth = self.depth + 1
        for row in range(4):
            for col in range(4):
                p.node_data[row][col] = self.node_data[row][col]
        return p

    """ 
    function to generate all possible child nodes (all possible states of puzzle, by shuffling blank)
    return: [list of all possible states]
    """

    def get_all_child_nodes(self):
        possible_child_nodes = []
        row, col = self.find_blank(self.node_data)

        if row > 0:  # move up
            p = self.clone()
            p.node_data[row - 1][col], p.node_data[row][col] = p.node_data[row][col], p.node_data[row - 1][col]
            possible_child_nodes.append(p)

        if row < 3:  # move down
            p = self.clone()
            p.node_data[row + 1][col], p.node_data[row][col] = p.node_data[row][col], p.node_data[row + 1][col]
            possible_child_nodes.append(p)

        if col > 0:  # move right
            p = self.clone()
            p.node_data[row][col - 1], p.node_data[row][col] = p.node_data[row][col], p.node_data[row][col - 1]
            possible_child_nodes.append(p)

        if col < 3:  # move left
            p = self.clone()
            p.node_data[row][col + 1], p.node_data[row][col] = p.node_data[row][col], p.node_data[row][col + 1]
            possible_child_nodes.append(p)

        return possible_child_nodes

    """
    Heuristic 1: Number of misplaced tiles h(n)
    """

    def heuristic_1_misplacedTiles(self):
        h_val = 0
        l = len(self.node_data)
        for row in range(l):
            for col in range(l):
                if self.node_data[row][col] == 0:
                    continue
                elif self.node_data[row][col] != goal_state[row][col]:
                    h_val = h_val + 1
        return h_val

    """
    Heuristic 2: Manhattan distance h(n)
    """

    def heuristic_2_manhattanDistance(self):  # calculating the manhattan distance
        h_val = 0
        l = len(self.node_data)
        for row in range(l):
            for col in range(l):
                if self.node_data[row][col] != 0:
                    if self.node_data[row][col] != goal_state[row][col]:
                        c = self.node_data[row][col] - 1
                        actual_col = c % 4
                        actual_row = c / 4
                        h_val = h_val + abs(actual_row - row) + abs(actual_col - col)
        return h_val

    """
    Heuristic 3: Chebyshev distance calculation, commonly known as the "maximum metric" h(n)
    """

    def heuristic_3_maxMatrix(self):
        h_val = 0
        l = len(self.node_data)
        for row in range(l):
            for col in range(l):
                if self.node_data[row][col] != 0:
                    if self.node_data[row][col] != goal_state[row][col]:
                        c = self.node_data[row][col] - 1
                        actual_col = c % 4
                        actual_row = c / 4
                        max_val = max((abs(actual_row - row)), (abs(actual_col - col)))
                        h_val = h_val + max_val
        return h_val

    """
    function logic for both BFS and A* algorithm (only the evaluation function changes)
    Evaluation function for BFS: f(n) = h(n)
    Evaluation function for A* : f(n) = h(n) + g(n)

    :param h: indicates which heuristics is running
    :param algo: indicates which algorithm is running (either BFS or A*): BFS = 0; A* = 1
    :return: [path_list] and number of moves
    """

    def BFS_a_star(self, h, algo):
        h_val = 0  # calculated heuristic value
        open_list = [self]  # list of discovered nodes
        close_list = []  # list of explored nodes
        sol_path = []  # list to store final path (if puzzle solved)
        count = 0  # algorithm runs max limit 1000

        while len(open_list) > 0:  # Loop until we have unexplored all nodes
            if count < 1000:  # Limit the search by 1000
                curr_node = open_list.pop(0)  # get current node to explore
                count = count + 1

                if curr_node.node_data == goal_state:  # puzzle solved
                    print("Puzzle Solved")
                    if len(close_list) > 0:
                        return curr_node.solution_path(sol_path), curr_node.depth
                    return sol_path

                else:  # if puzzle not yet solved (get other possible states from current state)
                    child_nodes_list = curr_node.get_all_child_nodes()  # generating the successor nodes

                    for nodes in child_nodes_list:
                        open_index = self.visited(nodes, open_list)
                        close_index = self.visited(nodes, close_list)

                        # Heuristic function h(n)
                        if h == 0:  # 1. for misplaced tile
                            h_val = nodes.heuristic_1_misplacedTiles()
                        elif h == 1:  # 2. for Manhattan distance
                            h_val = nodes.heuristic_2_manhattanDistance()
                        elif h == 2:  # 3. for max matrix distance
                            h_val = nodes.heuristic_3_maxMatrix()

                        # Evaluation function for both algorithms (BFS = 0 and A* = 1)
                        f_val = 0
                        if algo == 0:
                            f_val = h_val
                        elif algo == 1:
                            f_val = h_val + nodes.depth

                        if close_index == -1 and open_index == -1:  # if node not in open/closed lists
                            nodes.h_val = h_val
                            open_list.append(nodes)

                        elif open_index > -1:  # check for different Heuristic values
                            node_copy = open_list[open_index]
                            if f_val < node_copy.h_val:
                                node_copy.h_val = h_val
                                node_copy.parent = nodes.parent
                                node_copy.depth = nodes.depth

                        elif close_index > -1:  # add nodes in closed with lesser Heuristic value to open
                            node_copy = close_list[close_index]
                            if f_val < node_copy.h_val:
                                node_copy.h_val = h_val
                                close_list.remove(node_copy)
                                open_list.append(nodes)

                    close_list.append(curr_node)  # close the current node to

                    # sort based on f(n) value
                    if algo == 0:  # BFS
                        open_list = sorted(open_list, key=lambda p: p.h_val)
                    elif algo == 1:  # A*
                        open_list = sorted(open_list, key=lambda p: p.h_val + p.depth)
            else:
                return [0, 0]

    def print_solution_path(self, path_list, last):
        print("(", end=" ")
        for i in range(len(path_list)):
            for j in range(len(path_list[0])):
                print(path_list[i][j], end=" ")
        print(")", end=" ")
        if not last:
            print("--> ", end=" ")


if __name__ == "__main__":

    h_strings = ["Heuristic 1 - Number of misplaced Tiles", "Heuristic 2 - Manhattan Distance",
                 "Heuristic 3 - Maximum Matrix Distance"]
    algo_strings = ["BFS - Best First Search\n", "A* - A-star\n"]
    total_moves = 0
    path = []

    for algo in range(2):  # loop for 2 algorithms; 0 -> BFS and 1 -> A*
        avg_counts = [0, 0, 0]  # list for calculating average moves
        print(algo_strings[algo])
        for j in range(5):  # runs each algorithm for these 5 puzzles (initial states)
            if j == 0:
                initial_state = [[1, 2, 3, 4], [5, 7, 0, 8], [9, 6, 10, 12], [13, 14, 11, 15]]
            elif j == 1:
                initial_state = [[0, 1, 2, 4], [5, 7, 3, 8], [9, 6, 10, 12], [13, 14, 11, 15]]
            elif j == 2:
                initial_state = [[0, 1, 2, 4], [5, 7, 3, 8], [9, 6, 10, 12], [13, 14, 11, 15]]
            elif j == 3:
                initial_state = [[4, 2, 3, 1], [8, 6, 7, 5], [12, 10, 11, 9], [0, 14, 15, 13]]
            else:
                initial_state = [[1, 2, 3, 4], [5, 7, 8, 0], [9, 6, 10, 12], [13, 14, 11, 15]]

            puzzle = Puzzle()
            print("Puzzle", j + 1)
            puzzle.create_puzzle(initial_state)

            for h in range(3):  # runs each of 5 puzzles with 3 Heuristic functions
                print(h_strings[h])
                path, total_moves = puzzle.BFS_a_star(h, algo)  # algo = 0 (for BFS)
                # algo = 1 (for A*)
                if total_moves > 0:
                    print("Number of steps:", total_moves)
                    path.reverse()
                    last, count = 0, 0
                    for sp in path:
                        count += 1
                        if count == total_moves: last = 1
                        puzzle.print_solution_path(sp.node_data, last)
                    avg_counts[h] = avg_counts[h] + total_moves
                    print("\n")
                else:
                    print("Could not find solution\n")

        for c in range(3):  # print average moves for each Heuristic for both the algorithms
            print("Average steps: ", h_strings[c], ": ", avg_counts[c] / 5)
        print("\n")
