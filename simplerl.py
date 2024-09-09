from copy import deepcopy
from typing import List, Dict, Tuple
from dataclasses import dataclass
from rl import *


@dataclass
class Direction(Enum):
    """ Simple representation of a direction for movement in the grid """
    Up = (0, -1)
    Down = (0, 1)
    Left = (-1, 0)
    Right = (1, 0)

    def __hash__(self):
        return hash((self.value[0], self.value[1]))

    def __str__(self):
        return f"{(self.value[0], self.value[1])}"

    def __repr__(self):
        return self.__str__()

@dataclass
class Position:
    """ A position in the grid. x is the column and y the row """
    x:int
    y:int

    def move(self, dir:Direction):
        """ returns a new position moved in the direction """
        return Position(self.x + dir.value[0], self.y + dir.value[1])

    def allMoves(self):
        poss = []
        for dir in Direction:
            poss.append(self.move(dir))
        return poss

    def __hash__(self):
        return hash((self.x, self.y))

class Grid:
    """ The maze is represented by this grid, itself containing a two-dimensional array of ints """
    EMPTY = 0
    WALL = 1
    START = 2
    END = 3

    gridData:List[List[int]]
    def __init__(self, data):
        self.gridData = deepcopy(data)

    def isWall(self, pos:Position):
        """ is there a wall a this position? """
        return self.gridData[pos.y][pos.x] is self.WALL

    def get(self, pos:Position):
        """ what is there at this position? """
        return self.gridData[pos.y][pos.x]

    def validPos(self, pos:Position):
        """ is the position valid? we don't want to walk over walls or outside of the maze """
        return 0 <= pos.y < len(self.gridData) and 0 <= pos.x < len(self.gridData[pos.y]) and not self.isWall(pos)

    def findFirst(self, key:int) -> Position:
        y = 0
        for row in self.gridData:
            x = 0
            for cell in row:
                if cell == key:
                    return Position(x, y)
                x = x + 1
            y = y + 1
        return None


@dataclass
class GridAction(Action):
    dir:Direction

    def __hash__(self):
        return hash(self.dir)

    def __str__(self):
        return f"{self.dir}"

    def __repr__(self):
        return self.__str__()


@dataclass
class GridState(State):
    pos:Position

    def __init__(self, pos:Position):
        self.pos = pos

    def __hash__(self):
        return hash(self.pos)


class GridEnvironment(Environment):
    state:GridState
    grid:Grid

    def __init__(self, grid:Grid, startPosition:Position, endPosition:Position):
        self.grid = grid
        self.startPosition = startPosition
        self.endPosition = endPosition
        self.state = GridState(self.startPosition)

    def isWinState(self):
        return self.state.pos == self.endPosition

    def isValidMove(self, dir:Direction):
        next = self.state.pos.move(dir)
        return self.grid.validPos(next) and not self.grid.isWall(next)

    def getAllPossibleActions(self) -> List[Action]:
        actions = []
        for d in Direction:
            if self.isValidMove(d):
                actions.append(GridAction(d))
        return actions

    def getNewState(self, action:GridAction) -> GridState:
        if not self.isValidMove(action.dir):
            raise Exception(f"Invalid action {action.dir} from {self.state.pos}")

        newPos = self.state.pos.move(action.dir)
        return GridState(newPos)

DEFAULT_MAZE = [[0,0,0,1,0,0,1,0],
                [0,1,1,1,0,0,0,0],
                [0,1,0,1,0,1,1,1],
                [0,0,0,1,0,0,1,0],
                [0,1,1,1,1,0,1,0],
                [0,0,0,1,0,0,1,0],
                [0,1,0,0,0,1,1,0],
                [0,1,0,1,0,0,0,0],
                ]

DEFAULT_START = Position(0,0)
DEFAULT_END = Position(5, 0)
