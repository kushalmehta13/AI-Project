import numpy as np
from utils import Directions
import util_functions as uf
import utils
import math


class BaseAgent(object):
    def __init__(self, height, width, initial_strength, name='base_agent'):
        """
        Base class for a game agent
        Parameters
        ----------
        height: int
            Height of the game map
        width: int
            Width of the game map
        initial_strength: int
            Initial strength of the agent
        name: str
            Name of the agent
        """
        self.height = height
        self.width = width
        self.initial_strength = initial_strength
        self.name = name

    def step(self, location, strength, game_map, map_objects):
        """
        Parameters
        ----------
        location: tuple of int
            Current location of the agent in the map
        strength: int
            Current strength of the agent
        game_map: numpy.ndarray
            Map of the game as observed by the agent so far
        map_objects: dict
            Objects discovered by the agent so far
        Returns
        -------
        direction: Directions
            Which direction to move
        """
        pass


class RandomAgent(BaseAgent):
    """
    A random agent that moves in each direction randomly
    Parameters
    ----------
    height: int
        Height of the game map
    width: int
        Width of the game map
    initial_strength: int
        Initial strength of the agent
    name: str
        Name of the agent
    """

    def __init__(self, height, width, initial_strength, name='random_agent'):
        super().__init__(height=height, width=width,
                         initial_strength=initial_strength, name=name)

    def step(self, location, strength, game_map, map_objects):
        """
        Implementation of a random agent that at each step randomly moves in
        one of the four directions
        Parameters
        ----------
        location: tuple of int
            Current location of the agent in the map
        strength: int
            Current strength of the agent
        game_map: numpy.ndarray
            Map of the game as observed by the agent so far
        map_objects: dict
            Objects discovered by the agent so far
        Returns
        -------
        direction: Directions
            Which direction to move
        """
        return np.random.choice(list(Directions))


class HumanAgent(BaseAgent):
    """
    A human agent that that can be controlled by the user. At each time step
    the agent will prompt for an input from the user.
    Parameters
    ----------
    height: int
        Height of the game map
    width: int
        Width of the game map
    initial_strength: int
        Initial strength of the agent
    name: str
        Name of the agent
    """

    def __init__(self, height, width, initial_strength, name='human_agent'):
        super().__init__(height=height, width=width,
                         initial_strength=initial_strength, name=name)

    def step(self, location, strength, game_map, map_objects):
        """
        Implementation of an agent that at each step asks the user
        what to do
        Parameters
        ----------
        location: tuple of int
            Current location of the agent in the map
        strength: int
            Current strength of the agent
        game_map: numpy.ndarray
            Map of the game as observed by the agent so far
        map_objects: dict
            Objects discovered by the agent so far
        Returns
        -------
        direction: Directions
            Which direction to move
        """
        dir_dict = {'N': Directions.NORTH,
                    'S': Directions.SOUTH,
                    'W': Directions.WEST,
                    'E': Directions.EAST}

        dirchar = ''
        while not dirchar in ['N', 'S', 'W', 'E']:
            dirchar = input("Please enter a direction (N/S/E/W): ").upper()

        return dir_dict[dirchar]


class DcrawlerAgent(BaseAgent):
    """
   A Dcrawler agent that moves in each direction based on score value of each options
   ----------
   height: int
       Height of the game map
   width: int
       Width of the game map
   initial_strength: int
       Initial strength of the agent
   name: str
       Name of the agent
   """

def __init__(self, height, width, initial_strength, name='decrawler_agent'):
    super().__init__(height=height, width=width,initial_strength=initial_strength, name=name)
    self.location = tuple() # for storing the current location
    self.game_map = None #for storing the game map
    self.map_objects = dict() # for keeping track of map_objects
    self.explored = dict() # for keeping track of explored states
    self.bufferd_steps = [] #
    self.iterator = 0


def getLocation(self, dir, location):
    dir_location = {utils.Directions.NORTH:(-1,0), utils.Directions.SOUTH:(1,0), utils.Directions.EAST:(0,1), utils.Directions.WEST:(0,-1)}
    x_add, y_add = dir_location[dir]
    new_loc = (location[0]+ x_add, location[1]+y_add)
    return new_loc


