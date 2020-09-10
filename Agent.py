# Agent.py

import Action
from enum import Enum

class Orientation(Enum):
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3

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

def Adjacent(loc1, loc2) -> bool:
    x1, x2, y1, y2 = loc1.x, loc2.x, loc1.y, loc2.y
    if (x1 == x2 and abs(y1-y2) == 1) or (abs(x1-x2) == 1 and y1 == y2):
        return True
    return False



# class Agent:
#     def __init__(self):
#         pass

#     def __del__(self):
#         pass

#     def Initialize(self):
#         pass

#     def Process(self, percept):
#         valid_action = False
#         while not valid_action:
#             valid_action = True
#             if percept.glitter:
#                 action = Action.GRAB
#             # agent at (1,1) and has gold => CLIMB
#             elif location:
#                 action = Action.CLIMB
#             elif location:
#                 agent = Action.SHOOT
#             elif location:
#                 agent = Action.SHOOT
#             else:
#                 pass
#                 #     c = raw_input("Action? ") # Python 2 (replace raw_input with input for Python 3)
#                 #     if c == 'f':
#                 #         action = Action.GOFORWARD
#                 #     elif c == 'l':
#                 #         action = Action.TURNLEFT
#                 #     elif c == 'r':
#                 #         action = Action.TURNRIGHT
#                 #     elif c == 'g':
#                 #         action = Action.GRAB
#                 #     elif c == 's':
#                 #         action = Action.SHOOT
#                 #     elif c == 'c':
#                 #         action = Action.CLIMB
#                 #     else:
#                 #         print("Huh?")
#                 #         valid_action = False
#         return action

#     def GameOver(self, score):
#         pass
