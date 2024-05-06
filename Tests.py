from Constants import *
from MonteCarloTreeSearch import *
from MinimaxAlphaBeta import *

class MCTSvsMinimax:
        
    def main():
        wins = {}
        wins[AGENT] = 0
        wins[OPP] = 0
        
        for i in range(10):

            board = Board()
            turn = AGENT
            count = 0
            agent = mctsAgent(AGENT)
            
            while not board.isTerminal()[0]:
                if turn == AGENT:
                    move, piece = agent.mcts(board, AGENT, 5)
                else:
                    move, score, piece, = maxValue(OPP, 3, board)             
                    if move == None: 
                        board.movesLeft = False
                        break
                board.move(piece, move)
                turn = board.changeTurn()
                count += 1

            if board.isTerminal()[0]:
                result = board.isTerminal()
            
            if result[1] == AGENT:
                wins[AGENT] += 1
            else:
                wins[OPP] += 1

        print(wins)

    main()



class MCTSvsAlphaBeta:
        
    def main():
        wins = {}
        wins[AGENT] = 0
        wins[OPP] = 0
        
        for i in range(10):

            board = Board()
            turn = AGENT
            count = 0
            agent = mctsAgent(AGENT)
            
            while not board.isTerminal()[0]:
                if turn == AGENT:
                    move, piece = agent.mcts(board, AGENT, 5)
                else:
                    move, score, piece, = alphaMaxValue(OPP, 3, board, -float("inf"), float("inf"))             
                    if move == None: 
                        board.movesLeft = False
                        break
                board.move(piece, move)
                turn = board.changeTurn()
                count += 1

            if board.isTerminal()[0]:
                result = board.isTerminal()
            
            if result[1] == AGENT:
                wins[AGENT] += 1
            else:
                wins[OPP] += 1

        print(wins)

    main()
