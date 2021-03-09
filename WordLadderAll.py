import sys,os
import copy
#from graphviz import Graph
from igraph import *

wordDict = open("dictall.txt","r")
vertexDict = {}
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

    #We use an intersection between our dictionary of words and the words we found
    return list(wordSet.intersection(similarWords))

if __name__ == "__main__":

    wordIndex = 0
    wordLen = int(sys.argv[1])

    #otherPair = [["head","tail"],["five","four"],["like","flip"],["drive","sleep"]]

    for word in wordDict.readlines():
        splitWord = word.split()[0]
        if len(splitWord) == wordLen:
            wordSet.append(splitWord)
            wordList.append(splitWord)
            vertexDict[splitWord] = wordIndex
            wordIndex += 1

    wordSet = set(wordSet)
    seen = set()
    frontier = []

    #outputFile = 'wordConnections_len_'+str(sys.argv[1])+'.gv'

    #g = Graph('G', filename=outputFile, engine = 'neato', format='svg')
    g = Graph()

    g.add_vertices(len(wordList))
    g.vs["word"] = wordList
    g.vs["label"] = g.vs["word"]

    for word in wordList:
        frontier = [word]
        while(len(frontier) > 0):
            current = frontier.pop()
            if current not in seen:
                seen.add(current)
                currentIndex = vertexDict[current]
                successors = find_word_successors(current)
                for successor in successors:
                    if successor not in seen:
                        successorIndex = vertexDict[successor]
                        g.add_edges([(currentIndex,successorIndex)])
                        frontier.append(successor)

    plot(g, layout=g.layout("circle"), bbox=(8192,8192))

