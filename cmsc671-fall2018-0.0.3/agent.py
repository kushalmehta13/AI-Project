import numpy as np
from utils import Directions, MapTiles, MapObject
# import MEHTA_hw4

class BaseAgent(object):
    def __init__(self, name='base_agent'):
        """

        Parameters
        ----------
        name: str
            Name of the agent
        """
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
    def __init__(self, name='random_agent'):
        return super().__init__(name=name)

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

class Dcrawler(BaseAgent):
    location = tuple()
    strength = int()
    game_map = dict()
    map_objects = dict()
    def __init__(self, name='dcrawler'):
        location = tuple()
        return super().__init__(name=name)

    def chooseBestTile(self, moavable):
        return np.random.choice(list(movable.keys()))

    def get_surroundings(self):
        '''
        location: tuple <int, int>
        game_map: dict <map: value>
        Returns: dict <direction (string) : location>
        '''
        x = self.location[0]
        y = self.location[1]
        movable = {}
        maxlen = len(self.game_map)
        # North Neighbor
        if x-1 >= 0 and self.game_map[x-1][y] != MapTiles.W:
            if (x-1, y) in self.map_objects:
                movable[Directions.N] = (self.game_map[x-1][y], self.map_objects[(x-1, y)])
            else:
                movable[Directions.N] = (self.game_map[x-1][y], None])
        # East Neighbor
        if y+1 <= maxlen - 1 and self.game_map[x][y+1] != MapTiles.W:
            if (x, y+1) in self.map_objects:
                movable[Directions.E] = (self.game_map[x][y+1], self.map_objects[(x, y+1)])
            else:
                movable[Directions.E] = (self.game_map[x][y+1], None)
        # South Neighbor
        if x+1 <= maxlen - 1 and self.game_map[x+1][y] != MapTiles.W:
            if (x+1, y) in self.map_objects:
                movable[Directions.S] = (self.game_map[x+1][y], self.map_objects[(x+1, y)])
            else:
                movable[Directions.S] = (self.game_map[x+1][y], None)
        # West Neighbor
        if y-1 >= 0 and self.game_map[x][y-1] != MapTiles.W:
            if (x, y+1) in self.map_objects:
                movable[Directions.W] = (game_map[x][y-1], self.map_objects[(x, y-1)])
            else:
                movable[Directions.W] = (game_map[x][y-1], None)

        return moavable


    def step(self, location, strength, game_map, map_objects):
        self.location = location
        self.strength = strength
        self.game_map = game_map
        self.map_objects = map_objects

        movable = self.get_surroundings()
        return self.chooseBestTile(movable)
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
