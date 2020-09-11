# Agent.py

import Action
import Orientation
import random
from enum import Enum

class Location:
    def __init__(self, x=1, y=1):
        self.x = x
        self.y = y

    def __del__(self):
        pass

    # string representation
    def __repr__(self):
        return "({0}, {1})".format(self.x, self.y)

    def __eq__(self, location):
        if self.x == location.x and self.y == location.y:
            return True
        return False

    def setLocation(newLocation):
        self.x = newLocation.x
        self.y = newLocation.y

def Adjacent(loc1, loc2):
    x1, x2, y1, y2 = loc1.x, loc2.x, loc1.y, loc2.y
    if (x1 == x2 and abs(y1-y2) == 1) or (abs(x1-x2) == 1 and y1 == y2):
        return True
    return False

class State:
    def __init__(self):
        self.gold = False
        self.arrow = True
        self.location = Location()
        self.orientation = Orientation.RIGHT

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
        return switch[self.orientation]

class Agent:
    def __init__(self):
        self.state = State()
        # could replace prev Location by adding another function to moveBackwards based on Orientation
        self.prevLocation = Location()

    def __del__(self):
        pass

    def Initialize(self):
        pass

    def updateOrientation(self, rotate):
        # rotate LEFT
        if (rotate == 1):
            self.state.orientation = (self.state.orientation + 1) % 4
        # rotate == 2 => rotate RIGHT
        else:
            self.state.orientation = (self.state.orientation - 1) % 4

    # update coordinates 
    def moveForward(self):
        # set prev location = current location
        self.prevLocation.x = self.state.location.x
        self.prevLocation.y = self.state.location.y
        # update current location
        if self.state.reprOrientation() == "LEFT":
            self.state.location.x -= 1
        elif self.state.reprOrientation() == "RIGHT":
            self.state.location.x += 1
        elif self.state.reprOrientation() == "UP":
            self.state.location.y += 1
        # DOWN
        else:
            self.state.location.y -= 1

    def Process(self, percept):
        if percept.bump:
            # restore current location to prev location
            self.state.location.x = self.prevLocation.x
            self.state.location.y = self.prevLocation.y
        if percept.glitter:
            action = Action.GRAB
            self.state.gold = True
        # agent at (1,1) and has gold => CLIMB
        elif (self.state.location == Location()) and (self.state.gold == True):
            action = Action.CLIMB
        # agent has arrow, agent in top row => y = 4, agent's orientation RIGHT => SHOOT
        elif self.state.arrow is True and self.state.orientation == Orientation.RIGHT and self.state.location.y == 4:
            action = Action.SHOOT
            self.state.arrow = False
        # agent has arrow, agent in right most column => x = 4, agent's orientation UP => SHOOT
        elif self.state.arrow is True and self.state.orientation == Orientation.UP and self.state.location.x == 4:
            action = Action.SHOOT
            self.state.arrow = False
        else:
            #                               0           1          2
            # choose random action from {GOFORWARD, TURNLEFT, TURNRIGHT}
            action = random.randint(0,2)
            # GO FORWARD
            if action == 0:
                self.moveForward()
            # TURN RIGHT or LEFT
            elif action == 1 or action == 2:
                # keep track of orientation rotation
                self.updateOrientation(action)

        return action

    def GameOver(self, score):
        pass
