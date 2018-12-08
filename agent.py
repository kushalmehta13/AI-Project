import numpy as np
from utils import Directions
import util_functions as uf
import utils
import math
import util_functions
"""
Team Name: DCRAWLER
Team Member: Ajay Pal, Rohan Gujarathi, Kushal Mehta, Rishab Sachdeva
Class Name: DecrawlerAgent
"""
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


    def get_location(self, dir, location):
        """
        returns the location of the next tile in specified direction
        :param dir:  direction
        :param location: current location
        :return: tuple (x,y) - next tile location if agents moved in direction dir
        """
        dir_location = {utils.Directions.NORTH:(-1,0), utils.Directions.SOUTH:(1,0), utils.Directions.EAST:(0,1), utils.Directions.WEST:(0,-1)}

        x_incr, y_incr = dir_location[dir]
        new_loc = (location[0]+ x_incr, location[1]+y_incr)
        return new_loc

    def score(self, loc):
        """
        calculates score for each tile based on what is present on the tile.
        :param loc: location of the tile
        :return: integer specifiying the total strength gain/loss of the agent, if it was to step on the tile
        """
        return_value = 0
        # if there is an object in the specified location then calculate score of
        # the tile with respect to the object
        if loc in self.map_objects:
            obj = self.map_objects[loc]
            if isinstance(obj, utils.PowerUp):
                return_value =  obj.delta - utils.tile_cost[self.game_map[loc]]
            elif isinstance(obj, utils.StaticMonster):
                win_chance = (self.strength - utils.tile_cost[self.game_map[loc]])/((self.strength - utils.tile_cost[self.game_map[loc]]) + obj.strength)
                if(win_chance >= 0.5): # if win chance is 50% or more then the agent should fight
                    return_value = obj.strength - utils.tile_cost[self.game_map[loc]]
                else:
                    return_value = obj.delta - utils.tile_cost[self.game_map[loc]]
        # Else, the score will be the negative of the tile cost of the object
        else:
            return_value= -utils.tile_cost[self.game_map[loc]]

        return return_value

    def add_to_explored(self, location):
        """
        keeps track of visited tiles by maintaining the number of visit for the particular tile in explored dictionary
        :param location: current location in the form of integer tuple
        :return: Nothing
        """

        if location in self.explored:
            self.explored[location] += 1
        else:
            self.explored[location] = 1


    def get_movable(self):
        """
        This method finds which moves the agent can actually take from the current location and returns the possible direction
        in which agent can move

        :return: movable dictionary containing direction in which agent can travel with score value.
        """
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

    def decision_maker(self, movable):
        """

        :param movable: dictionary of possible moves along with score for each move
        :return: returns the best direction that is less visited and has highest score value.
        """
        movable_count = dict()

        # finding the count of each possible direction from the current location
        for dir in movable:
            new_loc = self.get_location(dir, self.location)
            if new_loc in self.explored:
                movable_count[dir] = self.explored[new_loc]
            else:
                movable_count[dir] = 0

        # finding the direction with minimum count
        dir = min(movable_count, key = lambda k : movable_count[k])
        min_count = movable_count[dir]
        less_explored = []

        # finding direction with same count as min count
        for move in movable_count:
            if movable_count[move] == min_count:
                less_explored.append(move)

        # finding the direction that has highest score among the minimum count locations.
        dir = max(less_explored, key = lambda k: movable[k])

        return dir

    def step(self, location, strength, game_map, map_objects):
        self.location = location
        self.strength = strength
        self.game_map = game_map

        # adding current locations to explored with count = 1
        self.add_to_explored(location)

        # finding the possible movable directions from current location
        movable = self.get_movable()

        # finding the best direction among the movable directions found above
        dir = self.decision_maker(movable)

        return dir