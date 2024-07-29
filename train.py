import random

import chess
import rl

WHITE_PAWN_POS = (3,3)
WHITE_ROOK_POS = (3,1)
BLACK_PAWN_POS = (1,3)
BLACK_KING_POS = (0,3)

board = chess.Board(4)
board.set(WHITE_PAWN_POS, chess.Piece(chess.PAWN, chess.WHITE))
board.set(WHITE_ROOK_POS, chess.Piece(chess.ROOK, chess.WHITE))
board.set(BLACK_PAWN_POS, chess.Piece(chess.PAWN, chess.BLACK))
board.set(BLACK_KING_POS, chess.Piece(chess.KING, chess.BLACK))
board.print()

nb = board.clone()
nb.print()

print(list(board.allPiecesFrom(chess.WHITE)))
print(list(board.allPiecesFrom(chess.BLACK)))
print(f"Possible moves for the white pawn: {list(board.possibleMoves(WHITE_PAWN_POS))}")
print(f"Possible moves for the black pawn: {list(board.possibleMoves(BLACK_PAWN_POS))}")

env = rl.Environment(board)

print(f"All possible current moves for white: {list(env.getAllPossibleActions())}")


n = 20
color = chess.WHITE
while not env.isEndState() and n > 0:
    moves = env.getAllPossibleActions(color)
    if moves:
        move = random.choice(moves)
        print (move)
        board.move(move)
        board.print()
    color = chess.otherColor(color)
    n = n - 1