def reachDestination(self, start, destination):
    map_mat = []

    for i in range(len(self.game_map)):
        map_mat.append([])
        for j in range(len(self.game_map[i])):
            if self.game_map[i][j] != utils.MapTiles.W and  self.game_map[i][j] != utils.MapTiles.U:
                map_mat[i].append(-self.score((i,j)))
            else:
                map_mat[i].append(math.inf)

    #bufferd_steps = astar.solve(start, destination, map_mat)

def score(self, loc):
    """
    returns the final deduction or addition in the agents strength after moving to the tile
    :param loc:
    :return:
    """
    return_value = 0
    #tc = self.game_map[loc]

    if loc in self.map_objects:
        obj = self.map_objects[loc]
        if isinstance(obj, utils.PowerUp):
            return_value =  obj.delta - utils.tile_cost[self.game_map[loc]]
        elif isinstance(obj, utils.StaticMonster):
            win_chance = (self.strength - utils.tile_cost[self.game_map[loc]])/((self.strength - utils.tile_cost[self.game_map[loc]]) + obj.strength)
            if(win_chance >= 0.5):
                return_value = obj.strength - utils.tile_cost[self.game_map[loc]]

            else:
                return_value = obj.delta - utils.tile_cost[self.game_map[loc]]
    else:
        return_value= -utils.tile_cost[self.game_map[loc]]
    return return_value

def add_to_explored(self, location):
    if location in self.explored:
        self.explored[location] += 1
    else:
        self.explored[location] = 1

def get_movable(self):
    '''
    location: tuple <int, int>
    game_map: dict <map: value>
    Returns: dict <direction (string) : location>
    '''
    x = self.location[0]
    y = self.location[1]
    movable = dict()
    maxlen = len(self.game_map)
    # North Neighbor
    if x-1 >= 0 and self.game_map[x-1][y] != utils.MapTiles.W:
        loc = (x-1, y)
        movable[utils.Directions.N] = self.score(loc)
    # East Neighbor
    if y+1 <= maxlen - 1 and self.game_map[x][y+1] != utils.MapTiles.W:
        loc = (x, y+1)
        movable[utils.Directions.E] = self.score(loc)
    # South Neighbor
    if x+1 <= maxlen - 1 and self.game_map[x+1][y] != utils.MapTiles.W:
        loc = (x+1, y)
        movable[utils.Directions.S] = self.score(loc)
    # West Neighbor
    if y-1 >= 0 and self.game_map[x][y-1] != utils.MapTiles.W:
        loc = (x, y-1)
        movable[utils.Directions.W] = self.score(loc)

    return movable

def decisionMaker(self, movable):
    movable_count = dict()

    #finding the count of each movable
    for dir in movable:
        new_loc = self.getLocation(dir, self.location)
        if new_loc in self.explored:
            movable_count[dir] = self.explored[new_loc]
        else:
            movable_count[dir] = 0

    dir = min(movable_count, key = lambda k : movable_count[k])
    min_count = movable_count[dir]
    less_explored = []

    #finding min count
    for move in movable_count:
        if movable_count[move] == min_count:
            less_explored.append(move)

    #print("less Explored", less_explored)
    #print("movable", movable)
    #finding best score for the same count:
    dir = max(less_explored, key = lambda k: movable[k])

    return dir

def step(self, location, strength, game_map, map_objects):
    self.location = location
    self.strength = strength
    self.game_map = game_map
    self.map_objects = {**self.map_objects, **map_objects} #for storing all the objects seen so far
    #print(map_objects)
    movable = self.get_movable()
    self.add_to_explored(location)
    dir = self.decisionMaker(movable)
    new_loc = self.getLocation(dir, location)
    if new_loc in map_objects:
        del self.map_objects[new_loc]

    return dir
    """
    Implementation of a random agent that at each step randomly moves in
    one of the four directions

    Parameters
    ----------
    location: tuple of int
        Current location of the agent in the map
    strength: int
        Current strength of the agent
    game_map: numpy.ndarray
        Map of the game as observed by the agent so far
    map_objects: dict
        Objects discovered by the agent so far

    Returns
    -------
    direction: Directions
        Which direction to move
    """
    # solve(location, )

    # return np.random.choice(list(Directions))