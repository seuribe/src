import random
from chess import *


@dataclass
class State:
    board:Board


@dataclass
class Action:
    move:Move


class Environment:
    board:Board
    def __init__(self, board):
        self.board = board

    def isEndState(self):
        """ It's an end state if:
            * White wins (black king is check-mated)
            * White loses (has no more pieces left)
        """
        return self.board.isCheckMated(Color.Black) or not self.getAllPossibleActions(Color.White)

    def getAllPossibleActions(self, color:Color = Color.White) -> List[Action]:
        allMoves = self.board.getAllMovesFor(color)
        # map each move to an action
        return list(map(lambda m:Action(move=m), allMoves))

    def execute(self, action:Action):
        self.board.move(action.move)
        return 0
    
    def getState(self) -> State:
        return self.encode(self.board)
    
    def encode(self, board:Board):
        return State(board=board)


class QLearning:

    class StateAction:
        maxAction:Action
        def __init__(self):
            self.actions = {}
            self.maxAction = None

        def getExpectedReward(self, action:Action):
            return self.actions.get(action) or 0
        
        def getMaxReward(self):
            return 0 if self.maxAction is None else self.actions[self.maxAction]
        
        def setExpectedReward(self, action:Action, reward):
            self.actions[action] = reward

    def __init__(self, learningRate = 0.9, discountRate = 0.5):
        self.learningRate = learningRate
        self.discountRate = discountRate
        self.sas = {}

    def getBestAction(self, state:State) -> Action:
        sa = self.sas.get(state)
        return None if sa is None else sa.maxAction

    def getStateAction(self, state:State) -> StateAction:
        sa = self.sas.get(state)
        if sa is None:
            sa = self.StateAction()
            self.sas[state] = sa

        return sa

    def update(self, oldState:State, action:Action, newState:State, reward):
        oldSA = self.getStateAction(oldState)
        currentValue = oldSA.getExpectedReward(action)
        newSA = self.getStateAction(newState)
        maxExpectedNew = newSA.getMaxReward()
        newExpectedReward = currentValue + self.learningRate * (reward + self.discountRate * maxExpectedNew - currentValue)
        oldSA.setExpectedReward(action, newExpectedReward)


class Policy:
    qLearning:QLearning
    env:Environment

    def __init__(self, env, qLearning, exploitRate):
        self.env = env
        self.qLearning = qLearning
        self.exploitRate = exploitRate
    
    def pickAction(self) -> Action:
        if random.random() < self.exploitRate:
            bestAction = self.qLearning.getBestAction(self.env.getState())
            if bestAction:
                return bestAction

        return self.randomAction()

    def randomAction(self) -> Action:
        actions = list(self.env.getAllPossibleActions())
        return random.choice(actions) if actions else None


class Episode:
    env: Environment
    policy: Policy
    qLearning: QLearning

    def __init__(self, env:Environment, qLearning:QLearning, exploitRate):
        self.env = env
        self.qLearning = qLearning
        self.policy = Policy(env, qLearning, exploitRate)

    def step(self, maxSteps = 100, onStepStart = lambda:None, onStepEnd = lambda:None):
        steps = 0
        while steps < maxSteps and not self.env.isEndState():
            steps = steps + 1
            onStepStart()
            oldState = self.env.getState()
            action = self.policy.pickAction()
            if not action:
                break
            reward = self.env.execute(action)
            newState = self.env.getState()
            self.qLearning.update(oldState, action, newState, reward)
            onStepEnd()

        return steps
        