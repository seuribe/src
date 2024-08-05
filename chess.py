from typing import List
from enum import Enum
from dataclasses import dataclass

EMPTY  = 0

class Color(Enum):
    White = 0
    Black = 7
    def other(self):
        return self.Black if self == self.White else self.White

class Piece(Enum):
    Empty  = 0
    Pawn   = 1
    Bishop = 2
    Knight = 3
    Rook   = 4
    Queen  = 5
    King   = 6

@dataclass
class Position:
    row: int
    col: int
    def above(self):
        return Position(row=self.row-1, col=self.col)

    def below(self):
        return Position(row=self.row+1, col=self.col)

    def left(self):
        return Position(row=self.row, col=self.col-1)

    def right(self):
        return Position(row=self.row, col=self.col+1)
    
    def __hash__(self):
        return hash((self.row, self.col))

@dataclass
class BoardPiece:
    piece: Piece
    color: Color
    pos: Position

    def pawnAdvance(self):
        return self.pos.above() if self.color == Color.White else self.pos.below()
    def pawnEatMoves(self):
        advance = self.pawnAdvance()
        return [advance.left(), advance.right()]
    def rookMoveFunctions(self):
        return [lambda x:x.left(), lambda x:x.right(), lambda x:x.above(), lambda x:x.below()]

@dataclass
class Move:
    orig:Position
    dest:Position

