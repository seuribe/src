import random
from chess import *

class Environment:
    def __init__(self, board):
        self.board = board

    def isEndState(self):
        """ It's an end state if:
            * White wins (black king is check-mated)
            * White loses (has no more pieces left)
        """
        return self.board.isCheckMated(BLACK) or not self.board.allPiecesFrom(WHITE)

    def getAllPossibleActions(self, color = WHITE):
        return self.board.getAllMovesFor(color)

    def execute(self, action):
        self.board.move(action)
        return 0
    
    def getState(self):
        return self.encode(self.board)
    
    def encode(self, board):
        return board

class QLearning:
    class StateAction:
        def __init__(self):
            self.actions = {}
            self.maxAction = None

        def getExpectedReward(self, action):
            return self.actions.get(action) or 0
        
        def getMaxReward(self):
            return 0 if self.maxAction is None else self.actions[self.maxAction]
        
        def setExpectedReward(self, action, reward):
            self.actions[action] = reward

    def __init__(self, learningRate = 0.9, discountRate = 0.5):
        self.learningRate = learningRate
        self.discountRate = discountRate
        self.sas = {}

    def getBestAction(self, state):
        sa = self.sas.get(state)
        return None if sa is None else sa.maxAction

    def getStateAction(self, state):
        sa = self.sas.get(state)
        if sa is None:
            sa = self.StateAction()
            self.sas[state] = sa

        return sa

    def update(self, oldState, action, newState, reward):
        oldSA = self.getStateAction(oldState)
        currentValue = oldSA.getExpectedReward(action)
        newSA = self.getStateAction(newState)
        maxExpectedNew = newSA.getMaxReward()
        newExpectedReward = currentValue + self.learningRate * (reward + self.discountRate * maxExpectedNew - currentValue)
        oldSA.setExpectedReward(action, newExpectedReward)

class Policy:
    def __init__(self, env, qLearning, exploitRate):
        self.env = env
        self.qLearning = qLearning
        self.exploitRate = exploitRate
    
    def pickAction(self):
        if random.random() < self.exploitRate:
            bestAction = self.qLearning.getBestAction(self.env.getState())
            if bestAction is not None:
                return bestAction

        return self.randomAction()

    def randomAction(self):
        actions = list(self.env.getAllPossibleActions())
        if not actions:
            return None
        return random.choice(actions)

class Episode:
    def __init__(self, env, qLearning, exploitRate):
        self.env = env
        self.qLearning = qLearning
        self.policy = Policy(env, qLearning, exploitRate)

    def step(self, maxSteps = 100):
        steps = 0
        while steps < maxSteps and not self.env.isEndState():
            steps = steps + 1
            
            oldState = self.env.getState()
            action = self.policy.pickAction()
            if not action:
                break
            reward = self.env.execute(action)
            newState = self.env.getState()
            self.qLearning.update(oldState, action, newState, reward)

        return steps
        