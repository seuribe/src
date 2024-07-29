EMPTY  = 0
PAWN   = 1
BISHOP = 2
KNIGHT = 3
ROOK   = 4
QUEEN  = 5
KING   = 6

WHITE  = 0
BLACK  = 7

def otherColor(color):
    return BLACK if color == WHITE else WHITE

def pieceStr(piece):
    return ["(none)", "Pawn", "Bishop", "Knight", "Rook", "Queen", "King"][piece]

def colorStr(color):
    return "White" if color == WHITE else "Black"

class Piece:
    def __init__(self, piece, color):
        self.piece = piece
        self.color = color

    def isA(self, piece, color):
        return self.piece == piece and self.color == color
    
    def __str__(self):
        return f"{colorStr(self.color)} {pieceStr(self.piece)}"
    def __repr__(self):
        return self.__str__()    

def above(pos):
    return (pos[0]-1, pos[1])

def below(pos):
    return (pos[0]+1, pos[1])

def left(pos):
    return (pos[0], pos[1]-1)

def right(pos):
    return (pos[0], pos[1]+1)

class Board:
    def __init__(self, size):
        self.size = size
        self.board = [[EMPTY] * self.size for _ in range(self.size)]
        self.clear()

    def set(self, pos, piece):
        self.board[pos[0]][pos[1]] = piece

    def get(self, pos):
        return self.board[pos[0]][pos[1]]

    def move(self, move):
        piece = self.board[move._from[0]][move._from[1]]
        self.board[move._from[0]][move._from[1]] = EMPTY
        self.board[move._to[0]][move._to[1]] = piece

    def find(self, piece):
        rowIndex = 0
        for row in self.board:
            colIndex = 0
            for square in row:
                c = (rowIndex, colIndex)
                if self.hasPiece(c) and piece.isA(square.piece, square.color):
                    return (rowIndex, colIndex)
                colIndex = colIndex + 1
            rowIndex = rowIndex + 1

    def clear(self):
        self.board = [[EMPTY] * self.size for _ in range(self.size)]

    def validPos(self, pos):
        return type(pos) is tuple and len(pos) == 2 and pos[0] >= 0 and pos[0] < self.size and pos[1] >= 0 and pos[1] < self.size

    def isEmpty(self, pos):
        return self.get(pos) == EMPTY

    def print(self):
        PIECES = "·♙♗♘♖♕♔·♟♝♞♜♛♚"
        print("+----+")
        for row in self.board:
            print("|", end='')
            for piece in row:
                index = 0 if piece == 0 else piece.piece
                print(PIECES[index], end='')
            print("|")
        print("+----+")

    def validDest(self, pos):
        """ Is 'pos' a square where a piece can move to? (valid and empty) """
        return self.validPos(pos) and self.isEmpty(pos)

    def validEat(self, pos, piece):
        """ Is there a piece at 'pos', that 'piece' can eat? """
        return self.validPos(pos) and not self.isEmpty(pos) and self.get(pos).color != piece.color and self.get(pos).piece != KING

    def hasPiece(self, pos):
        """ Is there _any_ piece in this pos? """
        return self.validPos(pos) and not self.isEmpty(pos)
    
    def validSurroundings(self, pos):
        potential = [left(above(pos)), above(pos), right(above(pos)),
                     left(pos),                             right(pos),
                     left(below(pos)), below(pos), right(below(pos))]

        return list(filter(self.validPos, potential))
  
    def isThreatened(self, pos, color):
        """ Is this posinate threatened by a piece of color 'color'? """

        # Check pawns
        pawnPreviousRow = below(pos) if color == WHITE else above(pos)
        for pp in [left(pawnPreviousRow), right(pawnPreviousRow)]:
            if self.hasPiece(pp) and self.get(pp).isA(PAWN, color):
                return True

        # Check Rooks
        for moveFunction in [left, right, above, below]:
            current = moveFunction(pos)
            while self.validPos(current) and self.isEmpty(current):
                current = moveFunction(current)

            if self.hasPiece(current) and self.get(current).isA(ROOK, color):
                return True

        # Check King
        for c in self.validSurroundings(pos):
            if self.hasPiece(c) and self.get(c).isA(KING, color):
                return True

        return False

    def possibleMoves(self, pos):
        """ Where could the piece at 'pos' move to?
            In the case of a king, it will only return squares
            that are not threatened by the other color
            """
        # initialize the array with potential moves
        moves = []

        # if not valid or empty, then no moves are possible
        if not self.hasPiece(pos):
            return moves

        piece = self.get(pos)

        match piece.piece:
            case 1: # Pawn
                # the basic move to advance one cell
                advance = above(pos) if piece.color == WHITE else below(pos)
                if (self.validDest(advance)):
                    moves.append(advance)

                # eat
                for eat_move in [left(advance), right(advance)]:
                    if self.validEat(eat_move, piece):
                        moves.append(eat_move)

            case 4: # Rook
                moveFunctions = [left, right, above, below]
                for moveFunction in moveFunctions:
                    current = moveFunction(pos)
                    # move
                    while self.validDest(current):
                        moves.append(current)
                        current = moveFunction(current)

                    # eat
                    if self.validEat(current, piece):
                        moves.append(current)

            case 6: # King
                # Temporarily remove the king from its current position so that it doesn't block potential threats
                self.set(pos, EMPTY)

                potential = [left(above(pos)), above(pos), right(above(pos)),
                    left(pos), right(pos),
                    left(below(pos)), below(pos), right(below(pos))]
                

                for c in potential:
                    if not self.isThreatened(c, otherColor(piece)) and (self.validEat(c, piece) or self.validDest(c)):
                        moves.append(c)

                # Restore the king to is position
                self.set(pos, piece)

        # Create proper Move from the resulting posinates
        return list(map(lambda m: Move(pos, m), moves))

    def allPiecesFrom(self, color):
        """ Returns an iterator of tuples (row, column, piece) """
        rowIndex = 0
        for row in self.board:
            colIndex = 0
            for piece in row:
                if piece is not 0 and piece.color == color:
                    yield (rowIndex, colIndex, piece)
                colIndex = colIndex + 1
            rowIndex = rowIndex + 1

    def isCheckMated(self, color):
        kingPos = self.find(Piece(KING, color))
        return self.isThreatened(kingPos, otherColor(color)) and not self.possibleMoves(kingPos)

    def isChecked(self, color):
        kingPos = self.find(Piece(KING, color))
        return self.isThreatened(kingPos, otherColor(color)) 

    def getAllMovesFor(self, color):
        """ if the king is checked, then the only possible moves are those that un-check him """
        moves = []
        for (row, col, _) in self.allPiecesFrom(color):
            moves = moves + self.possibleMoves((row, col))

        validMoves = []
        for move in moves:
            b = self.cloneMove(move)
            if not b.isChecked(color):
                validMoves.append(move)

        return validMoves

    def clone(self):
        newBoard = Board(self.size)
        for (pos, piece) in self.iter():
            newBoard.set(pos, piece)
        return newBoard

    def cloneMove(self, move):
        newBoard = self.clone()
        newBoard.move(move)
        return newBoard

    def iter(self):
        rowIndex = 0
        for row in self.board:
            colIndex = 0
            for square in row:
                c = (rowIndex, colIndex)
                yield (c, square)
                colIndex = colIndex + 1
            rowIndex = rowIndex + 1


class Move:
    def __init__(self, _from, _to):
        self._from = _from
        self._to = _to
    
    def __str__(self):
        return f"({self._from}, {self._to})"

    def __repr__(self):
        return self.__str__()    
