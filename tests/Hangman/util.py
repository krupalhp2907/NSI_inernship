import random
import math


def genFinalList(word, op):
    alphs = [chr(i) for i in range(ord('a'), ord('z') + 1)]

    for char in alphs:
        if char in word:
            alphs.remove(char)

    for i, al in enumerate(op):
        if al == False:
            op[i] = [alphs[random.randrange(0, len(alphs))], False]
        else:
            op[i] = [al, True]


def correctAnswer(word, wrong_input=6):
    op = [False] * wrong_input + list(word)
    random.shuffle(op)

    genFinalList(word, op)

    return op


def wrongAnswer(word, wrong_input=7):
    op = [False]*wrong_input + list(word)
    genFinalList(word, op)
    return op


def getRanChar():
    return chr(ord('a') + random.randrange(0, 25))


def compare(h1, h2, epoch=2):
    if abs(abs(float(h1)) - abs(float(h2))) <= epoch:
        return True
    return False


def distancePts(p1, p2):
    return math.sqrt(abs(p1.x - p2.x)**2 + abs(p1.y - p2.y)**2)
