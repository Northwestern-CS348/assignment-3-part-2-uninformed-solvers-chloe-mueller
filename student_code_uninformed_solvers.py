
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
        return True
