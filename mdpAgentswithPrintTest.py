# # -*-coding:utf-8-*-
# # coding=utf-8
# # mdpAgents.py
# # parsons/20-nov-2017
# #
# # Version 1
# #
# # The starting point for CW2.
# #
# # Intended to work with the PacMan AI projects from:
# #
# # http://ai.berkeley.edu/
# #
# # These use a simple API that allow us to control Pacman's interaction with
# # the environment adding a layer on top of the AI Berkeley code.
# #
# # As required by the licensing agreement for the PacMan AI we have:
# #
# # Licensing Information:  You are free to use or extend these projects for
# # educational purposes provided that (1) you do not distribute or publish
# # solutions, (2) you retain this notice, and (3) you provide clear
# # attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# #
# # Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# # The core projects and autograders were primarily created by John DeNero
# # (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# # Student side autograding was added by Brad Miller, Nick Hay, and
# # Pieter Abbeel (pabbeel@cs.berkeley.edu).
#
# # The agent here is was written by Simon Parsons, based on the code in
# # pacmanAgents.py
#
# from pacman import Directions
# from game import Agent
# import api
# import random
# import game
# import util
#
# # # Default
# # class MDPAgent(Agent):
# #
# #     # Constructor: this gets run when we first invoke pacman.py
# #     def __init__(self):
# #         print "Starting up MDPAgent!"
# #         name = "Pacman"
# #
# #     # Gets run after an MDPAgent object is created and once there is
# #     # game state to access.
# #     def registerInitialState(self, state):
# #         print "Running registerInitialState for MDPAgent!"
# #         print "I'm at:"
# #         print api.whereAmI(state)
# #
# #     # This is what gets run in between multiple games
# #     def final(self, state):
# #         print "Looks like the game just ended!"
# #
# #     # For now I just move randomly
# #     def getAction(self, state):
# #         # Get the actions we can try, and remove "STOP" if that is one of them.
# #         legal = api.legalActions(state)
# #         if Directions.STOP in legal:
# #             legal.remove(Directions.STOP)
# #         # Random choice between the legal options.
# #         return api.makeMove(random.choice(legal), legal)
#
# # class SatNav:
# #
# #     def __init__(self, state):
# #         # Number of Rows
# #         wall = api.walls(state)
# #         w = wall[-1][0] + 1
# #         self.row = w
# #         # Number of Columns
# #         h = wall[-1][1] + 1
# #         self.column = h
# #
# #         # Build up the map
# #         self.map = []
# #         while len(self.map) != self.row:
# #             self.map.append([0] * self.column)
# #         # Pacman location
# #         pac = api.whereAmI(state)
# #         self.map[pac[0]][pac[1]] = 'P'
# #         # Walls
# #         for x, y in wall:
# #             self.map[x][y] = '%'
# #         # Foods
# #         food = api.food(state)
# #         for x, y in food:
# #             self.map[x][y] = '*'
# #         # Ghosts
# #         ghost = api.ghosts(state)
# #         if ghost:
# #             for x, y in ghost:
# #                 self.map[x][y] = 'G'
# #         # Capsules
# #         capsule = api.capsules(state)
# #         if capsule:
# #             for x, y in capsule:
# #                 self.map[x][y] = 'C'
# #         # self.map = m
# #
# #         # Indexing systems
# #         self.freespace = self.Freespace()
# #         self.moves = self.legalMoves()
# #         self.utility = self.Utility()
# #         self.tableUtility = self.table_utility()
# #         self.policy = self.policyInit()
# #
# #     #
# #     # Parameters initialisation methods
# #     #
# #
# #     # 'Walkable' paths
# #     def Freespace(self):
# #         f = []
# #         for x in range(self.row):
# #             for y in range(self.column):
# #                 if self.map[x][y] != '%':
# #                     f.append((x, y))
# #         return f
# #
# #     # Utility values matrix initialisation
# #     def Utility(self):
# #         u = self.map
# #         for x in range(self.row):
# #             for y in range(self.column):
# #                 # Pacman & Walls
# #                 if u[x][y] == "P" or u[x][y] == "%":
# #                     u[x][y] = 0
# #                 # Foods
# #                 if u[x][y] == '*':
# #                     u[x][y] = 1
# #                 # Ghosts
# #                 if u[x][y] == 'G':
# #                     u[x][y] = -1
# #                 # Capsules
# #                 if u[x][y] == 'C':
# #                     u[x][y] = 10
# #         return u
# #
# #     # Action-next-state Utility values table
# #     def table_utility(self):
# #         # TABLE of UTILITY:
# #         tu = {}
# #         # Create a table that retrieve the utility value of next move with the format
# #         # tu[location][action] -> utility value
# #         #
# #         # Adding elements to the Nested Dictionary
# #         # From https://www.programiz.com/python-programming/nested-dictionary
# #         #
# #         for x, y in self.freespace:
# #             tu[(x, y)] = {}
# #             # NORTH
# #             if self.map[x][y + 1] != '%':
# #                 tu[(x, y)]['North'] = self.utility[x][y + 1]
# #             else:
# #                 tu[(x, y)]['North'] = self.utility[x][y]
# #             # EAST
# #             if self.map[x + 1][y] != '%':
# #                 tu[(x, y)]['East'] = self.utility[x + 1][y]
# #             else:
# #                 tu[(x, y)]['East'] = self.utility[x][y]
# #             # SOUTH
# #             if self.map[x][y - 1] != '%':
# #                 tu[(x, y)]['South'] = self.utility[x][y - 1]
# #             else:
# #                 tu[(x, y)]['South'] = self.utility[x][y]
# #             # WEST
# #             if self.map[x - 1][y] != '%':
# #                 tu[(x, y)]['West'] = self.utility[x - 1][y]
# #             else:
# #                 tu[(x, y)]['West'] = self.utility[x][y]
# #         return tu
# #
# #     # Initialise next-move guide
# #     def policyInit(self):
# #         p = {}
# #         for x, y in self.freespace:
# #             p[(x, y)] = 'East'
# #         return p
# #
# #     # Initialise the legal actions table
# #     def legalMoves(self):
# #         lm = {}
# #         for x, y in self.freespace:
# #             lm[(x, y)] = []
# #             # NORTH
# #             if self.map[x][y + 1] != '%':
# #                 lm[(x, y)].append('North')
# #             # EAST
# #             if self.map[x + 1][y] != '%':
# #                 lm[(x, y)].append('East')
# #             # SOUTH
# #             if self.map[x][y - 1] != '%':
# #                 lm[(x, y)].append('South')
# #             # WEST
# #             if self.map[x - 1][y] != '%':
# #                 lm[(x, y)].append('West')
# #         return lm
# #
# #     #
# #     # Value assignment methods
# #     #
# #
# #     # Print out the map
# #     def printmap(self):
# #         print 'Current map: '
# #         for i in range(self.row):
# #             for j in range(self.column):
# #                 print self.map[i][j],
# #             print '\n'
# #
# #     # Print out the utility matrix
# #     def printutility(self):
# #         print 'Utility values: '
# #         for x in range(self.row):
# #             for y in range(self.column):
# #                 print repr(round(self.utility[x][y], 3)).rjust(5),
# #             print '\n'
# #
# #     # Print out free grids
# #     def printfreespace(self):
# #         print 'Freespace: ',
# #         print self.freespace
# #
# #     # Update Utility values at new runtime
# #     def updateUtility(self, u_new):
# #         self.utility = u_new
# #
# #     # Update Table of Utility values at new runtime
# #     def updateUtilityTable(self, u_new):
# #         for x, y in self.freespace:
# #             if 'North' in self.moves[(x, y)]:
# #                 self.tableUtility[(x, y)]['North'] = u_new[x][y + 1]
# #             else:
# #                 self.tableUtility[(x, y)]['North'] = u_new[x][y]
# #             if 'East' in self.moves[(x, y)]:
# #                 self.tableUtility[(x, y)]['East'] = u_new[x + 1][y]
# #             else:
# #                 self.tableUtility[(x, y)]['East'] = u_new[x][y]
# #             if 'South' in self.moves[(x, y)]:
# #                 self.tableUtility[(x, y)]['South'] = u_new[x][y - 1]
# #             else:
# #                 self.tableUtility[(x, y)]['South'] = u_new[x][y]
# #             if 'West' in self.moves[(x, y)]:
# #                 self.tableUtility[(x, y)]['West'] = u_new[x - 1][y]
# #             else:
# #                 self.tableUtility[(x, y)]['West'] = u_new[x][y]
#
#
# # MDP Solver
# class MDPAgent(Agent):
#     # Constructor: this gets run when we first invoke pacman.py
#     def __init__(self):
#         print "Starting up MDPAgent!"
#         self.delta = 0.001  # Bellman factor: decides if the model converges
#         self.gamma = 0.5  # Discount factor: reduces the utility values with each time step
#         self.reward = -0.5  # Incentive for Pac-Man to keep moving
#
#     # Gets run after an MDPAgent object is created and once there is
#     # game state to access.
#     def registerInitialState(self, state):
#         # print "Running registerInitialState for MDPAgent!"
#         # print "I'm at: ", api.whereAmI(state)
#         print "\n======= Establishing new environment ========\n"
#         self.buildmap(state)
#         self.Freespace()
#         print "======= Map in registerInitialState: ========"
#         self.printmap()
#         self.legalMoves()
#         print "\n==== Ghost States ====\n"
#         self.ghoststate = api.ghostStates(state)
#         print self.ghoststate
#         print "\n==== Ghost Time Remain ====\n"
#         self.ghosttime = api.ghostStatesWithTimes(state)
#         print self.ghosttime, '\n'
#         print "==== Ghost Status Table ====\n"
#         self.ghoststatus = self.ghostStatus()
#         print self.ghoststatus, '\n'
#         # Something's wrong with the Utility table, once passed it, the Map turns into
#         # 导致出错的主要数据根源 utility
#         self.Utility(state)
#
#         self.table_utility()
#         self.policyInit()
#
#
#     # This is what gets run in between multiple games
#     def final(self, state):
#         print "Looks like the game just ended!"
#         # self.buildmap(state)
#         # self.Freespace()
#         # self.legalMoves()
#         # self.Utility(state)
#         # self.table_utility()
#         # self.policyInit()
#
#     #
#     # Data structures methods
#     #
#
#     # Map
#     def buildmap(self, state):
#         # Number of Rows
#         wall = api.walls(state)
#         w = wall[-1][0] + 1
#         self.row = w
#         # Number of Columns
#         h = wall[-1][1] + 1
#         self.column = h
#         self.map = []
#         while len(self.map) != self.row:
#             self.map.append([0] * self.column)
#         # Pacman location
#         pac = api.whereAmI(state)
#         self.map[pac[0]][pac[1]] = 'P'
#         # Walls
#         for x, y in wall:
#             self.map[x][y] = '%'
#         # Foods
#         food = api.food(state)
#         for x, y in food:
#             self.map[x][y] = '*'
#         # Capsules
#         capsule = api.capsules(state)
#         if capsule:
#             for x, y in capsule:
#                 self.map[x][y] = 'C'
#         # Ghosts
#         ghost = api.ghosts(state)
#         if ghost:
#             for x, y in ghost:
#                 self.map[int(x)][int(y)] = 'G'
#
#     # # Utility array v1
#     # def Utility(self):
#     #     print "====== Map BEFORE in Utility: ========="
#     #     self.printmap()
#     #     m = self.map
#     #     self.utility = m
#     #     for x in range(self.row):
#     #         for y in range(self.column):
#     #             # Pacman & Walls
#     #             if m[x][y] == "P" or m[x][y] == "%":
#     #                 self.utility[x][y] = 0
#     #             # Foods
#     #             if m[x][y] == '*':
#     #                 self.utility[x][y] = 0.1
#     #             # Ghosts
#     #             if m[x][y] == 'G':
#     #                 self.utility[x][y] = -30
#     #             # Capsules
#     #             if m[x][y] == 'C':
#     #                 self.utility[x][y] = 0.1
#     #     print "====== Map AFTER in Utility: ========="
#     #     self.printmap()
#
#     # Utility array v2
#     def Utility(self, state):
#         # print "====== Map BEFORE in Utility: ========="
#         # self.printmap()
#         self.utility = []
#         foods = api.food(state)
#         cap = api.capsules(state)
#         ghosts = api.ghosts(state)
#         f = self.freespace
#         print "===== Free Space ====="
#         print f
#         while len(self.utility) != self.row:
#             self.utility.append([0] * self.column)
#         for x, y in foods:
#             self.utility[x][y] = 0.1
#         for x, y in cap:
#             self.utility[x][y] = 10
#         # Hunting Mode change ghosts utility by checking EDIBLE status
#         # mediumClassic
#         if self.row > 8:
#             status = self.ghoststatus
#             # Keep yourself alive!
#             if not status[1]:
#                 for x, y in ghosts:
#                     self.utility[int(x)][int(y)] = -30
#                     # Ghosts dangerous perimeters
#                     # North
#                     if (x, y + 1) in f:
#                         self.utility[int(x)][int(y + 1)] = -30
#                     if (x, y + 2) in f:
#                         self.utility[int(x)][int(y + 2)] = -30
#                     # NorthEast
#                     if (x + 1, y + 1) in f:
#                         self.utility[int(x + 1)][int(y + 1)] = -30
#                     if (x + 1, y + 2) in f:
#                         self.utility[int(x + 1)][int(y + 2)] = -30
#                     if (x + 2, y + 1) in f:
#                         self.utility[int(x + 2)][int(y + 1)] = -30
#                     # East
#                     if (x + 1, y) in f:
#                         self.utility[int(x + 1)][int(y)] = -30
#                     if (x + 2, y) in f:
#                         self.utility[int(x + 2)][int(y)] = -30
#                     # SouthEast
#                     if (x + 1, y - 1) in f:
#                         self.utility[int(x + 1)][int(y - 1)] = -30
#                     if (x + 1, y - 2) in f:
#                         self.utility[int(x + 1)][int(y - 2)] = -30
#                     if (x + 2, y - 1) in f:
#                         self.utility[int(x + 2)][int(y - 1)] = -30
#                     # South
#                     if (x, y - 1) in f:
#                         self.utility[int(x)][int(y - 1)] = -30
#                     if (x, y - 2) in f:
#                         self.utility[int(x)][int(y - 2)] = -30
#                     # SouthWest
#                     if (x - 1, y - 1) in f:
#                         self.utility[int(x - 1)][int(y - 1)] = -30
#                     if (x - 1, y - 2) in f:
#                         self.utility[int(x - 1)][int(y - 2)] = -30
#                     if (x - 2, y - 1) in f:
#                         self.utility[int(x - 2)][int(y - 1)] = -30
#                     # West
#                     if (x - 1, y) in f:
#                         self.utility[int(x - 1)][int(y)] = -30
#                     if (x - 2, y) in f:
#                         self.utility[int(x - 2)][int(y)] = -30
#                     # NorthWest
#                     if (x - 1, y + 1) in f:
#                         self.utility[int(x - 1)][int(y + 1)] = -30
#                     if (x - 1, y + 2) in f:
#                         self.utility[int(x - 1)][int(y + 2)] = -30
#                     if (x - 2, y + 1) in f:
#                         self.utility[int(x - 2)][int(y + 1)] = -30
#             # Ghosts are scared!
#             else:
#                 if self.ghosttime[0][1] > 3:
#                     # Edible ghosts
#                     for x, y in foods:
#                         self.utility[x][y] = 0
#                     for x, y in cap:
#                         self.utility[x][y] = 0
#                     for x, y in status[1]:
#                         self.utility[int(x)][int(y)] = 30
#                     # Dangerous ghosts
#                     for x, y in status[0]:
#                         self.utility[int(x)][int(y)] = -30
#                         # Ghosts dangerous perimeters
#                         # North
#                         if (x, y + 1) in f:
#                             self.utility[int(x)][int(y + 1)] = -30
#                         if (x, y + 2) in f:
#                             self.utility[int(x)][int(y + 2)] = -30
#                         # NorthEast
#                         if (x + 1, y + 1) in f:
#                             self.utility[int(x + 1)][int(y + 1)] = -30
#                         if (x + 1, y + 2) in f:
#                             self.utility[int(x + 1)][int(y + 2)] = -30
#                         if (x + 2, y + 1) in f:
#                             self.utility[int(x + 2)][int(y + 1)] = -30
#                         # East
#                         if (x + 1, y) in f:
#                             self.utility[int(x + 1)][int(y)] = -30
#                         if (x + 2, y) in f:
#                             self.utility[int(x + 2)][int(y)] = -30
#                         # SouthEast
#                         if (x + 1, y - 1) in f:
#                             self.utility[int(x + 1)][int(y - 1)] = -30
#                         if (x + 1, y - 2) in f:
#                             self.utility[int(x + 1)][int(y - 2)] = -30
#                         if (x + 2, y - 1) in f:
#                             self.utility[int(x + 2)][int(y - 1)] = -30
#                         # South
#                         if (x, y - 1) in f:
#                             self.utility[int(x)][int(y - 1)] = -30
#                         if (x, y - 2) in f:
#                             self.utility[int(x)][int(y - 2)] = -30
#                         # SouthWest
#                         if (x - 1, y - 1) in f:
#                             self.utility[int(x - 1)][int(y - 1)] = -30
#                         if (x - 1, y - 2) in f:
#                             self.utility[int(x - 1)][int(y - 2)] = -30
#                         if (x - 2, y - 1) in f:
#                             self.utility[int(x - 2)][int(y - 1)] = -30
#                         # West
#                         if (x - 1, y) in f:
#                             self.utility[int(x - 1)][int(y)] = -30
#                         if (x - 2, y) in f:
#                             self.utility[int(x - 2)][int(y)] = -30
#                         # NorthWest
#                         if (x - 1, y + 1) in f:
#                             self.utility[int(x - 1)][int(y + 1)] = -30
#                         if (x - 1, y + 2) in f:
#                             self.utility[int(x - 1)][int(y + 2)] = -30
#                         if (x - 2, y + 1) in f:
#                             self.utility[int(x - 2)][int(y + 1)] = -30
#         # smallGrid
#         else:
#             for x, y in ghosts:
#                 self.utility[int(x)][int(y)] = -30
#                 # Ghosts dangerous perimeters
#                 # North
#                 # if (x, y + 1) in f:
#                 #     self.utility[int(x)][int(y + 1)] = -30
#                 # if (x, y + 2) in f:
#                 #     self.utility[int(x)][int(y + 2)] = -30
#                 # if (x, y + 3) in f:
#                 #     self.utility[int(x)][int(y + 3)] = -30
#                 # NorthEast
#                 # if (x + 1, y + 1) in f:
#                 #     self.utility[int(x + 1)][int(y + 1)] = -30
#                 # if (x + 1, y + 2) in f:
#                 #     self.utility[int(x + 1)][int(y + 2)] = -30
#                 # if (x + 2, y + 1) in f:
#                 #     self.utility[int(x + 2)][int(y + 1)] = -30
#                 # East
#                 # if (x + 1, y) in f:
#                 #     self.utility[int(x + 1)][int(y)] = -30
#                 # if (x + 2, y) in f:
#                 #     self.utility[int(x + 2)][int(y)] = -30
#                 # if (x + 3, y) in f:
#                 #     self.utility[int(x + 3)][int(y)] = -30
#                 # SouthEast
#                 # if (x + 1, y - 1) in f:
#                 #     self.utility[int(x + 1)][int(y - 1)] = -30
#                 # if (x + 1, y - 2) in f:
#                 #     self.utility[int(x + 1)][int(y - 2)] = -30
#                 # if (x + 2, y - 1) in f:
#                 #     self.utility[int(x + 2)][int(y - 1)] = -30
#                 # South
#                 # if (x, y - 1) in f:
#                 #     self.utility[int(x)][int(y - 1)] = -30
#                 # if (x, y - 2) in f:
#                 #     self.utility[int(x)][int(y - 2)] = -30
#                 # if (x, y - 3) in f:
#                 #     self.utility[int(x)][int(y - 3)] = -30
#                 # SouthWest
#                 if (x - 1, y - 1) in f:
#                     self.utility[int(x - 1)][int(y - 1)] = -30
#                 if (x - 1, y - 2) in f:
#                     self.utility[int(x - 1)][int(y - 2)] = -30
#                 # if (x - 2, y - 1) in f:
#                 #     self.utility[int(x - 2)][int(y - 1)] = -30
#                 # West
#                 # if (x - 1, y) in f:
#                 #     self.utility[int(x - 1)][int(y)] = -30
#                 # if (x - 2, y) in f:
#                 #     self.utility[int(x - 2)][int(y)] = -30
#                 # if (x - 3, y) in f:
#                 #     self.utility[int(x - 3)][int(y)] = -30
#                 # NorthWest
#                 # if (x - 1, y + 1) in f:
#                 #     self.utility[int(x - 1)][int(y + 1)] = -30
#                 # if (x - 1, y + 2) in f:
#                 #     self.utility[int(x - 1)][int(y + 2)] = -30
#                 # if (x - 2, y + 1) in f:
#                 #     self.utility[int(x - 2)][int(y + 1)] = -30
#         # print "====== Map AFTER in Utility: ========="
#         # self.printmap()
#         print "====== NEW UTILITY ======="
#         self.printutility()
#
#     # Free space
#     def Freespace(self):
#         self.freespace = []
#         for x in range(self.row):
#             for y in range(self.column):
#                 if self.map[x][y] != '%':
#                     self.freespace.append((x, y))
#         # print "========= Map in Freespace: =========="
#         # self.printmap()
#         # print "Freespace: ", self.freespace
#
#     # Legal moves at each state
#     def legalMoves(self):
#         self.availMoves = {}
#         # print "========= Map in legalMoves: ==========="
#         # self.printmap()
#         m = self.map
#         # print "===== Map in legalMoves ====="
#         # self.printmap()
#         # print "=== Freespace in legalMoves: ==="
#         # print self.freespace
#         for x, y in self.freespace:
#             self.availMoves[(x, y)] = []
#             # NORTH
#             if m[x][y + 1] != '%':  # and m[x][y + 1] != 'G'
#                 self.availMoves[(x, y)].append('North')
#             # EAST
#             if m[x + 1][y] != '%':  # and m[x + 1][y] != 'G'
#                 self.availMoves[(x, y)].append('East')
#             # SOUTH
#             if m[x][y - 1] != '%':  # and m[x][y - 1] != 'G'
#                 self.availMoves[(x, y)].append('South')
#             # WEST
#             if m[x - 1][y] != '%':   # and m[x - 1][y] != 'G':
#                 self.availMoves[(x, y)].append('West')
#         # Overseeing workspace
#         # print repr(self.availMoves)
#
#     # Table of Utility: legal moves utility & illegal moves 'still'
#     def table_utility(self):
#         # TABLE of UTILITY:
#         self.tableUtility = {}
#         # print "========= Map in table_utlity: ==========="
#         # self.printmap()
#         # Create a table that retrieve the utility value of next move with the format
#         # tu[location][action] -> utility value
#         #
#         # Adding elements to the Nested Dictionary
#         # From https://www.programiz.com/python-programming/nested-dictionary
#         #
#         for x, y in self.freespace:
#             self.tableUtility[(x, y)] = {}
#             # NORTH
#             if self.map[x][y + 1] != '%':
#                 self.tableUtility[(x, y)]['North'] = self.utility[x][y + 1]
#             else:
#                 self.tableUtility[(x, y)]['North'] = self.utility[x][y]
#             # EAST
#             if self.map[x + 1][y] != '%':
#                 self.tableUtility[(x, y)]['East'] = self.utility[x + 1][y]
#             else:
#                 self.tableUtility[(x, y)]['East'] = self.utility[x][y]
#             # SOUTH
#             if self.map[x][y - 1] != '%':
#                 self.tableUtility[(x, y)]['South'] = self.utility[x][y - 1]
#             else:
#                 self.tableUtility[(x, y)]['South'] = self.utility[x][y]
#             # WEST
#             if self.map[x - 1][y] != '%':
#                 self.tableUtility[(x, y)]['West'] = self.utility[x - 1][y]
#             else:
#                 self.tableUtility[(x, y)]['West'] = self.utility[x][y]
#         # self.tableUtility = tu
#         # Overseeing workspace
#         # print repr(self.tableUtility)
#
#     # Global policy
#     def policyInit(self):
#         p = {}
#         for x, y in self.freespace:
#             p[(x, y)] = 'East'
#         self.policy = p
#
#     # Ghost Status
#     def ghostStatus(self):
#         status = {0: [], 1: []}
#         for gh, st in self.ghoststate:
#             status[st].append(gh)
#         return status
#
#     #
#     # Data Update methods
#     #
#     def updateUtilityTable(self, nu):
#         for x, y in self.freespace:
#             if 'North' in self.availMoves[(x, y)]:
#                 self.tableUtility[(x, y)]['North'] = nu[x][y + 1]
#             else:
#                 self.tableUtility[(x, y)]['North'] = nu[x][y]
#             if 'East' in self.availMoves[(x, y)]:
#                 self.tableUtility[(x, y)]['East'] = nu[x + 1][y]
#             else:
#                 self.tableUtility[(x, y)]['East'] = nu[x][y]
#             if 'South' in self.availMoves[(x, y)]:
#                 self.tableUtility[(x, y)]['South'] = nu[x][y - 1]
#             else:
#                 self.tableUtility[(x, y)]['South'] = nu[x][y]
#             if 'West' in self.availMoves[(x, y)]:
#                 self.tableUtility[(x, y)]['West'] = nu[x - 1][y]
#             else:
#                 self.tableUtility[(x, y)]['West'] = nu[x][y]
#
#     #
#     # Print methods
#     #
#     # Print map
#     def printmap(self):
#         print 'Current Environment: '
#         for i in range(self.row):
#             for j in range(self.column):
#                 print self.map[i][j],
#             print '\n'
#
#     # Print Utility
#     def printutility(self):
#         print "Utility: "
#         for i in range(self.row):
#             for j in range(self.column):
#                 print repr(round(self.utility[i][j], 3)).rjust(7),
#             print '\n'
#
#     # Print out free grids
#     def printfreespace(self):
#         print 'Freespace: ',
#         print self.freespace
#
#     #
#     # Value Iteration methods
#     #
#     # Bellman function
#     def bellman(self, ns):  # ns -> N States: tuple(x, y)
#         tu = self.tableUtility
#         u = {}
#         # Loop over legal actions
#         for action in self.availMoves[ns]:
#             u[action] = 0.8 * tu[ns][action]
#             if action == 'North' or action == 'South':
#                 u[action] += 0.1 * (tu[ns]['East'] + tu[ns]['West'])
#             if action == 'East' or action == 'West':
#                 u[action] += 0.1 * (tu[ns]['North'] + tu[ns]['South'])
#             u[action] = self.reward + self.gamma * u[action]
#         v = list(u.values())
#         k = list(u.keys())
#         # If all actions have the same utility? Shouldn't have same utility at the end of algorithm
#         return max(v), k[v.index(max(v))]
#
#     # Value iteration algorithm: return current optimal policy
#     def valueIteration(self, state):
#         # maxdiff = -1e9
#         print "==== Value Iteration Algorithm ===="
#         # u_old = self.utility
#         u = self.utility
#         p = self.policy
#         print "==== TEST 1 ===="
#         foods = api.food(state)
#         ghosts = api.ghosts(state)
#         g = api.ghosts(state)
#         cap = api.capsules(state)
#         print "==== TEST 2 ===="
#         f = self.freespace
#         print "==== TEST 3 ===="
#         # Ghosts dangerous perimeters
#         # V1: Manipulate food list
#         # pass
#         # for x, y in ghosts:
#         #     # North
#         #     if (x, y + 1) in foods:
#         #         foods.remove((x, y + 1))
#         #     if (x, y + 1) in cap:
#         #         cap.remove((x, y + 1))
#         #     # NorthEast
#         #     if (x + 1, y + 1) in foods:
#         #         foods.remove((x + 1, y + 1))
#         #     if (x + 1, y + 1) in cap:
#         #         cap.remove((x + 1, y + 1))
#         #     if (x + 1, y + 2) in foods:
#         #         foods.remove((x + 1, y + 2))
#         #     if (x + 1, y + 2) in cap:
#         #         cap.remove((x + 1, y + 2))
#         #     # East
#         #     if (x + 1, y) in foods:
#         #         foods.remove((x + 1, y))
#         #     if (x + 1, y) in cap:
#         #         cap.remove((x + 1, y))
#         #     # SouthEast
#         #     if (x + 1, y - 1) in foods:
#         #         foods.remove((x + 1, y - 1))
#         #     if (x + 1, y - 1) in cap:
#         #         cap.remove((x + 1, y - 1))
#         #     if (x + 1, y - 2) in foods:
#         #         foods.remove((x + 1, y - 2))
#         #     if (x + 1, y - 2) in cap:
#         #         cap.remove((x + 1, y - 2))
#         #     # South
#         #     if (x, y - 1) in foods:
#         #         foods.remove((x, y - 1))
#         #     if (x, y - 1) in cap:
#         #         cap.remove((x, y - 1))
#         #     # SouthWest
#         #     if (x - 1, y - 1) in foods:
#         #         foods.remove((x - 1, y - 1))
#         #     if (x - 1, y - 1) in cap:
#         #         cap.remove((x - 1, y - 1))
#         #     if (x - 1, y - 2) in foods:
#         #         foods.remove((x - 1, y - 2))
#         #     if (x - 1, y - 2) in cap:
#         #         cap.remove((x - 1, y - 2))
#         #     # West
#         #     if (x - 1, y) in foods:
#         #         foods.remove((x - 1, y))
#         #     if (x - 1, y) in cap:
#         #         cap.remove((x - 1, y))
#         #     # NorthWest
#         #     if (x - 1, y + 1) in foods:
#         #         foods.remove((x - 1, y + 1))
#         #     if (x - 1, y + 1) in cap:
#         #         cap.remove((x - 1, y + 1))
#         #     if (x - 1, y + 2) in foods:
#         #         foods.remove((x - 1, y + 2))
#         #     if (x - 1, y + 2) in cap:
#         #         cap.remove((x - 1, y + 2))
#
#         # pass
#         # Ghosts dangerous perimeters
#         # V2: Manipulate Ghost list
#         print "==== TEST 4 ===="
#         # mediumClassic
#         if self.row > 8:
#             # Keep yourself alive!
#             for x, y in g:
#                 x = int(x)
#                 y = int(y)
#                 # North
#                 print "==== TEST 5 ===="
#                 if (x, y + 1) in f:
#                     ghosts.append((x, y + 1))
#                 # if (x, y + 2) in f:
#                 #     ghosts.append((x, y + 2))
#                 # NorthEast
#                 # if (x + 1, y + 1) in f:
#                 #     ghosts.append((x + 1, y + 1))
#                 # if (x + 1, y + 2) in f:
#                 #     ghosts.append((x + 1, y + 2))
#                 # if (x + 2, y + 1) in f:
#                 #     ghosts.append((x + 1, y + 2))
#                 # East
#                 if (x + 1, y) in f:
#                     ghosts.append((x + 1, y))
#                 # if (x + 2, y) in f:
#                 #     ghosts.append((x + 2, y))
#                 # SouthEast
#                 # if (x + 1, y - 1) in f:
#                 #     ghosts.append((x + 1, y - 1))
#                 # if (x + 1, y - 2) in f:
#                 #     ghosts.append((x + 1, y - 2))
#                 # if (x + 2, y - 1) in f:
#                 #     ghosts.append((x + 1, y - 1))
#                 # South
#                 if (x, y - 1) in f:
#                     ghosts.append((x, y - 1))
#                 # if (x, y - 2) in f:
#                 #     ghosts.append((x, y - 2))
#                 # SouthWest
#                 # if (x - 1, y - 1) in f:
#                 #     ghosts.append((x - 1, y - 1))
#                 # if (x - 1, y - 2) in f:
#                 #     ghosts.append((x - 1, y - 2))
#                 # if (x - 2, y - 1) in f:
#                 #     ghosts.append((x - 2, y - 1))
#                 # West
#                 if (x - 1, y) in f:
#                     ghosts.append((x - 1, y))
#                 # if (x - 2, y) in f:
#                 #     ghosts.append((x - 2, y))
#                 # NorthWest
#                 # if (x - 1, y + 1) in f:
#                 #     ghosts.append((x - 1, y - 1))
#                 # if (x - 1, y + 2) in f:
#                 #     ghosts.append((x - 1, y + 2))
#                 # if (x - 2, y + 1) in f:
#                 #     ghosts.append((x - 2, y + 1))
#         # smallGrid
#         else:
#             status = [0, 0]
#             for x, y in g:
#                 # North
#                 print "==== TEST 5 ===="
#                 # if (x, y + 1) in f:
#                 #     ghosts.append((x, y + 1))
#                 # if (x, y + 2) in f:
#                 #     ghosts.append((x, y + 2))
#                 # NorthEast
#                 # if (x + 1, y + 1) in f:
#                 #     ghosts.append((x + 1, y + 1))
#                 # if (x + 1, y + 2) in f:
#                 #     ghosts.append((x + 1, y + 2))
#                 # if (x + 2, y + 1) in f:
#                 #     ghosts.append((x + 1, y + 2))
#                 # East
#                 # if (x + 1, y) in f:
#                 #     ghosts.append((x + 1, y))
#                 # if (x + 2, y) in f:
#                 #     ghosts.append((x + 2, y))
#                 # SouthEast
#                 # if (x + 1, y - 1) in f:
#                 #     ghosts.append((x + 1, y - 1))
#                 # if (x + 1, y - 2) in f:
#                 #     ghosts.append((x + 1, y - 2))
#                 # if (x + 2, y - 1) in f:
#                 #     ghosts.append((x + 1, y - 1))
#                 # SouthWest
#                 if (x - 1, y - 1) in f:
#                     ghosts.append((x - 1, y - 1))
#                 if (x - 1, y - 2) in f:
#                     ghosts.append((x, y - 2))
#                 # SouthWest
#                 # if (x - 1, y - 1) in f:
#                 #     ghosts.append((x - 1, y - 1))
#                 # if (x - 1, y - 2) in f:
#                 #     ghosts.append((x - 1, y - 2))
#                 # if (x - 2, y - 1) in f:
#                 #     ghosts.append((x - 2, y - 1))
#                 # West
#                 # if (x - 1, y) in f:
#                 #     ghosts.append((x - 1, y))
#                 # if (x - 2, y) in f:
#                 #     ghosts.append((x - 2, y))
#                 # NorthWest
#                 # if (x - 1, y + 1) in f:
#                 #     ghosts.append((x - 1, y - 1))
#                 # if (x - 1, y + 2) in f:
#                 #     ghosts.append((x - 1, y + 2))
#                 # if (x - 2, y + 1) in f:
#                 #     ghosts.append((x - 2, y + 1))
#         # print "== Save Zone Built =="
#         # print ghosts
#         c = 0
#         # Algorithm body
#         # Iterating until the maximum difference between iteration < delta(threshold)
#         print "\n== Ghost List in VI ==\n"
#         print ghosts
#         print "== Start Iterations ==\n"
#         while True:
#             # Iteration starts
#             c += 1
#             # print "Entered Iteration", c
#             # Go through all states except foods, capsules & ghosts positions
#             for s in f:
#                 if (s in foods) or (s in list(set(ghosts))) or (s in cap):
#                     continue
#                 x = s[0]
#                 y = s[1]
#                 # if (s in foods) or (s in cap):
#                 #     if u[x][y] != -30:
#                 #         continue
#                 u[x][y], p[s] = self.bellman(s)
#             # Check if values converge. If so, determine the optimal policy
#             # Maximum Expected Utility (MEU)
#             # for x in range(self.row):
#             #     for y in range(self.column):
#             #         maxdiff = max(maxdiff, abs(u[x][y] - u_old[x][y]))
#             # print "Maximum Difference: ", maxdiff
#             # u_old = u  # U_i+1 <- U_i
#             print "=== Iteration ", c, " ==="
#             self.updateUtilityTable(u)  # U_i+1 <- U_i
#             self.utility = u
#             self.policy = p
#             self.printutility()
#             # 循环出口：只循环了一次？？
#             # Shouldn't have same utility at the end of algorithm
#             # if maxdiff < self.delta:
#             # if maxdiff <= self.delta:
#             #     break
#             if c > 20:
#                 break
#
#         pacman = api.whereAmI(state)
#         Legal = self.availMoves[pacman]
#         x = pacman[0]
#         y = pacman[1]
#         #
#         # Maximum Expected Utility
#         #
#         radar = {}
#         for direct in Legal:
#             if direct == 'North':
#                 radar['North'] = []
#                 if (x, y + 1) in f:
#                     radar['North'].append(u[x][y + 1])
#                 if (x, y + 2) in f:
#                     radar['North'].append(u[x][y + 2])
#                 if (x, y + 3) in f:
#                     radar['North'].append(u[x][y + 3])
#                 # Corner Issue
#                 if len(radar['North']) <= 1:
#                     p = x
#                     q = y + 1
#                     safe = self.availMoves[(p, q)]
#                     for sf in safe:
#                         if sf == 'East':
#                             if (p + 1, q) in f:
#                                 radar['North'].append(u[p + 1][q])
#                             if (p + 2, q) in f:
#                                 radar['North'].append(u[p + 2][q])
#                             # if (p + 3, q) in f:
#                             #     radar['North'].append(u[p + 3][q])
#                         if sf == 'West':
#                             if (p - 1, q) in f:
#                                 radar['North'].append(u[p - 1][q])
#                             if (p - 2, q) in f:
#                                 radar['North'].append(u[p - 2][q])
#                             # if (p - 3, q) in f:
#                             #     radar['North'].append(u[p - 3][q])
#                     radar['North'] = float(sum(radar['North'])) / len(radar['North'])
#                 else:
#                     radar['North'] = float(sum(radar['North'])) / len(radar['North'])
#             if direct == 'East':
#                 radar['East'] = []
#                 if (x + 1, y) in f:
#                     radar['East'].append(u[x + 1][y])
#                 if (x + 2, y) in f:
#                     radar['East'].append(u[x + 2][y])
#                 if (x + 3, y) in f:
#                     radar['East'].append(u[x + 3][y])
#                 # Corner Issue
#                 if len(radar['East']) <= 1:
#                     p = x + 1
#                     q = y
#                     safe = self.availMoves[(p, q)]
#                     for sf in safe:
#                         if sf == 'North':
#                             if (p, q + 1) in f:
#                                 radar['East'].append(u[p][q + 1])
#                             if (p, q + 2) in f:
#                                 radar['East'].append(u[p][q + 2])
#                             # if (p, q + 3) in f:
#                             #     radar['East'].append(u[p][q + 3])
#                         if sf == 'South':
#                             if (p, q - 1) in f:
#                                 radar['East'].append(u[p][q - 1])
#                             if (p, q - 2) in f:
#                                 radar['East'].append(u[p][q - 2])
#                             # if (p, q - 3) in f:
#                             #     radar['East'].append(u[p][q - 3])
#                     radar['East'] = float(sum(radar['East'])) / len(radar['East'])
#                 else:
#                     radar['East'] = float(sum(radar['East'])) / len(radar['East'])
#             if direct == 'South':
#                 radar['South'] = []
#                 if (x, y - 1) in f:
#                     radar['South'].append(u[x][y - 1])
#                 if (x, y - 2) in f:
#                     radar['South'].append(u[x][y - 2])
#                 if (x, y - 3) in f:
#                     radar['South'].append(u[x][y - 3])
#                 # Corner Issue
#                 if len(radar['South']) <= 1:
#                     p = x
#                     q = y - 1
#                     safe = self.availMoves[(p, q)]
#                     for sf in safe:
#                         if sf == 'East':
#                             if (p + 1, q) in f:
#                                 radar['South'].append(u[p + 1][q])
#                             if (p + 2, q) in f:
#                                 radar['South'].append(u[p + 2][q])
#                             # if (p + 3, q) in f:
#                             #     radar['South'].append(u[p + 3][q])
#                         if sf == 'West':
#                             if (p - 1, q) in f:
#                                 radar['South'].append(u[p - 1][q])
#                             if (p - 2, q) in f:
#                                 radar['South'].append(u[p - 2][q])
#                             # if (p - 3, q) in f:
#                             #     radar['South'].append(u[p - 3][q])
#                     radar['South'] = float(sum(radar['South'])) / len(radar['South'])
#                 else:
#                     radar['South'] = float(sum(radar['South'])) / len(radar['South'])
#             if direct == 'West':
#                 radar['West'] = []
#                 if (x - 1, y) in f:
#                     radar['West'].append(u[x - 1][y])
#                 if (x - 2, y) in f:
#                     radar['West'].append(u[x - 2][y])
#                 if (x - 3, y) in f:
#                     radar['West'].append(u[x - 3][y])
#                 # Corner Issue
#                 if len(radar['West']) <= 1:
#                     p = x - 1
#                     q = y
#                     safe = self.availMoves[(p, q)]
#                     for sf in safe:
#                         if sf == 'North':
#                             if (p, q + 1) in f:
#                                 radar['West'].append(u[p][q + 1])
#                             if (p, q + 2) in f:
#                                 radar['West'].append(u[p][q + 2])
#                             # if (p, q + 3) in f:
#                             #     radar['West'].append(u[p][q + 3])
#                         if sf == 'South':
#                             if (p, q - 1) in f:
#                                 radar['West'].append(u[p][q - 1])
#                             if (p, q - 2) in f:
#                                 radar['West'].append(u[p][q - 2])
#                             # if (p, q - 3) in f:
#                             #     radar['West'].append(u[p][q - 3])
#                     radar['West'] = float(sum(radar['West'])) / len(radar['West'])
#                 else:
#                     radar['West'] = float(sum(radar['West'])) / len(radar['West'])
#         print "===== RADAR =====\n"
#         print radar, '\n'
#         vr = list(radar.values())
#         vk = list(radar.keys())
#         print "===== Chosen Action =====\n"
#         print '  === ', vk[vr.index(max(vr))], ' ===', '\n'
#         # Maximum Expected Utility (MEU)
#         # WRONG!!!!!!!!
#         # Maybe take AVG of 3 available grids on either sides
#         # moves = self.tableUtility[pacman]
#         # v = list(moves.values())
#         # k = list(moves.keys())
#         # if not v:
#         #     print "\nEmpty actions, go random\n"
#         #     a = ['West', 'North', 'East', "South"]
#         #     return random.choice(a)
#         # print "Best move is: ", k[v.index(max(v))]
#         # print '\n'
#         # return k[v.index(max(v))]
#         return vk[vr.index(max(vr))]
#
#     #
#     # Main function
#     #
#     def getAction(self, state):
#         # Update Map & utility values after each runtime according to realtime environment
#         # pacsmap = SatNav(state)
#         print "======================================================="
#         print "===================== NEW STATE ======================="
#         print "======================================================="
#         self.registerInitialState(state)
#         # cap = api.capsules(state)
#         # self.buildmap(state)
#         # print "=== Get Action Map ==="
#         # self.printmap()
#         # self.printfreespace()
#         # self.printutility()
#         # Get the actions we can try, and remove "STOP" if that is one of them.
#         legal = api.legalActions(state)
#         if Directions.STOP in legal:
#             legal.remove(Directions.STOP)
#         action = self.valueIteration(state)
#
#         # self.printutility()
#         # if action not in legal:
#         #     return api.makeMove(random.choice(legal), legal)
#         return api.makeMove(action, legal)
#
# # Same values area action random selection
# # Detect legal moves
#
# # SensingAgent
# #
# # Doesn't move, but reports sensory data available to Pacman
# class SensingAgent(Agent):
#
#     def getAction(self, state):
#
#         # Demonstrates the information that Pacman can access about the state
#         # of the game.
#
#         # What are the current moves available
#         legal = api.legalActions(state)
#         print "Legal moves: ", legal
#
#         # Where is Pacman?
#         pacman = api.whereAmI(state)
#         print "Pacman position: ", pacman
#
#         # Where are the ghosts?
#         print "Ghost positions:"
#         theGhosts = api.ghosts(state)
#         for i in range(len(theGhosts)):
#             print theGhosts[i]
#
#         # How far away are the ghosts?
#         print "Distance to ghosts:"
#         for i in range(len(theGhosts)):
#             print util.manhattanDistance(pacman, theGhosts[i])
#
#         # Where are the capsules?
#         print "Capsule locations:"
#         print api.capsules(state)
#
#         # Where is the food?
#         print "Food locations: "
#         print api.food(state)
#
#         # Where are the walls?
#         print "Wall locations: "
#         print api.walls(state)
#
#         # getAction has to return a move. Here we pass "STOP" to the
#         # API to ask Pacman to stay where they are.
#         return api.makeMove(Directions.STOP, legal)
