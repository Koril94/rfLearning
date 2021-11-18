import math
import multiprocessing
import random
import time
import json

numberToGuess = random.randint(1, 100)
actions = [i for i in range(100)]
alpha = 0.7
gamma = 0.4
greed = 0.5


def tupleToState(theTuple):
    min, max = theTuple
    return str(min).zfill(3) + str(max).zfill(3)

def initQTable():
    qTable = {}
    for min in range(1, 101):
        for max in range(1, 101):
            qTable[tupleToState((min,max))] = [0 for i in range(0,100)]
    return qTable


def getMaxIndex(l):
    max = l[0]
    result = 0
    for index, value in enumerate(l):
        if value > max:
            max = value
            result = index
    return result

def getMaxValue(l):
    max = l[0]
    result = 0
    for index, value in enumerate(l):
        if value > max:
            max = value
            result = index
    return max

def getMinValue(l):
    max = l[0]
    result = 0
    for index, value in enumerate(l):
        if value < max:
            max = value
            result = index
    return max


def gameLoop(guessedNumber, min, max, numberToGuess):
    if guessedNumber < min or guessedNumber > max:
        return -100, -1, guessedNumber, min, max
    elif guessedNumber == numberToGuess:
        return 100, 0, guessedNumber, min, max
    elif guessedNumber < numberToGuess:
        if guessedNumber > min:
            min = guessedNumber
        return -1, -1, guessedNumber, min, max
    elif guessedNumber > numberToGuess:
        if guessedNumber < max:
            max = guessedNumber
        return -1, -1, guessedNumber, min, max

def game(episodes, qTable):
    
    guesses = {}
    for i in range(100):
        guesses[i + 1] = 0
    tries = []
    for i in range(episodes):
        if i > 25:
            greed = 0.8
        elif i > 100:
            greed = 0.9
        elif i > 1000:
            greed = 0.95
        else:
            greed = 1

        numberToGuess = random.randint(1, 100)
        min = 1
        max = 100
        # reward, gameState, guessedNumber, min, max = gameLoop(50, min, max, numberToGuess)
        gameState = "start"
        currentTries = 0
        while gameState != 0:
            currentState = tupleToState((min, max))
            currentAction = getMaxIndex(qTable[currentState]) if random.random() < greed  else random.randint(0, 99)
            currentGuess = currentAction + 1
            guesses[currentGuess] += 1
            reward, gameState, guessedNumber, min, max = gameLoop(currentGuess, min, max, numberToGuess)

            oldValue = qTable[currentState][currentAction]
            
            maxNextValue = getMaxValue(qTable[tupleToState((min, max))]) if gameState != 0 else 100

            newValue = (1 - alpha) * oldValue + alpha * (reward + gamma * maxNextValue)

            qTable[currentState][currentAction] = newValue

            currentTries += 1

        tries.append(currentTries)
    if i == episodes - 1:
        # print(qTable)
        f = open("qTable.json", "w")
        f.write(json.dumps(qTable))
        f.close()

    return sum(tries) / len(tries)

def runGameAndGenerateOutput(loopCounter, qTable):
    print(game(loopCounter, qTable), "Loopcounter:", loopCounter)
    

    outFile = open("qTable{0}.txt".format(loopCounter), "w")
    outFile2 = open("IntervalMax{0}.txt".format(loopCounter), "w")
    for row in qTable:
        maxValue = getMaxValue(qTable[row])
        minValue = getMinValue(qTable[row])
        if maxValue != minValue:
            outFile2.write(row[0:3] + "-" + row[3::] + ":" + str(getMaxIndex(qTable[row]) + 1) + "\n")
            outFile.write(str(row) + " " + str(qTable[row]) + "\n")
    outFile.close()
    outFile2.close()

if __name__ == '__main__':
    for i in range(100):
        maxValue = 10000
        tic = time.time()
        try:
            qTable = json.load(open('qTable.json', "r"))
        except:
            qTable = initQTable()
        runGameAndGenerateOutput(maxValue, qTable)
        tac = time.time()
        print("{0}".format(tac - tic))
