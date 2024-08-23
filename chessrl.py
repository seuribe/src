from dataclasses import dataclass
from chess import *
from rl import *

def encodeMove(move:Move):
    return move.orig.row  + (move.orig.col << 4) + (move.dest.row << 8) + (move.dest.col << 16)

def encodePiece(piece:BoardPiece):
    return piece.piece.value + (piece.color.value << 8) + (piece.pos.row << 16) + (piece.pos.col << 24)

def encodeBoard(board:Board):
    data = []
    for piece in board.pieces:
        data.append(encodePiece(piece))
    return data


@dataclass
class BoardAction:
    move:Move
    def __init__(self, move:Move):
        self.move = move
        self.encoding = encodeMove(self.move)

    def __hash__(self):
        return hash((self.move.orig, self.move.dest))


@dataclass
class BoardState(State):
    board:Board
    encoding:List[int]
    boardHash:int

    def __init__(self, board:Board):
        self.board = board.clone()
        self.encoding = encodeBoard(self.board)
        self.boardHash = 0

    def __hash__(self):
        return self.boardHash

    def isEnd(self):
        return self.isWin() or self.isLose()

    def isWin(self):
        return self.board.isCheckMated(Color.Black)

    def isLose(self):
        return not self.getAllPossibleActions()

    def isTie(self):
        ## TODO: implement stalemate
        return False

    def getAllPossibleActionsFor(self, color:Color = Color.White) -> List[Action]:
        allMoves = self.board.getAllMovesFor(color)
        # map each move to an action
        return list(map(lambda m:BoardAction(move=m), allMoves))

    def getAllPossibleActions(self) -> List[Action]:
        return self.getAllPossibleActionsFor(Color.White)


class ChessEnvironment(Environment):
    state:BoardState

    def doExecute(self, action:BoardAction):
        newBoard = self.state.board.cloneMove(action.move)
        self.state = BoardState(newBoard)
