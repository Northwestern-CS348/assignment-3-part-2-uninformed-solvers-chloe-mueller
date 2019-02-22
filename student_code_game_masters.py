from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        # return list
        tuples = []

        # check peg1
        peg1_list = []
        fact_1 = parse_input('fact: (on ?d peg1)')

        matches = self.kb.kb_ask(fact_1)
        if matches == False:
            tuples.append(())
        else:
            for m in matches:
                d = m.bindings_dict['?d']
                peg1_list.append(int(d[-1]))
            peg1_list.sort()
            tuples.append(tuple(peg1_list))

        # check peg2
        peg2_list = []
        fact_2 = parse_input('fact: (on ?d peg2)')

        matches = self.kb.kb_ask(fact_2)
        if matches == False:
            tuples.append(())
        else:
            for m in matches:
                d = m.bindings_dict['?d']
                peg2_list.append(int(d[-1]))
            peg2_list.sort()
            tuples.append(tuple(peg2_list))

        #check peg3
        peg3_list = []
        fact_3 = parse_input('fact: (on ?d peg3)')

        matches = self.kb.kb_ask(fact_3)
        if matches == False:
            tuples.append(())
        else:
            for m in matches:
                d = m.bindings_dict['?d']
                peg3_list.append(int(d[-1]))
            peg3_list.sort()
            tuples.append(tuple(peg3_list))

        return tuple(tuples)


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        if GameMaster.isMovableLegal(self, movable_statement):

            vars = movable_statement.terms
            currDisk = str(vars[0])
            oldPeg = str(vars[1])
            newPeg = str(vars[2])

            # assert and retract ON facts
            self.kb.kb_retract(parse_input('fact: (on '+currDisk+' '+oldPeg+')'))
            self.kb.kb_assert(parse_input('fact: (on '+currDisk+' '+newPeg+')'))

            #find what its onTopOf
            q1 = parse_input('fact: (onTopOf '+currDisk+' ?d)')
            match1 = self.kb.kb_ask(q1)
            # if its on top of something
            if match1:
                underneath = match1[0].bindings_dict['?d']
                self.kb.kb_retract(parse_input('fact: (onTopOf '+currDisk+' '+underneath+')'))
                # make underneath the new top of peg
                self.kb.kb_assert(parse_input('fact: (top '+underneath+' '+oldPeg+')'))
            else:
                self.kb.kb_assert(parse_input('fact: (empty '+oldPeg+')'))

            #find whats on top of new peg
            q2 = parse_input('fact: (top ?d '+newPeg+')')
            match2 = self.kb.kb_ask(q2)
            #if a disk is on new peg
            if match2:
                oldTop = match2[0].bindings_dict['?d']
                self.kb.kb_retract(parse_input('fact: (top '+oldTop+' '+newPeg+')'))
                self.kb.kb_assert(parse_input('fact: (top '+currDisk+' '+newPeg+')'))
                self.kb.kb_assert(parse_input('fact: (onTopOf '+currDisk+' '+oldTop+')'))
            #if nothing on peg
            else:
                self.kb.kb_retract(parse_input('fact: (empty '+newPeg+')'))
                self.kb.kb_assert(parse_input('fact: (top '+currDisk+' '+newPeg+')'))

        pass





        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code
        tuples = []
        #row 1
        row1 = []
        q = parse_input('fact: (posn ?t pos1 pos1)')
        match = self.kb.kb_ask(q)
        m = match[0].bindings_dict['?t']
        if m == 'empty':
            row1.append(-1)
        else:
            row1.append(int(m[-1]))

        q = parse_input('fact: (posn ?t pos2 pos1)')
        match = self.kb.kb_ask(q)
        m = match[0].bindings_dict['?t']
        if m == 'empty':
            row1.append(-1)
        else:
            row1.append(int(m[-1]))

        q = parse_input('fact: (posn ?t pos3 pos1)')
        match = self.kb.kb_ask(q)
        m = match[0].bindings_dict['?t']
        if m == 'empty':
            row1.append(-1)
        else:
            row1.append(int(m[-1]))

        tuples.append(tuple(row1))

        row2 = []
        q = parse_input('fact: (posn ?t pos1 pos2)')
        match = self.kb.kb_ask(q)
        m = match[0].bindings_dict['?t']
        if m == 'empty':
            row2.append(-1)
        else:
            row2.append(int(m[-1]))

        q = parse_input('fact: (posn ?t pos2 pos2)')
        match = self.kb.kb_ask(q)
        m = match[0].bindings_dict['?t']
        if m == 'empty':
            row2.append(-1)
        else:
            row2.append(int(m[-1]))

        q = parse_input('fact: (posn ?t pos3 pos2)')
        match = self.kb.kb_ask(q)
        m = match[0].bindings_dict['?t']
        if m == 'empty':
            row2.append(-1)
        else:
            row2.append(int(m[-1]))

        tuples.append(tuple(row2))

        row3 = []
        q = parse_input('fact: (posn ?t pos1 pos3)')
        match = self.kb.kb_ask(q)
        m = match[0].bindings_dict['?t']
        if m == 'empty':
            row3.append(-1)
        else:
            row3.append(int(m[-1]))

        q = parse_input('fact: (posn ?t pos2 pos3)')
        match = self.kb.kb_ask(q)
        m = match[0].bindings_dict['?t']
        if m == 'empty':
            row3.append(-1)
        else:
            row3.append(int(m[-1]))

        q = parse_input('fact: (posn ?t pos3 pos3)')
        match = self.kb.kb_ask(q)
        m = match[0].bindings_dict['?t']
        if m == 'empty':
            row3.append(-1)
        else:
            row3.append(int(m[-1]))

        tuples.append(tuple(row3))

        return tuple(tuples)


        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        if GameMaster.isMovableLegal(self, movable_statement):
            vars = movable_statement.terms
            currTile = str(vars[0])
            oldX = str(vars[1])
            oldY = str(vars[2])
            newX = str(vars[3])
            newY = str(vars[4])

            q = parse_input('fact: (posn ?t '+newX+' '+newY+')')
            match = self.kb.kb_ask(q)
            oldTile = match[0].bindings_dict['?t']

            self.kb.kb_retract(parse_input('fact: (posn '+currTile+' '+oldX+' '+oldY+')'))
            self.kb.kb_retract(parse_input('fact: (posn '+oldTile+' '+newX+' '+newY+')'))

            self.kb.kb_assert(parse_input('fact: (posn '+currTile+' '+newX+' '+newY+')'))
            self.kb.kb_assert(parse_input('fact: (posn '+oldTile+' '+oldX+' '+oldY+')'))

        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
