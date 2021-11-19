import json
import random
import rf


if __name__ == "__main__":
    qTable = json.load(open('./qTable.json', "r"))
    numberToGuess = random.randint(1,100)

    playerToken = 1
    gameState = -1
    min = 1
    max = 100
    playermin = 1
    playermax = 100
    playerGuesses = []
    computerGuesses = []
    while gameState != 0:
        if playerToken == 2:
            currentState = rf.tupleToState((min, max))
            currentAction = rf.getMaxIndex(qTable[currentState])
            currentGuess = currentAction + 1
            computerGuesses.append({
                "min": min,
                "max": max,
                "guess": currentGuess
            })
            reward, gameState, guessedNumber, min, max = rf.gameLoop(currentGuess, min, max, numberToGuess)
            if gameState == 0:
                print("Computer won. Number was: " + str(numberToGuess))
                break
            playerToken = 1
        if playerToken == 1:
            playerGuess = int(input("Zahl: "))
            playerGuesses.append({
                "min": playermin,
                "max": playermax,
                "guess": playerGuess
            })
            reward, gameState, guessedNumber, playermin, playermax = rf.gameLoop(playerGuess, playermin, playermax, numberToGuess)
            if(gameState == 0):
                currentState = rf.tupleToState((min, max))
                currentAction = rf.getMaxIndex(qTable[currentState])
                currentGuess = currentAction + 1
                computerGuesses.append({
                    "min": min,
                    "max": max,
                    "guess": currentGuess
                })
                reward, gameState, guessedNumber, min, max = rf.gameLoop(currentGuess, min, max, numberToGuess)
                print("Player won. Number was: " + str(numberToGuess))
                break

            if(playerGuess < numberToGuess):
                print("Zu niedrig")
            if(playerGuess > numberToGuess):
                print("Zu hoch")
            playerToken = 2

    print("Computer:")
    for i, guess in enumerate(computerGuesses):
        print(str(i + 1) + ". Versuch:" + str(guess))

    print("----------------")
    print("Spieler")
    for i, guess in enumerate(playerGuesses):
        print(str(i + 1) + ". Versuch:" + str(guess))


