# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent
import random

class MyAI ( Agent ):

def __init__ ( self ):
	self.x = 0
	self.y = 0
	self.hasArrow = True
	self.hasGold = False

	self.safe = [[(0,0)]]


def getAction( self, stench, breeze, glitter, bump, scream ):

	if self.x == 1 and self.y == 1:
		if stench or breeze:
			return Agent.Action.CLIMB

	return self.__actions [ random.randrange ( len ( self.__actions ) ) ]


	__actions = [
	Agent.Action.TURN_LEFT,
	Agent.Action.TURN_RIGHT,
	Agent.Action.FORWARD,
	Agent.Action.CLIMB,
	Agent.Action.SHOOT,
	Agent.Action.GRAB
	]