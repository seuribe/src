from copy import deepcopy
from typing import List, Dict, Tuple
from dataclasses import dataclass
from rl import *


@dataclass
class Direction(Enum):
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
    EMPTY = 0
    WALL = 1
    START = 2
    END = 3

    gridData:List[List[int]]
    def __init__(self, data):
        self.gridData = deepcopy(data)

    def isWall(self, pos:Position):
        return self.gridData[pos.y][pos.x] is self.WALL

    def get(self, pos:Position):
        return self.gridData[pos.y][pos.x]

    def validPos(self, pos:Position):
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
    playerPos:Position

    def __init__(self, playerPos:Position):
        self.playerPos = playerPos

    def __hash__(self):
        return hash(self.playerPos)


class GridEnvironment(Environment):
    state:GridState
    grid:Grid

    def __init__(self, grid:Grid):
        self.grid = grid
        self.startPosition = self.grid.findFirst(Grid.START)
        self.endPosition = self.grid.findFirst(Grid.END)
        self.state = GridState(self.startPosition)

    def isWinState(self):
        return self.state.playerPos == self.endPosition

    def isValidMove(self, dir:Direction):
        next = self.state.playerPos.move(dir)
        return self.grid.validPos(next) and not self.grid.isWall(next)

    def getAllPossibleActions(self) -> List[Action]:
        actions = []
        for d in Direction:
            if self.isValidMove(d):
                actions.append(GridAction(d))
        return actions

    def getNewState(self, action:GridAction) -> GridState:
        if not self.isValidMove(action.dir):
            raise Exception(f"Invalid action {action.dir} from {self.state.playerPos}")

        newPos = self.state.playerPos.move(action.dir)
        return GridState(newPos)