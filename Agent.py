# Agent.py
#
# Code doesn't interpret intermediate safe locations

import Action
import Orientation
import Search
from random import randint
from collections import deque

class State:
    def __init__(self):
        self.gold = False
        self.arrow = True
        self.stenchLocations = set()
        self.breezeLocations = set()
        self.pitLocations = set()
        self.visitedLocations = set()
        self.safeLocations = set()
        self.removedSafeLocations = set()
        self.orientation = Orientation.RIGHT
        # coordinate x, y
        self.worldSize = [3,3]
        self.location = [1,1]
        self.prevLocation = []
        self.goldLocation = []
        self.wumpusLocation = []

    def reprOrientation(self):
        switch = {
            Orientation.LEFT: "LEFT",
            Orientation.UP: "UP",
            Orientation.RIGHT: "RIGHT",
            Orientation.DOWN: "DOWN",
            -3: "UP",
            -2: "LEFT",
            -1: "DOWN"
        }
        return switch.get(self.orientation)

    def updateOrientation(self, action):
        # TURN LEFT
        if action == Action.TURNLEFT:
            self.orientation = (self.orientation + 1) % 4
            print("orientation update value = " + str(self.orientation) + ", " + self.reprOrientation())
        # rotate == 2 => TURN RIGHT
        else:
            self.orientation = (self.orientation - 1) % 4
        return

    # update coordinates 
    def moveForward(self):
        self.prevLocation = [self.location[0], self.location[1]]
        # update current location
        # location[0] == x, location[1] == y
        if self.reprOrientation() == "LEFT":
            self.location[0] -= 1
        elif self.reprOrientation() == "RIGHT":
            self.location[0] += 1
        elif self.reprOrientation() == "UP":
            self.location[1] += 1
        # DOWN
        else:
            self.location[1] -= 1
        return
        
    def updateState(self, action):
        if action == Action.GOFORWARD:
            self.moveForward()
        elif action == Action.TURNLEFT:
            self.updateOrientation(action)
        elif action == Action.TURNRIGHT:
            self.updateOrientation(action)
        elif action == Action.SHOOT:
            self.gold = True
        return

    def updateWorldSize(self, newLocation):
        if newLocation[0] > self.worldSize[0] or newLocation[1] > self.worldSize[1]:
            self.worldSize[0] = max(newLocation[0], newLocation[1])
            self.worldSize[1] = self.worldSize[0]
        return

    def diagonalStench(self, currLocation):
        x, y = currLocation
        # top right diagonal
        if (x + 1, y + 1) in self.stenchLocations:
            # ? is UP safe
            if (x, y + 1) in self.safeLocations:
                self.wumpusLocation = [x + 1, y]
            # ? is RIGHT safe
            elif (x + 1, y) in self.safeLocations:
                self.wumpusLocation = [x, y + 1]
        # bottom left diagonal
        elif (x - 1, y - 1) in self.stenchLocations:
            # ? is LEFT safe
            if (x - 1, y) in self.safeLocations:
                self.wumpusLocation = [x, y - 1]
            # ? is BOTTOM safe
            elif (x, y - 1) in self.safeLocations:
                self.wumpusLocation = [x - 1, y]
        # bottom right diagonal
        elif (x + 1, y - 1) in self.stenchLocations:
            # ? is BOTTOM safe
            if (x, y - 1) in self.safeLocations:
                self.wumpusLocation = [x + 1, y]
            # ? is RIGHT safe
            elif (x + 1, y) in self.safeLocations:
                self.wumpusLocation = [x, y - 1]
        # top left diagonal
        elif (x - 1, y + 1) in self.stenchLocations:
            # ? is UP safe
            if (x, y + 1) in self.safeLocations:
                self.wumpusLocation = [x - 1, y]
            # ? is LEFT safe
            elif (x - 1, y) in self.safeLocations:
                self.wumpusLocation = [x, y + 1]
        return 

    def dumpStats(self):
       print("agent has gold? " + str(self.gold))
       print("stench locations = " + str(self.stenchLocations))
       print("breeze locations = " + str(self.breezeLocations))
       print("visited locations = " + str(self.visitedLocations))
       print("safe locations = " + str(self.safeLocations))
       print("orientation = " + str(self.orientation) + ", " + self.reprOrientation())
       print("worldSize = " + str(self.worldSize))
       print("location = " + str(self.location))
       print("prevLocation = " + str(self.prevLocation))
       print("gold Loc = " + str(self.goldLocation))
       print("wumpus location = " + str(self.wumpusLocation)) 

