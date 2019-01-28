import sys
from time import time

rankvalues = dict((r,i) for i,r in enumerate('..23456789TJQKA'))

# helper function to get cardinality of values to find pairs
def getFreqs(ranks):
    res = [set() for _ in range(5)]
    for r in ranks:
        count = ranks.count(r)
        res[count].add(r)
    return res


def getScore(hand):
    # list of suits in hand
    suits = [s for r,s in hand]

    # list of values in hand, in reverse order for tiebreakers
    ranks = sorted([rankvalues[r] for r,s in hand], reverse = True)

    # creates list of size 5 where index represents the cardinality of the card value
    # Ex: 9H 9D 9C 2H 3S -> [{}, {2,3}, {}, {9}, {}]
    freq = getFreqs(ranks)

    # if set length == 1, all cards same suit == flush
    flush = len(set(suits)) == 1

    # if max and min values range by 4 and no duplicate cards, hand is a straight
    straight = (max(ranks)-min(ranks))==4 and len(set(ranks))==5

    # Logic: 
    # assign score to a players hand
    # return score and also sorted hand values as tiebreaker

    if straight and flush: 
        return 9, ranks

    # four of a kind
    if len(freq[4]):
        return 8, freq[4].pop(), freq[1].pop()

    # full house
    if len(freq[3]) and len(freq[2]):
        return 7, freq[3].pop(), freq[2].pop()

    if flush: 
        return 6, ranks

    if straight: 
        return 5, ranks

    # 3 of a kind
    if len(freq[3]):
        return 4, freq[3].pop(), ranks

    # two pair
    if len(freq[2]) == 2:
        firstPair = freq[2].pop()
        secondPair = freq[2].pop()
        if firstPair >= secondPair:
            larger = firstPair
            smaller = secondPair
        else:
            larger = secondPair
            smaller = firstPair
        return 3, larger, smaller, ranks

    # 2 of a kind
    if len(freq[2]):
        return 2, freq[2].pop(), ranks

    # lowest score, checks high card(s)
    return 1, ranks


def main():
    if len(sys.argv) > 1:
        fileName = sys.argv[1]
    else:
        return "No input file passed"

    p1Wins = 0
    p2Wins = 0

    f = open(fileName, "r")
    for line in f:
        p1Cards = line.split()[:5]
        p2Cards = line.split()[5:]

        if getScore(p1Cards) > getScore(p2Cards):
            p1Wins += 1
        else:
            p2Wins += 1

    return 'Player 1: ' + str(p1Wins) + '\n' + 'Player 2: ' + str(p2Wins)

print(main())