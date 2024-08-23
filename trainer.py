from typing import Callable
from multiprocessing import Pool
from tqdm import tqdm

from rl import *

NUM_TRAIN_EPISODES = 50
NUM_TEST_EPISODES = 100
NUM_BATCHES = 100
MAX_STEPS = 20
TEST_EXPLOIT_RATE = 0.75


class Episode:
    env: Environment
    policy: Policy

    def __init__(self, env:Environment, policy:Policy, exploitRate):
        self.env = env
        self.policy = policy
        self.exploitRate = exploitRate

    def step(self, maxSteps = 100, onStepStart = lambda e:None, onStepEnd = lambda e:None):
        steps = 0
        while steps < maxSteps and not self.env.isEndState():
            onStepStart(self.env)
            action = self.policy.pickAction(self.env, self.exploitRate)
            if not action:
                break
            oldState = self.env.getState()
            reward = self.env.execute(action)
            newState = self.env.getState()
            self.policy.update(oldState, action, newState, reward)
            onStepEnd(self.env)
            steps = steps + 1

        return steps


class Trainer:
    policy:Policy

    def __init__(self, envProvider:Callable[[], Environment]):
        """ envProvider is a function that returns an Environment for training and testing """
        self.envProvider = envProvider
        self.rWins = []
        self.eRates = []
        self.nStates = []
        self.nSteps = []
        self.stateMaxRewards = []
        self.policy = Policy(discountRate=1)

    def trainExploitRate(self, batchNumber, numBatches):
        return 0.5 + (batchNumber / numBatches)/2

    def train(self, maxSteps, exploitRate):
        env = self.envProvider()
        episode = Episode(env, self.policy, exploitRate)
        return episode.step(maxSteps)

    def test(self, maxSteps, exploitRate):
        env = self.envProvider()
        episode = Episode(env, self.policy, exploitRate)
        steps = episode.step(maxSteps)
        return (env.isWinState(), steps, self.policy.getMaxReward(env.getState()))

    def batchTrain(self, numBatches:int = NUM_BATCHES, numTrainEpisodes = NUM_TRAIN_EPISODES, numTestEpisodes = NUM_TEST_EPISODES, maxSteps = MAX_STEPS, maxProcesses:int = 1):
        self.numBatches = numBatches

        for b in tqdm(range(numBatches)):
            exploitRate = self.trainExploitRate(b, numBatches)
            if maxProcesses > 1:
                with Pool(processes=maxProcesses) as pool:
                    for _ in range(numTrainEpisodes):
                        pool.apply_async(self.train, maxSteps, exploitRate)
                    pool.close()
                    pool.join()
            else:
                for _ in range(numTrainEpisodes):
                    self.train(maxSteps, exploitRate)

            wins = 0
            totalSteps = 0
            stateMaxReward = 0
            for _ in range(numTestEpisodes):
                (isWin, steps, maxReward) = self.test(maxSteps, TEST_EXPLOIT_RATE)
                stateMaxReward = stateMaxReward + maxReward
                totalSteps = totalSteps + steps
                if isWin:
                    wins = wins + 1

            totalStates = self.policy.numKnownStates()
            self.stateMaxRewards.append(stateMaxReward / numTestEpisodes)
            self.rWins.append(wins)
            self.eRates.append(exploitRate)
            self.nStates.append(totalStates)
            self.nSteps.append(totalSteps / numTestEpisodes)
