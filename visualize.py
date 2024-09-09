from copy import deepcopy
import matplotlib.pyplot as plt
from trainer import *
from simplerl import *

def drawMazeRewards(maze, policy:Policy):
    fig, ax = plt.subplots()
    fig.set_size_inches(2,2)
    m = deepcopy(maze)
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            gstate = GridState(Position(x, y))
            m[y][x] = policy.qMemory.getMaxReward(gstate)

    ax.imshow(m, origin='lower')
    plt.gca().invert_yaxis()
    plt.axis('off')
    plt.show()

def drawMaze(maze, agentPosition, endPosition):
    fig, ax = plt.subplots()
    fig.set_size_inches(2,2)
    m = deepcopy(maze)
    m[agentPosition.y][agentPosition.x] = 2
    m[endPosition.y][endPosition.x] = 3

    ax.imshow(m, origin='lower')
    plt.gca().invert_yaxis()
    plt.axis('off')
    plt.show()


def showTrainingResults(trainer:Trainer, numBatches):
    x = range(numBatches)

    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2)

    ax1.set_title('Exploit Rate (training)')
    ax1.plot(x, trainer.eRates, label="Exploit Rate (training)", color='blue')

    ax2.set_title('Wins')
    ax2.plot(x, trainer.rWins, label='Wins', color='magenta')

    ax3.set_title("# Known States")
    ax3.plot(x, trainer.nStates, label="Known States", color='red')

    ax4.set_title("State max reward")
    ax4.plot(x, trainer.stateMaxRewards, label="state max reward", color='yellow')

    ax5.set_title("Avg. Test Steps")
    ax5.plot(x, trainer.nSteps, label="Avg. Test Steps", color='green')
