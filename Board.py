import numpy as np
import random
from Constants import *

class Board:
    """
    A board object acts as the playing surface for the agents playing checkers.
    Each board is made up of a 6x6 array initialized to the starting position of checkers
    with functions to ensure the rules of checkers are enforced regarding legal moves 
    that can be made.
    A board object also contains variables and functions used to evaluate
    the current game state in regards to whether a given agent is winning or losing.
    """
    
    def __init__(self):
        self.board = self.generateBoard()
        self.turn = AGENT
        self.movesLeft = True   # tracks if a player has legal moves left to make
        self.pieceCount = {}
        self.kingCount = {}
        
        self.pieceCount[AGENT] = 6
        self.pieceCount[OPP] = 6
        
        self.kingCount[AGENT] = 0
        self.kingCount[OPP] = 0

        
    def generateBoard(self):
        """
        Creates a new 6x6 board and initializes starting position of pieces.
        """

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
        """
        Returns current state of the board.
        """
        return self.board
    

    def setBoard(self, board):
        """
        Sets the current board to the board given in the argument.
        """
        self.board = board


    def getPieceCount(self, player):
        """
        Returns the number of pieces the given player has.
        """
        return self.pieceCount[player]
    

    def getKingCount(self, player):
        """
        Returns the number of kings the given player has.
        """
        return self.kingCount[player]


    def getBackRowCount(self, player):
        """
        Returns the number of pieces a given player has in the back row 
        on their side of the board. 
        Used to put an emphasis on moves that avoid moving pieces 
        out of the back row and opening up a king opportunity for the opponent.
        """
        if player == AGENT:
            return np.sum(self.board[5] == 1)
        else:
            return np.sum(self.board[0] == -1)


    def getPieces(self, player):
        """
        Returns a list containing the location of the remaining pieces the given player has.
        """
        pieces = []
        x = 0
        y = 0
        
        for row in self.board:
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
        """
        Returns the number of pieces the given player has on the opponent's 
        side of the board. 
        Used to determine the value of a state.
        """
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
        """
        Returns the moves that are in bounds on the game board.
        """
        if self.board[loc] == 0:
            return None

        # Get x and y coordinates of the current piece's location on the board
        x, y = loc

        # Create an empty list used to keep track of illegal moves
        illMoves = []

        # If current piece is a king, start with all legal moves
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
    

    def getNewPos(self, loc, direction): 
        """
        Returns the new position of a piece after performing a move.
        """
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
    

    def checkPosInBounds(self, loc):
        """
        Checks if the given location is in bounds on the board. 
        Used when a jump is performed by a player.
        """
        x, y = loc
        if x > 5 or x < 0 or y > 5 or y < 0:
            return False
        
        return True
    

    def getLegalMoves(self, loc):
        """
        Returns the legal moves that can be made from a given location.
        """
        jump = False
        movesInBounds = self.getMovesInBounds(loc)
        legalMoves = []
        
        # If no legal moves are available, return empty list
        if movesInBounds is None: return legalMoves
        
        
        for move in movesInBounds:
            jump = False
            newPos = self.getNewPos(loc, move)

            # Check if the new position is vacant or occupied
            if self.board[newPos] == 0:     # position is vacant, add legal move to list
                legalMoves.append((move, jump))
                continue
            else:   # position is occupied
                if np.sign(self.board[newPos]) == np.sign(self.board[loc]):   # if the new position is occupied by an allied piece,
                    continue                                                  # do not add move to list of legal moves
                else:   # new position is occupied by an enemy piece
                    newPos2 = self.getNewPos(newPos, move)      # get the location of new position after a jump is performed
                    if self.checkPosInBounds(newPos2) and self.board[newPos2] == 0:     # position after jump is in bounds and vacant
                        jump = True
                        legalMoves.append((move, jump))

        return legalMoves


    def getAllLegalMoves(self, player):
        """
        Returns the legal moves of all pieces for a given player, 
        rather than just the legal moves of a given piece.
        """
        allLegalMoves = []
        
        pieces = self.getPieces(player)
        for piece in pieces:
            for move in self.getLegalMoves(piece):
                allLegalMoves.append((move, piece))

        return allLegalMoves
    

    def testMove(self, loc, move):
        """
        Performs a move on a new board rather than the current playing board.
        Used to test the value of different available moves in Monte Carlo Tree Search,
        Alpha-Beta, and Minimax algorithms.
        """
        newBoard = Board()
        newBoard.setBoard(self.board.copy())

        newBoard.move(loc, move)

        return newBoard


    def move(self, loc, move):
        """
        Performs a given move from a specified location on the current game board.
        """

        # Check if the given move is in fact a legal move
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

        # Perform the move
        if move[1] == False:    # if no jump is available
            newPos = self.getNewPos(loc, move[0])
            finalLoc = newPos

            self.board[newPos] = self.board[loc]
            self.board[loc] = 0
        else:   # if jump is available
            newPos = self.getNewPos(loc, move[0])   # represents the position of the piece being jumped
            newPos2 = self.getNewPos(newPos, move[0])   # represents the position of the piece being moved (doing the jumping)
            finalLoc = newPos2

            self.board[newPos2] = self.board[loc]
            self.board[loc] = 0
            self.board[newPos] = 0  # remove enemy piece

        # Check if the piece moved should be upgraded to a king    
        if not self.isKing(self.board, finalLoc):    # if piece moved is not already a king
            x, y = finalLoc
            if turn == AGENT and x == 0:    # if it is the agent's turn and their piece reaches the opponent's back row
                self.board[finalLoc] = 2
                self.kingCount[AGENT] += 1
            elif turn == OPP and x == 5:   # if it is the opponent's turn and their piece reaches the agent's back row
                self.board[finalLoc] = -2
                self.kingCount[OPP] +=1
        
    

    def randomMove(self, player):
        """
        Selects a random move for a player to perform.
        Used for performance testing of other algorithms.
        """

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
        """
        Selects the first available move that a player has.
        Used for performance testing of other algorithms.
        """
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
        """
        Returns whether or not a specific location on a given board
        is a king or not.
        """
        if abs(board[loc]) == 2:
            return True
        
        return False
    

    def changeTurn(self):
        """
        Changes the turn of the board game.
        """
        if self.turn == AGENT:
            self.turn = OPP
        else:
            self.turn = AGENT

        return self.turn
    

    def nextPlayer(self, player):
        """
        Returns whose turn it is next (returns the opposing player).
        Used to calculate the state evalution formula.
        """
        if player == AGENT:
            nextPlayer = OPP
        else:
            nextPlayer = AGENT

        return nextPlayer


    def evaluateState(self, player):
        """
        Returns the value of a state for a given player.
        Considers the number of pieces each player has, the number of 
        kings each player has, and how many pieces the given player 
        has in the enemy's territory.
        """
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
        """
        Determines if a game state is terminal.
        Returns True or False, along with the winner if the game is over.
        """
        gameOver = False
        winner = None

        if len(self.getPieces(AGENT)) == 0 or (self.movesLeft == False and self.turn == AGENT): # if agent is out of pieces
            gameOver = True
            winner = OPP
        if len(self.getPieces(OPP)) == 0 or (self.movesLeft == False and self.turn == OPP):   # if opponent is out of pieces
            gameOver = True
            winner = AGENT

        return gameOver, winner
