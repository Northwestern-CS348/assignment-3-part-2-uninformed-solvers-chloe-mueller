
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        #if start node is victory condition
        #print(self.currentState.state)
        if self.currentState.state == self.victoryCondition:
            return True

        # mark current node as visited
        self.visited[self.currentState] = True

        currNode = self.currentState
        # if there are possible moves
        moves = self.gm.getMovables()
        #print(moves[0], moves[1])
        if moves:
            # populate children
            for m in moves:
                self.gm.makeMove(m)
                newState = GameState(self.gm.getGameState(), currNode.depth + 1, m)
                newState.parent = currNode
                currNode.children.append(newState)
                self.gm.reverseMove(m)
            # iterate through children
            while(currNode.nextChildToVisit < len(currNode.children)):
                currChild = self.currentState.children[self.currentState.nextChildToVisit]
                #if visited it true, go to the next
                if currChild in self.visited:
                    currNode.nextChildToVisit += 1
                #if not visited, go into this node and return
                else:
                    currNode.nextChildToVisit += 1
                    self.visited[currChild] = True
                    self.gm.makeMove(currChild.requiredMovable)
                    self.currentState = currChild
                    return False

        # if no possible moves or unvisited child not found, move up to parent node
        self.gm.reverseMove(self.currentState.requiredMovable)
        self.currentState = currNode.parent
        return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.queue = []
        self.head = 0

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.currentState.state == self.victoryCondition:
            return True
        #if the children haven't been enqueued, add them
        if not self.currentState.children:
            moves = self.gm.getMovables()
            for m in moves:
                self.gm.makeMove(m)
                newState = GameState(self.gm.getGameState(), self.currentState.depth + 1, m)
                newState.parent = self.currentState
                self.currentState.children.append(newState)
                self.queue.append(newState)
                self.gm.reverseMove(m)
        #if haven't gone through whole queue
        while self.head < len(self.queue):
            #get next from queue
            nextNode = self.queue[self.head]
            self.head += 1
            #if visited, go to next
            if nextNode in self.visited:
                continue
            #see if new Node is a child of oldNode
            if nextNode.parent == self.currentState:
                self.currentState = nextNode
                self.gm.makeMove(self.currentState.requiredMovable)
                self.visited[self.currentState] = True
                if self.currentState.state == self.victoryCondition:
                    return True
                else:
                    return False
            #if sibling depth and parent are the same
            if nextNode.parent == self.currentState.parent and nextNode.depth == self.currentState.depth:
                #reverse move to get to parent
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.gm.makeMove(nextNode.requiredMovable)
                self.currentState = nextNode
                self.visited[self.currentState] = True
                if self.currentState.state == self.victoryCondition:
                    return True
                else:
                    return False
            #else: its a cousin or a nephew
            else:
                #go to the head of the tree
                while self.currentState.parent:
                    self.gm.reverseMove(self.currentState.requiredMovable)
                    self.currentState = self.currentState.parent
                curr = nextNode
                reqMoves = []
                #go up the tree
                while curr.parent:
                    reqMoves.append(curr.requiredMovable)
                    curr = curr.parent
                reqMoves.reverse()
                #make moves until you reach depth
                i = 0
                while i < nextNode.depth:
                    self.gm.makeMove(reqMoves[i])
                    i += 1
                self.currentState = nextNode
                self.visited[self.currentState] = True
                if self.currentState.state == self.victoryCondition:
                    return True
                else:
                    return False
