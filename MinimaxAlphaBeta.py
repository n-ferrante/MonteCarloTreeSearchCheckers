import Board

def minimax(player, depth, board):
    if depth == 0 or board.isTerminal()[0]:
        return board.evaluateState(player)
    if player == AGENT:
        return maxValue(AGENT, depth, board)[1]
    else:
        return minValue(OPP, depth, board)[1]
    

def maxValue(player, depth, board):
    nextTurn = None
    if player == AGENT:
        nextTurn = OPP
    else:
        nextTurn = AGENT

    maxScore = -float("inf")
    maxMove = None
    maxPiece = None

    pieces = board.getPieces(player)
    for piece in pieces:
        for move in board.getLegalMoves(piece):
            #moves.append((piece, move))
            if move[1]:     # if there is a jump available, take it
                return move, 100, piece
            nextState = board.testMove(piece, move)
            score = minimax(nextTurn, depth - 1, nextState)

            if score > maxScore:
                maxScore = score
                maxMove = move
                maxPiece = piece
        
    return maxMove, maxScore, maxPiece  


def minValue(player, depth, board):
    nextTurn = None
    if player == AGENT:
        nextTurn = OPP
    else:
        nextTurn = AGENT

    
    minScore = float("inf")
    minMove = None
    minPiece = None

    pieces = board.getPieces(player)
    for piece in pieces:
        for move in board.getLegalMoves(piece):
            if move[1]:
                return move, -100, piece
            nextState = board.testMove(piece, move)
            score = minimax(nextTurn, depth - 1, nextState)

            if score < minScore:
                minScore = score
                minMove = move
                minPiece = piece
        
    return minMove, minScore, minPiece    

  



def alphaBeta(player, depth, board, alpha, beta):
    if depth == 0 or board.isTerminal()[0]:
        return board.evaluateState(player)
    if player == AGENT:
        return alphaMaxValue(AGENT, depth, board, alpha, beta)[1]
    else:
        return alphaMinValue(OPP, depth, board, alpha, beta)[1]

def alphaMaxValue(player, depth, board, alpha, beta):
    nextTurn = None
    if player == AGENT:
        nextTurn = OPP
    else:
        nextTurn = AGENT

    maxScore = -float("inf")
    maxMove = None
    maxPiece = None

    pieces = board.getPieces(player)
    for piece in pieces:
        for move in board.getLegalMoves(piece):
            #moves.append((piece, move))
            nextState = board.testMove(piece, move)
            score = alphaBeta(nextTurn, depth - 1, nextState, alpha, beta)

            if score > maxScore:
                maxScore = score
                maxMove = move
                maxPiece = piece
            if maxScore > beta:
                return maxMove, maxScore, maxPiece
            elif maxScore > alpha:
                alpha = maxScore
        
    return maxMove, maxScore, maxPiece


def alphaMinValue(player, depth, board, alpha, beta):
    nextTurn = None
    if player == AGENT:
        nextTurn = OPP
    else:
        nextTurn = AGENT
    
    minScore = float("inf")
    minMove = None
    minPiece = None

    pieces = board.getPieces(player)
    for piece in pieces:
        for move in board.getLegalMoves(piece):
            nextState = board.testMove(piece, move)
            score = alphaBeta(nextTurn, depth - 1, nextState, alpha, beta)

            if score < minScore:
                minScore = score
                minMove = move
            if minScore < alpha:
                return minMove, minScore, minPiece
            elif minScore < beta:
                beta = minScore
        
    return minMove, minScore, minPiece
