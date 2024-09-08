import random

listOfGreets = ["Semangat", "Hai", "Yuhuu"]
listOfEmoji = ["🔥", "🥇", "✨", "👋", "🚀"]

def getRandomGreet(greets: list = listOfGreets) -> str:
    return random.choice(greets)

def getRandomEmoji(emoji: list = listOfEmoji) -> str:
    return random.choice(emoji)
