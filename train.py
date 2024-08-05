import random

from chess import Color, Piece, BoardPiece, Board, Move, Position
import rl

WHITE_PAWN_POS = Position(3,3)
WHITE_ROOK_POS = Position(3,1)
BLACK_PAWN_POS = Position(1,3)
BLACK_KING_POS = Position(0,3)

board = Board(4)
whitePawn = BoardPiece(Piece.Pawn, Color.White, WHITE_PAWN_POS)
whiteRook = BoardPiece(Piece.Rook, Color.White, WHITE_ROOK_POS)
blackPawn = BoardPiece(Piece.Pawn, Color.Black, BLACK_PAWN_POS)
blackKing = BoardPiece(Piece.King, Color.Black, BLACK_KING_POS)
board.addPiece(whitePawn)
board.addPiece(whiteRook)
board.addPiece(blackPawn)
board.addPiece(blackKing)
print(board)

env = rl.Environment(board)

qLearning = rl.QLearning()
episode = rl.Episode(env, qLearning, 0.5)

def onStepEnd():
    """ Black plays a random (valid) move """
    actions = env.getAllPossibleActions(Color.Black)
    if actions:
        env.execute(random.choice(actions))


steps = episode.step(100, onStepEnd=onStepEnd)
print(f"Board state after {steps} steps:")
print(board)
print(f"End State: {env.isEndState()}")
print(f"Black checkmated: {board.isCheckMated(Color.Black)}")
print(f"Number of states: {len(qLearning.sas)}")
