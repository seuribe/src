from simplerl import *
from trainer import *

DEFAULT_GRID = [[2,0,0,1,0,3,0,0],
                [0,1,1,1,0,0,0,0],
                [0,1,0,1,0,1,1,1],
                [0,0,0,1,0,0,1,0],
                [0,1,1,1,1,0,1,0],
                [0,0,0,1,0,0,1,0],
                [0,1,0,0,0,1,1,0],
                [0,1,0,1,0,0,0,0],
                ]

def envBuilder():
    return GridEnvironment(Grid(DEFAULT_GRID))

trainer = Trainer(envBuilder)
NUM_BATCHES = 100
trainer.batchTrain(numBatches = NUM_BATCHES, numTrainEpisodes = 200, numTestEpisodes = 100, maxSteps = 50, maxProcesses = 8)
