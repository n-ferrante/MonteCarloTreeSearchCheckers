from Board import *

class mctsAgent:
    def __init__(self, player):
        self.player = player
        self.gameTree = []
    

    def mcts(self, board, player, iterations):
        state = board.getBoard()
        currentNode = None

        for node in self.gameTree:
            if (node.getState() == state).all():
                currentNode = node

        if currentNode is not None:
            currentNode.removeParent()
        else:
            allLegalMoves = board.getAllLegalMoves(player)
            currentNode = Node(player, state, None, len(allLegalMoves))
            self.gameTree.append(currentNode)

        iter = 0
        while iter < iterations:
            nextNode = self.chooseNode(currentNode, player)
            val = self.simulate(nextNode)
            self.backProp(nextNode, val)
            iter += 1

        move, piece = self.bestMove(currentNode)
        return move, piece
        

    def chooseNode(self, node, player):
        currentState = node.getState()

        board = Board()  
        board.setBoard(currentState)

        while node.getNumChildren() > 0:
            if board.isTerminal()[0]:
                return node

            legalMoves = board.getAllLegalMoves(player)
                    
            if len(node.getChildren()) < len(legalMoves):
                
                unexpandedMoves = []
                for move in legalMoves:
                    if move not in node.expandedMoves:
                        unexpandedMoves.append(move)
                
                move = random.choice(unexpandedMoves)

                nextBoard = board.testMove(move[1], move[0])
                nextState = nextBoard.getBoard()
                nextPlayer = nextBoard.nextPlayer(player)
                numChildren = len(nextBoard.getAllLegalMoves(nextPlayer))
                
                child = Node(nextPlayer, nextState, move, numChildren)
                node.addChild(child)
                self.gameTree.append(child)

                return child
            
            else:
                node = self.getBestChild(node)

        return node
        

    def getBestChild(self, node):
        maxUCB = -float("inf")
        maxChild = None

        for child in node.getChildren():
            if self.getUCBVal(child) == float("inf"):
                return child
            
            if self.getUCBVal(child) > maxUCB:
                maxUCB = self.getUCBVal(child)
                maxChild = child

        return maxChild


    def bestMove(self, node):
        bestChild = self.getBestChild(node)
        move = bestChild.getMove()

        return move[0], move[1]


    def simulate(self, node):
        board = Board()
        board.setBoard(node.getState())
        player = node.getPlayer()

        iter = 0
        while not board.isTerminal()[0] and iter < 10:
            move, piece = board.randomMove(player)
            if move is None:
                break
            
            board.move(piece, move)
            player = board.nextPlayer(player)
            iter += 1

        return board.evaluateState(self.player)


    def backProp(self, node, val):
        while node.parent is not None:
            node.addVisit()
            node.addNodeValue(val)

            node = node.parent

        node.addVisit()
        node.addNodeValue(val)
        

    def getUCBVal(self, node):
        if node.getNumVisits() == 0:
            return float("inf")
        
        avgVal = 0
        count = 0
        children = node.getChildren()


        for child in children:
            if child.getNumVisits() == 0: continue
            avgVal += child.getNodeScore()
            count += 1

        if count != 0:
           avgVal = avgVal / count
        else:
            avgVal = node.getNodeScore()
        ucb = avgVal + 2 * np.sqrt(np.log(node.getParentNumVisits()) / node.getNumVisits())

        return ucb
    


class Node:
    def __init__(self, player, state, move, numChildren):
        self.player = player
        self.state = state 
        self.move = move
        self.parent = None
        self.children = []
        self.expandedMoves = set()
        self.numVisits = 0
        self.totalScore = 0
        self.numChildren = numChildren

    def getPlayer(self):
        return self.player

    def getState(self):
        return self.state

    def getMove(self):
        return self.move
    
    def getChildren(self):
        return self.children
    
    def getNumChildren(self):
        return self.numChildren
    
    def getNumVisits(self):
        return self.numVisits
    
    def getParentNumVisits(self):
        return self.parent.getNumVisits()
    
    def getNodeScore(self):
        if self.numVisits == 0:
            return float("inf")
        return self.totalScore
    
    def addChild(self, child):
        self.expandedMoves.add(child.getMove())
        self.children.append(child)
        child.parent = self

    def addVisit(self):
        self.numVisits += 1
    
    def addNodeValue(self, val):
        self.totalScore += val

    def removeParent(self):
        self.parent = None
