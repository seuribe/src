from typing import List, Dict
from enum import Enum
from dataclasses import dataclass
import random


@dataclass
class Action:
    pass


@dataclass
class State:
    pass


class Environment:
    state:State

    def __init__(self, state:State):
        self.state = state

    def isEndState(self) -> bool:
        return self.isWinState() or self.isTieState() or self.isLoseState()

    def isWinState(self) -> bool:
        return False

    def isLoseState(self) -> bool:
        return False

    def isTieState(self) -> bool:
        return False

    def execute(self, action:Action) -> int:
        self.state = self.getNewState(action)
        return self.getReward()

    def getNewState(self, action:Action) -> State:
        return self.state

    def getReward(self):
        return 100 if self.isWinState() else -1

    def getState(self) -> State:
        return self.state

    def getAllPossibleActions(self) -> List[Action]:
        return []


class QMemory:
    class ActionRewards:
        maxAction:Action
        def __init__(self):
            self.actions = {}
            self.maxAction = None

        def getExpectedReward(self, action:Action):
            return self.actions.get(action, 0)

        def getMaxReward(self):
            return 0 if self.maxAction is None else self.actions[self.maxAction]

        def setExpectedReward(self, action:Action, reward):
            self.actions[action] = reward
            if not self.maxAction or reward > self.actions[self.maxAction]:
                self.maxAction = action

    sar: Dict[State, ActionRewards]

    def __init__(self, learningRate = 0.9, discountRate = 0.5):
        self.learningRate = learningRate
        self.discountRate = discountRate
        self.sar = {}

    def getBestAction(self, state:State) -> Action:
        return self.getActionRewards(state).maxAction

    def getActionRewards(self, state:State) -> ActionRewards:
        if state in self.sar:
            return self.sar[state]

        ars = self.ActionRewards()
        self.sar[state] = ars

        return ars

    def getMaxReward(self, state:State):
        return self.getActionRewards(state).getMaxReward()

    def update(self, oldState:State, action:Action, newState:State, reward):
        oldSA = self.getActionRewards(oldState)
        currentValue = oldSA.getExpectedReward(action)
        newSA = self.getActionRewards(newState)
        maxExpectedNew = newSA.getMaxReward()
        newExpectedReward = currentValue + self.learningRate * (reward + self.discountRate * maxExpectedNew - currentValue)
        oldSA.setExpectedReward(action, newExpectedReward)


class Policy:
    qMemory:QMemory

    def __init__(self, learningRate = 0.9, discountRate = 0.5):
        self.qMemory = QMemory(learningRate, discountRate)

    def pickAction(self, env:Environment, exploitRate = 1) -> Action:
        if random.random() <= exploitRate:
            st = env.getState()
            bestAction = self.qMemory.getBestAction(st)
            if bestAction:
                return bestAction

        return self.randomAction(env)

    def randomAction(self, env:Environment) -> Action:
        actions = list(env.getAllPossibleActions())
        return random.choice(actions) if actions else None

    def update(self, oldState:State, action:Action, newState:State, reward):
        self.qMemory.update(oldState, action, newState, reward)

    def getMaxReward(self, state):
        return self.qMemory.getMaxReward(state)

    def numKnownStates(self):
        return len(self.qMemory.sar)
