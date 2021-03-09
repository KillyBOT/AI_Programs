import sys,os
import copy
import heapq as hq

wordDict = open("dictall.txt","r")
wordSet = []
wordList = []
    
#Find all successors
def find_word_successors(word):
    letters = "abcdefghijklmnopqrstuvwxyz"
    wordSplit = list(word)
    #Sets are much easier to compare to each other than lists, so we're using them for our list of similar words
    similarWords = set()

    #Replace one of the letters
    for letterPos in range(len(wordSplit)):
        for replaceLetter in letters:
            current = wordSplit[:]
            current[letterPos] = replaceLetter
            currentWord = "".join(current)
            if currentWord != word:
                similarWords.add(currentWord)

    """
    #Add a letter to the beginning and the end of the word
    for addLetter in letters:
        currentBeginning = addLetter + word
        currentEnd = word + addLetter
        similarWords.add(currentBeginning)
        similarWords.add(currentEnd)


    #Remove a letter from the beginning and the end of the word
    similarWords.add("".join(wordSplit[1:]))
    similarWords.add("".join(wordSplit[:-1]))
    """

    #We use an intersection between our dictionary of words and the words we found
    return list(wordSet.intersection(similarWords))

#This only works when the words are of the same length

if __name__ == "__main__":

    longestChainLen = 0
    shortestChainLen = 99999999
    longestChain = []

    #otherPair = [["head","tail"],["five","four"],["like","flip"],["drive","sleep"]]
    pairs = []
    for word in wordDict.readlines():
        splitWord = word.split()[0]
        wordSet.append(splitWord)
        wordList.append(splitWord)

    wordSet = set(wordSet)
    wordLen = int(sys.argv[1])

    for word in wordList:
        seen = set()
        frontier = [[word]]
