import random

from chess import Color, Piece, BoardPiece, Board, Move, Position
#import rl

WHITE_PAWN_POS = Position(3,3)
WHITE_ROOK_POS = Position(3,1)
BLACK_PAWN_POS = Position(1,3)
BLACK_KING_POS = Position(0,3)

board = Board(4)
whitePawn = BoardPiece(Piece.Pawn, Color.White, WHITE_PAWN_POS)
whiteRook = BoardPiece(Piece.Rook, Color.White, WHITE_ROOK_POS)
blackPawn = BoardPiece(Piece.Pawn, Color.Black, BLACK_PAWN_POS)
blackKing = BoardPiece(Piece.King, Color.Black, BLACK_KING_POS)
board.add(whitePawn)
board.add(whiteRook)
board.add(blackPawn)
board.add(blackKing)
print(board)

nb = board.clone()
print(nb)

print(f"All white pieces: {board.allPiecesFrom(Color.White)}")
print(f"All black pieces: {board.allPiecesFrom(Color.Black)}")

print(f"Possible moves for the white pawn: {list(board.possibleMoves(whitePawn))}")
print(f"Possible moves for the black pawn: {list(board.possibleMoves(blackPawn))}")

exit()



env = rl.Environment(board)

print(f"All possible current moves for white: {list(env.getAllPossibleActions())}")
