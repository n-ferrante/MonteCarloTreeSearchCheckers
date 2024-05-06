import numpy as np
import random

# Different directions to move
NORTHEAST = "northeast"
NORTHWEST = "northwest"
SOUTHEAST = "southeast"
SOUTHWEST = "southwest"

# Different turns
AGENT = "agent"
OPP = "opposition"


class Board:
    def __init__(self):
        self.board = self.generateBoard()
        self.turn = AGENT
        self.movesLeft = True
        self.pieceCount = {}
        self.kingCount = {}
        
        self.pieceCount[AGENT] = 12
        self.pieceCount[OPP] = 12
        
        self.kingCount[AGENT] = 0
        self.kingCount[OPP] = 0

        
    def generateBoard(self):
        board = np.zeros((6,6), dtype = 'int8')

        # Initialize starting position of opponent's pieces
        board[0:2, 1::2] = -1
        board[1, :] = 0
        board[1, ::2] = -1

        # Intialize starting position of agent's pieces
        board[4:6, ::2] = 1
        board[4, ::2] = 0
        board[4, 1::2] = 1
        
        return board


    def getBoard(self):
        return self.board
    

    def setBoard(self, board):
        self.board = board


    def getPieceCount(self, player):
        return self.pieceCount[player]
    

    def getKingCount(self, player):
        return self.kingCount[player]


    def getBackRowCount(self, player):
        if player == AGENT:
            return np.sum(self.board[5] == 1)
        else:
            return np.sum(self.board[0] == -1)


    def getPieces(self, player):
        pieces = []
        x = 0
        y = 0
        
        for row in self.board: # maybe try for row in board.getBoard()
            if x > 5: x = 0
            for piece in row:
                if y > 5: y = 0
                if player == AGENT: # if it is the agent's turn, get location of all pieces greater than 0
                    if piece > 0:  
                        loc = (x,y)
                        pieces.append(loc)
                else:
                    if piece < 0: # if it's the opponent's turn, get location of all pieces less than 0
                        loc = (x,y)
                        pieces.append(loc)
                y += 1
            x += 1
        
        return pieces


    def getPieceEnemyTerritory(self, player):
        pieces = self.getPieces(player)
        count = 0

        if player == AGENT:
            for piece in pieces:
                x, y = piece
                if x < 3: count += 1
        else:
            for piece in pieces:
                x, y = piece
                if x > 2: count += 1

        return count


    def getMovesInBounds(self, loc):
        if self.board[loc] == 0:
            return None

        # Get x and y coordinates of the current piece's location on board
        x, y = loc

        # Create an empty list used to keep track of illegal moves
        illMoves = []

        # If current piece is a king, start with all moves legal
        # otherwise assign appropriate moves to start
        if self.isKing(self.board, loc):
            moves = [NORTHEAST, NORTHWEST, SOUTHEAST, SOUTHWEST]
        else:
            if self.board[loc] > 0:
                moves = [NORTHEAST, NORTHWEST]
            else:
                moves = [SOUTHEAST, SOUTHWEST]

        if x - 1 < 0:
            illMoves.extend([NORTHEAST, NORTHWEST])
        if x + 1 > 5:
            illMoves.extend([SOUTHEAST, SOUTHWEST])
        if y - 1 < 0:
            illMoves.extend([NORTHWEST, SOUTHWEST])
        if y + 1 > 5:
            illMoves.extend([NORTHEAST, SOUTHEAST])
            
        moves = [ele for ele in moves if ele not in illMoves]
        
        return moves


    def getNewPos(self, loc, direction): # Used to get new position after doing a move
        x, y = loc
        newPos = None

        if direction == NORTHEAST:
            newPos = ((x - 1), (y + 1))
        elif direction == NORTHWEST:
            newPos = ((x - 1), (y - 1))
        elif direction == SOUTHEAST:
            newPos = ((x + 1), (y + 1))
        elif direction == SOUTHWEST:
            newPos = ((x + 1), (y - 1))

        return newPos

    def checkPosInBounds(self, loc): # Used to check if position after jumping a piece is in bounds
        x, y = loc
        if x > 5 or x < 0 or y > 5 or y < 0:
            return False
        
        return True


    def getLegalMoves(self, loc):
        jump = False
        movesInBounds = self.getMovesInBounds(loc)
        legalMoves = []
        
        if movesInBounds is None: return legalMoves
        for move in movesInBounds:
            jump = False
            newPos = self.getNewPos(loc, move)

            if self.board[newPos] == 0:     # if the new position after the move is vacant, add move to legal moves
                legalMoves.append((move, jump))
                continue
            else:   # new position after move is occupied
                if np.sign(self.board[newPos]) == np.sign(self.board[loc]):   # if the new position after the move is occupied by an allied piece, don't add move to legal moves, spot is already taken 
                    continue
                else:   # new position after move is occupied by an enemy piece
                    newPos2 = self.getNewPos(newPos, move)
                    if self.checkPosInBounds(newPos2) and self.board[newPos2] == 0:
                        jump = True
                        legalMoves.append((move, jump))

        return legalMoves


    def getAllLegalMoves(self, player):
        allLegalMoves = []
        
        pieces = self.getPieces(player)
        for piece in pieces:
            for move in self.getLegalMoves(piece):
                allLegalMoves.append((move, piece))

        return allLegalMoves
    

    def testMove(self, loc, move):
        newBoard = Board()
        newBoard.setBoard(self.board.copy())
        
        #newBoard = self.copyBoard(self.board)

        newBoard.move(loc, move)

        return newBoard


    def move(self, loc, move):
        legalMoveCheck = False
        for legalMove in self.getLegalMoves(loc):
            if legalMove[0] == move[0]:
                legalMoveCheck = True
                break
        if not legalMoveCheck: return "Not a legal move"

        finalLoc = None

        # Determine whose turn it is
        if self.board[loc] > 0:
            turn = AGENT
        else:
            turn = OPP

        if move[1] == False:    # if no jump is available
            newPos = self.getNewPos(loc, move[0])
            finalLoc = newPos

            self.board[newPos] = self.board[loc]
            self.board[loc] = 0

        else:   # if jump is available
            newPos = self.getNewPos(loc, move[0])   # represents the position of the piece being jumped
            newPos2 = self.getNewPos(newPos, move[0])   # represents the position of the piece being move (doing the jumping)
            finalLoc = newPos2

            self.board[newPos2] = self.board[loc]
            self.board[loc] = 0
            self.board[newPos] = 0  # remove enemy piece

        if not self.isKing(self.board, finalLoc):    # if the piece being moved is not already a king
            x, y = finalLoc
            if turn == AGENT and x == 0:    # if it is the agent's turn and their piece reaches the opponent's back row
                self.board[finalLoc] = 2
                self.kingCount[AGENT] += 1
            elif turn == OPP and x == 5:   # if it is the opponent's turn and their piece reaches the agent's back row
                self.board[finalLoc] = -2
                self.kingCount[OPP] +=1
        
    

    def randomMove(self, player):
        pieces = self.getPieces(player)
        randPiece = random.choice(pieces)
        while len(self.getLegalMoves(randPiece)) == 0:
            pieces.remove(randPiece)
            if len(pieces) == 0:
                self.movesLeft = False
                return None, None
            randPiece = random.choice(pieces)
        
        randMove = random.choice(self.getLegalMoves(randPiece))

        return randMove, randPiece


    def selectFirstAction(self, player):
        pieces = self.getPieces(player, self.board)
        piece = None

        for i in range(len(pieces)):
            piece = pieces[i]
            legalMoves = self.getLegalMoves(piece)
            if len(legalMoves) != 0: break
        
        if len(legalMoves) == 0: 
            self.movesLeft = False
            return None, None
        move = legalMoves[0]
        
        return move, piece
   

    def isKing(self, board, loc):
        if abs(board[loc]) == 2:
            return True
        
        return False
    

    def changeTurn(self):
        if self.turn == AGENT:
            self.turn = OPP
        else:
            self.turn = AGENT

        return self.turn
    

    def nextPlayer(self, player):
        if player == AGENT:
            nextPlayer = OPP
        else:
            nextPlayer = AGENT

        return nextPlayer


    def evaluateState(self, player):
        if self.isTerminal()[0]:
            if self.isTerminal()[1] == player: return 100 
            else: return -100
        
        enemy = self.nextPlayer(player)

        pieceCount = self.getPieceCount(player)
        enemyPieceCount = self.getPieceCount(enemy)
        kingCount = self.getKingCount(player)
        enemyKingCount = self.getKingCount(enemy)
        piecesinEnTerritory = self.getPieceEnemyTerritory(player)  


        return pieceCount + (2 * kingCount) - enemyPieceCount - (2 * enemyKingCount) + piecesinEnTerritory
       

    def isTerminal(self):
        gameOver = False
        winner = None

        if len(self.getPieces(AGENT)) == 0 or (self.movesLeft == False and self.turn == AGENT): # if agent is out of pieces
            gameOver = True
            winner = OPP
        if len(self.getPieces(OPP)) == 0 or (self.movesLeft == False and self.turn == OPP):   # if opponent is out of pieces
            gameOver = True
            winner = AGENT

        return gameOver, winner
