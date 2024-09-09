import matplotlib.pyplot as plt
from simplerl import *
from trainer import *
from visualize import *

def trainAndShowRewards(maze):
    def envBuilder(startPosition = DEFAULT_START, endPosition = DEFAULT_END):
        return GridEnvironment(Grid(maze), startPosition, endPosition)

    trainer = Trainer(envBuilder)
    trainer.batchTrain(numBatches = 50, numTrainEpisodes = 200, numTestEpisodes = 100, maxSteps = 100, maxProcesses = 8)

    drawMazeRewards(maze, trainer.policy)
