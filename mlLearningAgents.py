#K20111591 Kwame Owusu Boahene
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
        # keeps of last action
        self.last_action = None
        # keep track of last state
        self.last_state = None
        # keeps track of Q values
        self.q_values = {}
        #keeps track of number of game state
        self.gamestate = 0


    
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
    #Also https://www.freecodecamp.org/news/diving-deeper-into-reinforcement-learning-with-q-learning-c18d0db58efe/ 
    #provides a step by step guide on implementing q-learning
    #In my implementation, I combine my understanding gained from off these websites and lecture materials.
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
        previous_value = self.q_values[self.last_state][self.last_action]
        #gets the max q value of the current state
        max_q = self.max_Q(state)
        #calculates the reward 
        reward = state.getScore() - self.score
        # updates the q value of the previous state/action pair
        self.q_values[self.last_state][self.last_action] = previous_value + (self.alpha * (reward + self.gamma * max_q - previous_value) )


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


    #adopted from my AIN implementation
    def max_Action(self, state, legal):
        """
            max_Action(state) - return the direction with max utility for a state

            parameters:
            state - current state of the game
            legal - legal actions of the current state of the game

            returns:
            returns direction with max utility
            
        """
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
            legal - legal actions of current state of the game

            returns:
            returns True or False
            
        """
        #random probability 
        random_probability = random.random()
        #return true if random probability is less than elipson
        return random_probability < self.epsilon


    def policy(self, state, legal):
        """
            policy(state,legal) - return the direction pacman should go in

            parameters:
            state -  state of the game
            legal - legal actions of current state of the game

            returns:
            returns direction pacman should go in
            
        """

        #check if e greedy
        if self.e_Greedy():
            #if yes set direction to a random direction
            direction = random.choice(legal)
            #set last action to direction
            self.last_action = direction
            
            
        #if not e-greedy return direction with max utility
        else:
            #get  direction with the mamximum utility
            direction = self.max_Action(state, legal)
            #set last action to direction
            self.last_action = direction


        #set score to score of state
        self.score = state.getScore()
        #increase gamestate by 1
        self.gamestate +=1

        return direction




    
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

        #check if the state,action pair has not been added to q-table
        if state not in self.q_values:
            #if not, create state in Q-table
            self.q_values[state] = {}
            #look at all possible legal directions
            for direction in legal:
                #create state/action pair for each direction
                self.q_values[state][direction]= 0.0
                

        #check if gamestate is 0, if its greater update qvalue
        # this is vital as when gamestate is 0 there is no last state action pair
        if self.gamestate != 0:
            #update qvalue for current state
            self.update_Q(state)

        #set last state to current state
        self.last_state = state

        #where to go
        direction = self.policy(state,legal);
        
        return direction
            

    # Handle the end of episodes
    #
    # This is called by the game after a win or a loss.
    def final(self, state):
        #terminal state
        #get q_value for previous state/action pair
        previous_value = self.q_values[self.last_state][self.last_action]
        #final execution therefore max utility is 0
        max_q = 0
        #reward value
        reward = state.getScore() - self.score
        #update q value of previous state 
        self.q_values[self.last_state][self.last_action] = previous_value + (self.alpha * (reward + self.gamma * max_q - previous_value) )


    	print "A game just ended!"

    	#reset score, gamestate, last action and state
        self.last_state = None
        self.last_action = None
        self.score = 0
        self.gamestate = 0

        
        # Keep track of the number of games played, and set learning
        # parameters to zero when we are done with the pre-set number
        # of training episodes
        self.incrementEpisodesSoFar()
        if self.getEpisodesSoFar() == self.getNumTraining():
            msg = 'Training Done (turning off epsilon and alpha)'
            print '%s\n%s' % (msg,'-' * len(msg))
            self.setAlpha(0)
            self.setEpsilon(0)


