# mlLearningAgents.py
# parsons/27-mar-2017
#
# A stub for a reinforcement learning agent to work with the Pacman
# piece of the Berkeley AI project:
#
# http://ai.berkeley.edu/reinforcement.html
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The agent here was written by Simon Parsons, based on the code in
# pacmanAgents.py
# learningAgents.py

from pacman import Directions
from game import Agent
import random
import game
import util
import math

# QLearnAgent
#
class QLearnAgent(Agent):

    # Constructor, called when we start running the
    def __init__(self, alpha=0.2, epsilon=0.05, gamma=0.8, numTraining = 10):
        # alpha       - learning rate
        # epsilon     - exploration rate
        # gamma       - discount factor
        # numTraining - number of training episodes
        # sc
        # These values are either passed from the command line or are
        # set to the default values above. We need to create and set
        # variables for them
        self.alpha = float(alpha)
        self.epsilon = float(epsilon)
        self.gamma = float(gamma)
        self.numTraining = int(numTraining)
        # Count the number of games we have played
        self.episodesSoFar = 0
        # keeps track of the score
        self.score = 0
        # keeps track of actions
        self.last_action = None
        # keeps track of state
        self.last_state = None
        # keeps track of Q values
        self.q_values = {}


    
    # Accessor functions for the variable episodesSoFars controlling learning
    def incrementEpisodesSoFar(self):
        self.episodesSoFar +=1

    def getEpisodesSoFar(self):
        return self.episodesSoFar

    def getNumTraining(self):
            return self.numTraining

    # Accessor functions for parameters
    def setEpsilon(self, value):
        self.epsilon = value

    def getAlpha(self):
        return self.alpha

    def setAlpha(self, value):
        self.alpha = value
        
    def getGamma(self):
        return self.gamma

    def getMaxAttempts(self):
        return self.maxAttempts

    # My implementation of Q-learning is based of reading Epilson-Greedy Q-learning algorithm on
    #https://www.baeldung.com/cs/epsilon-greedy-q-learning
    # the site presents a detailed understanding of Q-learning algorithm as well as Epsilon-Greedy Q-learning including psuedo-code
    # on how to implement the algorithms
    
    #In my implementation, I combine my understanding gained from off the website and lecture materials.
    #Additionally, I use the function max_Action from my mdp implementation from AIN module
    


    def update_Q(self, state):
        """
            update_Q(state) - updates the q value of the previous state/action pair

            parameters:
            state - current state of the game

            returns:
            does not return a value
            
        """
        #get q_value for previous state/action pair
    	previous_state = self.q_values[self.last_state][self.last_action]
        #gets the max q value of the current state
    	max_q = self.max_Q(state)
        #calculates the reward 
    	reward = state.getScore() - self.score
        # updates the q value of the previous state/action pair
    	self.q_values[self.last_state][self.last_action] = previous_state + (self.alpha * (reward + self.gamma * max_q - previous_state) )


    def max_Q(self,state):
        """
            max_Q(state) - return the max value of all actions in a given state

            parameters:
            state - current state of the game

            returns:
            returns max value
            
        """
        #obtain list of all state-action pair values
     	action_values = list(self.q_values[state].values())
        #return the highest value from list
     	return max(action_values)


    #get direction pacman should go in
    def max_Action(self, state, legal):
        """
            max_Action(state) - return the direction with max utility for a state

            parameters:
            state - current state of the game
            legal - legal actions of a given state

            returns:
            returns direction with max utility
            
        """
        if self.getEpisodesSoFar()*1.0/self.getNumTraining()<0.5:
            distance0 = state.getPacmanPosition()[0]- state.getGhostPosition(1)[0]
            distance1 = state.getPacmanPosition()[1]- state.getGhostPosition(1)[1]

            if math.sqrt(distance0**2 + distance1**2) > 2:
                if (game.Actions.reverseDirection(self.last_action) in legal) and len(legal)>1:
                    legal.remove(game.Actions.reverseDirection(self.last_action))


        distance0 = state.getPacmanPosition()[0]- state.getGhostPosition(1)[0]
        distance1 = state.getPacmanPosition()[1]- state.getGhostPosition(1)[1]

        if math.sqrt(distance0**2 + distance1**2) > 2:
            if (game.Actions.reverseDirection(self.last_action) in legal) and len(legal)>1:
                legal.remove(game.Actions.reverseDirection(self.last_action))

        #direction to go 
    	where_to_go = None
        #utilty current set to -10000000000
    	max_utility = -10000000000
        #for each legal direction
    	for direction in legal:
            #if the direction value 
    		if self.q_values[state][direction] > max_utility:
                # set max utility to state/action value
    			max_utility = self.q_values[state][direction]
                #set direction to go to direction
    			where_to_go = direction
        # return direction
    	return where_to_go



    def e_Greedy(self):
        """
            max_Action(state) - return the direction with max utility for a state

            parameters:
            state - current state of the game
            legal - legal actions of a given state

            returns:
            returns True or False
            
        """
    	#random probability 
        random_probability = random.random()
	    # return true if random probability is less than elipson
        return random_probability < self.epsilon



    
    # getAction
    #
    # The main method required by the game. Called every time that
    # Pacman is expected to move
    def getAction(self, state):

    	
        # The data we have about the state of the game
        legal = state.getLegalPacmanActions()
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        print "Legal moves: ", legal
        print "Pacman position: ", state.getPacmanPosition()
        print "Ghost positions:" , state.getGhostPositions()
        print "Food locations: "
        print state.getFood()
        print "Score: ", state.getScore()
 		
 		#check if the state,action pair has been created has not been stored
    	if state not in self.q_values:
    		#create state
    		self.q_values[state] = {}
    		for direction in legal:
    			#add actions for state
    			self.q_values[state][direction] = 0.0



    	if self.e_Greedy():   
	        # Now pick what action to take. For now a random choice among
	        # the legal moves
        	direction = random.choice(legal)
	        # We have to return an action
            if self.last_state != None:
    	        self.last_state = state
    	        self.last_action = direction
            self.score = state.getScore()
	        return direction
	    
	    
        direction = self.max_Action(state, legal)
        if self.last_state != None:
            self.last_state = state
            self.last_action = direction
        self.score = state.getScore()
        return direction

            

    # Handle the end of episodes
    #
    # This is called by the game after a win or a loss.
    def final(self, state):
        # #get q_value for previous state/action pair
    	previous_state = self.q_values[self.last_state][self.last_action]
        #final execution therefore max utility is 0
    	max_q = 0
        #reward value
    	reward = state.getScore() - self.score
        #update q value of previous state 
    	self.q_values[self.last_state][self.last_action] = previous_state + (self.alpha * (reward + self.gamma * max_q - previous_state) )


    	print "A game just ended!"

    	#reset score, last action and state
        self.last_state = None
        self.last_action = None
        self.score = 0


        
        # Keep track of the number of games played, and set learning
        # parameters to zero when we are done with the pre-set number
        # of training episodes
        self.incrementEpisodesSoFar()
        if self.getEpisodesSoFar() == self.getNumTraining():
            msg = 'Training Done (turning off epsilon and alpha)'
            print '%s\n%s' % (msg,'-' * len(msg))
            self.setAlpha(0)
            self.setEpsilon(0)