class Agent:
    def __init__(self):
        self.state = State()
        self.actionList = deque([])
        self.searchEngine = Search.SearchEngine()
    
    def __del__(self):
        pass

    def Initialize(self):
        # ** Reinitialize from either global variables or file 
        self.state.location = [1,1]
        self.state.orientation = Orientation.RIGHT
        self.state.prevLocation = []
        self.state.visitedLocations = set()
        self.state.gold = False
        self.actionList.clear()
        if self.state.goldLocation:
            self.actionList.extend(self.searchEngine.FindPath(self.state.location, self.state.orientation, self.state.goldLocation, Orientation.LEFT))
    
    # Input percept is a dictionary [perceptName: boolean]
    def Process (self, percept):
        # ** hit a wall go back to previous location
        if percept.bump:
            # TODO: update location
            self.state.location[0], self.state.location[1] = self.state.prevLocation[0], self.state.prevLocation[1]
            # ** if bump -> trying to go to a location outside of the board.MAXSIZE
            # TODO: need to delete that safe location
            self.removeOutOfBoardSafeLocations()
            # TODO: clear action list
            self.actionList.clear()
            # ** random int return odd or even i.e. 0 or 1
            # TODO: Add 1 => Action.TURNLEFT or Action.TURNRIGHT
            # ** Action.TURNLEFT == 1
            # ** Action.TURNRIGHT == 2
            action = (randint(0,100) % 2) + 1
            self.actionList.append(action)
        
        # ** get current location
        currLocation = tuple(self.state.location)

        print("is action list? = " + str(bool(self.actionList)))


        if not self.actionList:
            if not self.state.gold:                
                # ** update world size
                self.state.updateWorldSize(currLocation) 

                # TODO: add currLocation to safe locations
                self.state.safeLocations.add(currLocation)
                # TODO: add currLocation to visitedLocations
                self.state.visitedLocations.add(currLocation)
                # TODO: add safe locations to the search algorithm
                self.searchEngine.AddSafeLocation(currLocation[0], currLocation[1])

                if percept.stench:
                    # TODO: infer wumpus location
                    self.state.diagonalStench(currLocation)
                    # TODO: add currLocation to stenchLocation
                    self.state.stenchLocations.add(currLocation)
                if percept.breeze:
                    # TODO: add currlocation to breezeLocations
                    self.state.breezeLocations.add(currLocation)

                # ** found gold
                if percept.glitter:
                    self.actionList.append(Action.GRAB)
                    self.state.goldLocation = [self.state.location[0], self.state.location[1]]
                    print("heading towards = (1, 1)")
                    self.actionList.extend(self.searchEngine.FindPath([currLocation[0], currLocation[1]], self.state.orientation, [1,1], Orientation.LEFT))
                    self.actionList.append(Action.CLIMB)

                # ** No Danger perceived
                if percept.stench == 0 and percept.breeze == 0:
                    x, y = currLocation
                    # TODO: add neighbors to safe locations
                    # ** left neighbor
                    # TODO: check for known out of bounds
                    if (x - 1, y) not in self.state.removedSafeLocations:
                        if self.state.location[0] - 1 >= 1:
                            self.state.safeLocations.add(tuple([x-1, y]))
                            # TODO: add safe locations to the search algorithm
                            self.searchEngine.AddSafeLocation(x-1, y)
                    # ** down neighbor
                    if (x - 1, y) not in self.state.removedSafeLocations:
                        if self.state.location[1] - 1 >= 1:
                            self.state.safeLocations.add(tuple([x, y-1]))
                            self.searchEngine.AddSafeLocation(x, y-1)
                    # TODO: add right and up neighbors w/o reserve
                    # ** right neighbor
                    if (x + 1, y) not in self.state.removedSafeLocations:
                        self.state.safeLocations.add(tuple([x+1, y]))
                        self.searchEngine.AddSafeLocation(x+1, y)
                    # ** up neighbor
                    if (x, y + 1) not in self.state.removedSafeLocations:
                        self.state.safeLocations.add(tuple([x, y+1]))
                        self.searchEngine.AddSafeLocation(x, y+1)

                # ** action list is updated by gold
                if not self.actionList:
                    unvisitedSafeLocations = self.state.safeLocations - self.state.visitedLocations

                    if unvisitedSafeLocations:
                        # ** destination x, destination y
                        destX, destY = unvisitedSafeLocations.pop()
                        print("heading towards = ({0}, {1})".format(destX, destY))
                        self.actionList.extend(self.searchEngine.FindPath([currLocation[0], currLocation[1]], self.state.orientation, [destX, destY], self.state.orientation))
                    # ** no where to go
                    else:
                        # # same orientation bump
                        # if currLocation == tuple(self.state.prevLocation):
                        #     # ** random int return odd or even i.e. 0 or 1
                        #     # TODO: Add 1 => Action.TURNLEFT or Action.TURNRIGHT
                        #     # ** Action.TURNLEFT == 1
                        #     # ** Action.TURNRIGHT == 2
                        #     action = (randint(0,100) % 2) + 1
                        #     self.actionList.append(action)
                        # ! NEVER HAPPENs FOR TESTCASE
                        # TODO: default GOFORWARD
                        # else:
                        self.actionList.append(Action.GOFORWARD)
      
            # ? has gold but doesn't know what to do
            else:
                # TODO: start from whatever location & orientation you're in
                # TODO contd: return to origin and have orientation either down or left
                self.actionList.extend(self.searchEngine.FindPath([currLocation[0], currLocation[1]], self.state.orientation, [1,1], Orientation.LEFT))
                self.actionList.append(Action.CLIMB)
        
        self.state.dumpStats()
        print("actionList = " + str(self.actionList))
        action = self.actionList.popleft()
        print("action value on pop = " + str(action))
        # TODO: update location and orientation
        self.state.updateState(action)
        return action

        # ** call only upon percept.bump == 1
    def removeOutOfBoardSafeLocations(self):
        tempSet = set(self.state.safeLocations - self.state.visitedLocations)
        for x, y in tempSet:
            if x > self.state.worldSize[0] or y > self.state.worldSize[1]:
                self.state.safeLocations.remove((x, y))
                self.searchEngine.RemoveSafeLocation(x, y)
                self.state.removedSafeLocations.add((x,y))
        return
    
    def GameOver(self, score):
        pass
