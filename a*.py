'''
Code by - Kushal Samir Mehta

References:
    1. https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
'''



import heapq

class Node():
    '''
    Contains the information for every position in the the matrix
    '''

    def __init__(self, parent=None, position=None):
        '''

        :param parent: Parent of the current node
        :param position: (x, y) in a 2D matrix
        '''
        self.parent = parent
        self.location = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        '''

        :param other: Other node to be compared with
        :return: True or False. (True if location of both the nodes are same, False otherwise)
        '''
        return self.location == other.location

    def __lt__(self, other):
        '''

        :param other: Other node to compare with
        :return: True or False. (True if the f value of current node is smaller than the other node, False otherwise
        '''
        return self.f < other.f


def manhattan_distance(x,y):
    '''

    :param x: (Integer, Integer). Location of the agent
    :param y: (Integer, Integer). Location of the goal state
    :return: Manhattan distance between the location of the agent and the goal
    '''
    return abs(x[0] - y[0]) + abs(x[1] - y[1])


def get_relative_neighbors():
    '''

    :return: List of tuples. Tuples contain all possible values that can be used to generate children
    '''
    return [(0,1),(1,0),(0,-1),(-1,0)]


def distance_matrixify(mat):
    '''

    :param mat: 2D list. Eg: [[p, p, p], [p, m ,p], [s, s, m]]
    :return: A 2D list populated with the corresponding path cost
    '''
    for i in range(len(mat)):
        for j in range(len(mat)):
            if mat[i][j] == 'p':
                mat[i][j] = 10
            elif mat[i][j] == 'm':
                mat[i][j] = 100
            elif mat[i][j] == 's':
                mat[i][j] = 30
    return mat


def getCost(path, d_matrix):
    '''

    :param path: List of tuples. Tuples describe the location of the agent.
    :param d_matrix: cost matrix (2D list)
    :return: Total cost of a path taken to reach the goal
    '''
    cost = 0
    for i in path[1:]:
        cost += d_matrix[i[0]][i[1]]
    return cost


def calculateDirections(path):
    '''

    :param path: List of tuples that represent the path taken to reach the goal by the agent
    :return: String the depicts the direction the agent has to go in at each step to reach the goal
    '''
    d = []
    for i, j in zip(path, path[1:]):
        if i[0] == j[0]:
            if i[1] < j[1]:
                d.append('E')
            else:
                d.append('W')
        else:
            if i[0] < j[0]:
                d.append('S')
            else:
                d.append('N')
    return ''.join(d)


def set_ghf(child, goal, d_matrix,n):
    '''

    :param child: Node containing information of the child for which the cost needs to be calculated
    :param goal: Node containing information of the goal state
    :param d_matrix: 2D list that contains the cost for each terrain
    :param n: Current node that has been popped off the frontier
    :return: None
    '''
    child.g = d_matrix[child.location[0]][child.location[1]] + n[1].g
    child.h = manhattan_distance(child.location, goal)
    child.f = child.g + child.h

def backtrack(n, d_matrix):
    '''

    :param n: Current node that has been popped off the frontier
    :param d_matrix: 2D list that contains the cost for each terrain
    :return: Direction of the path that has been taken
    '''
    path = []
    temp = n[1]
    while temp is not None:
        path.append(temp.location)
        temp = temp.parent
    # cost = getCost(path[::-1], d_matrix)
    directions = calculateDirections(path[::-1])
    return directions

def solve(start, goal, mat):
    '''

    :param start: Tuple that has the location of the start state
    :param goal: Tuple that has the location of the goal state
    :param mat: Matrix that represents the
    :return:
    '''

    if start[0] > -1 and start[0] < len(mat) and goal[0] > -1 and goal [0] < len(mat) and start[1] > -1 and start[1] < len(mat) and goal[1] > -1 and goal[1] < len(mat):
        # Replace the matrix in place with the corresponding path costs
        d_matrix = distance_matrixify(mat)

        # Initialize start node
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0

        # Initialize goal node (End node)
        end_node = Node(Node, goal)
        end_node.g = d_matrix[goal[0]][goal[1]]
        end_node.h = 0
        end_node.f = end_node.g + end_node.h

        # Define frontier as a priority queue
        frontier = []
        heapq.heapify(frontier)

        # Define interior as a set
        interior = set()

        # Push start node into the frontier
        heapq.heappush(frontier, (start_node.f, start_node))
        direction = ''
        cost = 0

        while len(frontier) > 0:
            # Get node with smallest cost from frontier and push it to interior
            n = heapq.heappop(frontier)
            interior.add(n[1].location)

            # Check if current node is goal node
            if n[1] == end_node:
                direction = backtrack(n, d_matrix)
                return direction

            # Calculate the locations of the neighbors / children of the current node
            c = list()
            relative_neighbors = get_relative_neighbors()
            for rel_loc in relative_neighbors:
                possible_pos = (n[1].location[0] + rel_loc[0], n[1].location[1] + rel_loc[1])
                if possible_pos[0] not in range(len(mat)) or possible_pos[1] not in range(len(mat[0])):
                    continue
                new_node = Node(n[1], possible_pos)
                c.append(new_node)


            for child in c:
                flag = 0
                # If child is visited then move on to the next child
                if child.location in interior:
                    continue

                # Set the path cost, heuristic and the total cost f for the child
                set_ghf(child,goal,d_matrix,n)

                # if child location is in the frontier and if its cost is lower than the one in the frontier,
                # replace the frontier node with the current child
                for untraversed in frontier:
                    if child.location == untraversed[1].location:
                        if child.f < untraversed[1].f:
                            frontier.remove(untraversed)
                        else:
                            flag = 1
                if flag == 1:
                    continue

                heapq.heappush(frontier, (child.f, child))
    return ''


def main():
   x = solve((1, 0),(2, 2),[['p','p','p'],['p','m','p'],['s','s','s']])
   print(x)

if __name__ == '__main__':
    main()