class Board:
    pieces: List[BoardPiece] = []

    def __init__(self, size:int):
        self.size = size
        self.clear() # initialize board and pieces

    def clear(self):
        self.board = [[EMPTY] * self.size for _ in range(self.size)]
        self.pieces = []

    def get(self, pos:Position):
        return self.board[pos.row][pos.col]

    def add(self, piece:Piece, color:Color, pos:Position):
        bp = BoardPiece(piece, color, pos)
        self.addPiece(bp)

    def addPiece(self, piece:BoardPiece):
        if piece in self.pieces:
            raise Exception(f"Piece {piece} already in board")
        self.pieces.append(piece)
        self.board[piece.pos.row][piece.pos.col] = piece
        # keep pieces always sorted
        self.pieces.sort(key=lambda p:p.piece.value * 1000 + p.color.value * 100 + p.pos.row * 10 + p.pos.col)

    def isEmpty(self, pos:Position):
        return self.get(pos) == EMPTY

    def remove(self, pos:Position):
        piece = self.get(pos)
        if piece:
            self.pieces.remove(piece)
            self.board[piece.pos.row][piece.pos.col] = EMPTY

    def move(self, move:Move):
        """ Will remove any piece at the destination, WITHOUT checking if the move or eat is valid """
        bPiece = self.get(move.orig)
        if not bPiece:
            return
        self.remove(move.orig)
        self.remove(move.dest)
        self.add(bPiece.piece, bPiece.color, move.dest)


    def getKing(self, color:Color):
        """ returns None if there is no king of that color """
        for bp in self.pieces:
            if bp.piece is Piece.King and bp.color is color:
                return bp
        return None


    def validPos(self, pos:Position):
        return 0 <= pos.row < self.size and 0 <= pos.col < self.size


    def __str__(self):
        PIECES = "·♙♗♘♖♕♔·♟♝♞♜♛♚"
        str = "+----+\n"
        for row in self.board:
            str = str + "|"
            for piece in row:
                index = 0 if piece == 0 else piece.piece.value + piece.color.value
                str = str + PIECES[index]
            str = str + "|\n"
        str = str + "+----+"
        return str


    def validDest(self, pos:Position):
        """ Is 'pos' a square where a piece can move to? (valid and empty) """
        return self.validPos(pos) and self.isEmpty(pos)


    def validEat(self, pos:Position, piece:BoardPiece):
        """ Is there a piece at 'pos', that 'piece' can eat? """
        return self.validPos(pos) and not self.isEmpty(pos) and self.get(pos).color != piece.color and self.get(pos).piece != Piece.King


    def hasPiece(self, pos:Position):
        """ Is there _any_ piece in this pos? """
        return self.validPos(pos) and not self.isEmpty(pos)
    

    def validSurroundings(self, pos:Position):
        ab = pos.above()
        be = pos.below()
        potential = [ab.left(), ab, ab.right(),
                    pos.left(),    pos.right(),
                     be.left(), be, be.right()]

        return list(filter(self.validPos, potential))
  

    def isThreatened(self, pos:Position, color:Color):
        """ Is this position threatened by a piece of color 'color'? """

        # Check pawns
        pawnPreviousRow = pos.below() if color == Color.White else pos.above()
        for pp in [pawnPreviousRow.left(), pawnPreviousRow.right()]:
            if self.validPos(pp):
                bp = self.get(pp)
                if bp and bp.piece is Piece.Pawn and bp.color is color:
                    return True

        # Check Rooks
        for moveFunction in [lambda x:x.left(), lambda x:x.right(), lambda x:x.above(), lambda x:x.below()]:
            current = moveFunction(pos)
            while self.validPos(current) and self.isEmpty(current):
                current = moveFunction(current)

            if self.validPos(current):
                bp = self.get(current)
                if bp and bp.piece is Piece.Rook and bp.color is color:
                    return True

        # Check King
        for c in self.validSurroundings(pos):
            bp = self.get(c)
            if bp and bp.piece is Piece.King and bp.color is color:
                return True

        return False
        


    def possibleMoves(self, piece:BoardPiece):
        """ Where could the piece at 'pos' move to?
            In the case of a king, it will only return squares
            that are not threatened by the other color
            """
        moves = []
        match piece.piece:
            case Piece.Pawn: # Pawn
                advance = piece.pawnAdvance()
                if (self.validDest(advance)):
                    moves.append(advance)

                for eat_move in piece.pawnEatMoves():
                    if self.validEat(eat_move, piece):
                        moves.append(eat_move)

            case Piece.Rook: # Rook
                for moveFunction in piece.rookMoveFunctions():
                    current = moveFunction(piece.pos)
                    # move
                    while self.validDest(current):
                        moves.append(current)
                        current = moveFunction(current)

                    # eat
                    if self.validEat(current, piece):
                        moves.append(current)

            case Piece.King: # King
                # Temporarily remove the king from its current position so that it doesn't block potential threats
                self.remove(piece.pos)

                potential = self.validSurroundings(piece.pos)
                for c in potential:
                    if not self.isThreatened(c, piece.color.other()) and (self.validEat(c, piece) or self.validDest(c)):
                        moves.append(c)

                # Restore the king to is position
                self.addPiece(piece)

        # Create proper Move from the resulting posinates
        return list(map(lambda m: Move(piece.pos, m), moves))


    def allPiecesFrom(self, color:Color) -> List[BoardPiece]:
        return [p for p in self.pieces if p.color is color]


    def isCheckMated(self, color:Color) -> bool:
        king = self.getKing(color)
        return king is not None and self.isThreatened(king.pos, king.color.other()) and not self.possibleMoves(king)


    def isChecked(self, color:Color):
        return self.isKingChecked(self.getKing(color))


    def isKingChecked(self, king:BoardPiece):
        return king is not None and self.isThreatened(king.pos, king.color.other()) 


    def getAllMovesFor(self, color:Color):
        moves = []
        for piece in self.allPiecesFrom(color):
            moves = moves + self.possibleMoves(piece)

        # Return only moves where the king is not checked
        validMoves = []
        for move in moves:
            b = self.cloneMove(move)
            if not b.isChecked(color):
                validMoves.append(move)

        return validMoves


    def clone(self):
        """ Return a clone of the board """
        newBoard = Board(self.size)
        for piece in self.pieces:
            np = BoardPiece(piece.piece, piece.color, piece.pos)
            newBoard.addPiece(np)

        return newBoard


    def cloneMove(self, move:Move):
        """ Return a clone of the board where the move 'move' has been played """
        newBoard = self.clone()
        newBoard.move(move)
        return newBoard
