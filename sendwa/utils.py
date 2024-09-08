import random

listOfGreets = ["Semangat", "Hai", "Yuhuu"]

def getRandomGreet(greets: list = listOfGreets) -> str:
    return random.choice(greets)
