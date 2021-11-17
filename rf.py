import multiprocessing
import random;

numberToGuess = random.randint(1, 100)
actions = [i for i in range(100)]
alpha = 0.6
gamma = 0.3
greed = 0.75

qTable = {}

def tupleToState(theTuple):
    currentState, min, max = theTuple
    return str(min).zfill(3) + str(max).zfill(3)  +str(currentState)

def initQTable():
    for state in (-1,1):
        for min in range(1, 101):
            for max in range(1, 101):
                qTable[tupleToState((state,min,max))] = [0 for i in range(0,100)]

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
    # guessedNumber = int(input("Versuch: "))
    if guessedNumber == numberToGuess:
        return 10, 0, guessedNumber, min, max
    if guessedNumber < numberToGuess:
        if guessedNumber > min:
            min = guessedNumber
        return -1, -1, guessedNumber, min, max
    if guessedNumber > numberToGuess:
        if guessedNumber < max:
            max = guessedNumber
        return -1, 1, guessedNumber, min, max

def game(episodes):
    initQTable()
    guesses = {}
    for i in range(100):
        guesses[i + 1] = 0
    tries = []
    for i in range(episodes):
        numberToGuess = random.randint(1, 100)
        reward, gameState, guessedNumber, min, max = gameLoop(random.randint(1,100), 1, 100, 50)
        currentTries = 0
        while gameState != 0:
            currentState = tupleToState((gameState, min, max))
           
            currentAction = getMaxIndex(qTable[currentState]) if random.random() < greed else random.randint(0, 99)
            currentGuess = currentAction + 1
            guesses[currentGuess] += 1
            reward, gameState, guessedNumber, min, max = gameLoop(currentGuess, min, max, numberToGuess)

            oldValue = qTable[currentState][currentAction]
            
            maxNextValue = getMaxValue(qTable[tupleToState((gameState, min, max))]) if gameState != 0 else 200

            newValue = (1 - alpha) * oldValue + alpha * (reward + gamma * maxNextValue)

            qTable[currentState][currentAction] = newValue

            currentTries += 1

        tries.append(currentTries)

    # print(sum(tries) / len(tries))
    return sum(tries) / len(tries)
    # print(guesses)

# p = multiprocessing.Pool(4)
# # p.apply(game, args=[5000])


for i in range(10):
    print(game(50000))

outFile = open("qTable.txt", "w")
for row in qTable:
    maxValue = getMaxValue(qTable[row])
    minValue = getMinValue(qTable[row])
    if maxValue != minValue:
        outFile.write(str(row) + " " + str(qTable[row]) + "\n")
outFile.close()



