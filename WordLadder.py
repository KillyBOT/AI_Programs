import sys,os
import threading
import copy
import heapq as hq

wordDict = open("dictall.txt","r")
inputFile = open("wordladder_input.txt","r")
outFile = open("wout.txt","w+")
wordList = []
wordSet = []
wordSuccessorsSeen = set()
wordSuccessorsDict = dict()
wordDistSeen = set()
wordDistDict = dict()

maxThreads = 1
exitFlag = 0

totalLongest = []
totalLongestLen = 0

checkLongestLock = threading.Lock()

#We assume there are 4 threads running at once
class searchThread(threading.Thread):
    def __init__(self, threadID, name, wordLen):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.wordLen = wordLen

    def run(self):
        wordListLen = len(wordList)
        if maxThreads == 1:
            wordListLen -= 1
        wordListDivision = int(wordListLen / maxThreads)

        searchRange = wordList[wordListDivision * self.threadID:wordListDivision * (self.threadID + 1)]

        print(self.name + " searching from [" + searchRange[0] + "] to [" + searchRange[-1] + "]")
        astar_longest_shortest_path(self.name,searchRange,self.wordLen)
        print(self.name + " finished search")
        #print(" -> ".join(totalLongest))
        #print(len(totalLongest))
    
#Find all successors
def find_word_successors(searchRange, word):

    global wordSuccessorsSeen
    global wordSuccessorsDict

    if word not in wordSuccessorsSeen:

        wordSuccessorsSeen.add(word)
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

        wordSuccessorsDict[word] = list(searchRange.intersection(similarWords))

    #We use an intersection between our dictionary of words and the words we found
    return wordSuccessorsDict[word]

#This only works when the words are of the same length
def distance_to_goal(current, end):

    global wordDistSeen
    global wordDistDict

    if (current, end) not in wordDistSeen:

        wordDistSeen.add((current,end))
        wordDistSeen.add((end,current))

        cost = len(current)

        smaller = current if len(current) < len(end) else end
        larger = current if len(current) >= len(end) else end

        if len(smaller) != len(larger):

            cost += len(larger) - len(smaller)

            currentSmallest = 999999999
            for offset in range(len(larger)-len(smaller)):
                toBeSmallest = cost
                for currentLetter in range(len(smaller)):
                    if smaller[currentLetter] != larger[currentLetter + offset]:
                        toBeSmallest -= 1

                currentSmallest = toBeSmallest if toBeSmallest < currentSmallest else currentSmallest


            cost += currentSmallest

        else:
            for letter in range(len(current)):
                if current[letter] == end[letter]:
                    cost -= 1

        wordDistDict[(current,end)] = cost
        wordDistDict[(end,current)] = cost

    return wordDistDict[(current,end)]

#Find the closest path from one word to the other using A*
def astar(start, end):
    frontier = [(distance_to_goal(start,end),0,start)]
    hq.heapify(frontier)
    seen = set()
    seen.add(start)
    keepSearching = 1

    while keepSearching:

        current = hq.heappop(frontier)
        path = current[2:]
        last = path[-1]

        if last != end:
            for successor in find_word_successors(wordSet,last):
                if successor not in seen:
                    seen = seen.add(successor)

                    new = list(path)
                    new.append(successor)

                    distToGoal = distance_to_goal(successor,end)
                    distFromStart = current[1] + 1
                    new.insert(0,distFromStart)
                    new.insert(0,distToGoal+distFromStart)

                    hq.heappush(frontier,tuple(new))

            if len(frontier) == 0:
                return ['No solution']
        else:
            keepSearching = 0

    return list(path)

def astar_range(start, end, searchRange):
    frontier = [(distance_to_goal(start,end),0,start)]
    hq.heapify(frontier)
    seen = set()
    seen.add(start)
    keepSearching = 1

    while keepSearching:

        current = hq.heappop(frontier)
        path = current[2:]
        last = path[-1]

        if last != end:
            for successor in find_word_successors(searchRange,last):
                if successor not in seen:
                    seen.add(successor)

                    new = list(path)
                    new.append(successor)

                    distToGoal = distance_to_goal(successor,end)
                    distFromStart = current[1] + 1
                    new.insert(0,distFromStart)
                    new.insert(0,distToGoal+distFromStart)

                    hq.heappush(frontier,tuple(new))

            if len(frontier) == 0:
                return ['No solution']
        else:
            keepSearching = 0

    return list(path)

def astar_len(start, end,wordLen):

    newSearchSet = set([word for word in wordList if len(word)==wordLen])

    frontier = [(distance_to_goal(start,end),0,start)]
    hq.heapify(frontier)
    seen = set()
    seen.add(start)
    keepSearching = 1

    while keepSearching:

        current = hq.heappop(frontier)
        path = current[2:]
        last = path[-1]

        if last != end:
            for successor in find_word_successors(newSearchSet,last):

                if successor not in seen:
                    seen.add(successor)

                    new = list(path)
                    new.append(successor)

                    distToGoal = distance_to_goal(successor,end)
                    distFromStart = current[1] + 1
                    new.insert(0,distFromStart)
                    new.insert(0,distToGoal+distFromStart)

                    hq.heappush(frontier,tuple(new))

            if len(frontier) == 0:
                return ['No solution']
        else:
            keepSearching = 0

    return list(path)

def astar_longest_shortest_path(threadName, searchRange, wordLen):
    newSearchSet = set([word for word in wordList if len(word) == wordLen])

    seenPairs = set()
    percentComplete = 0
    percentChange = (1 / len(newSearchSet)) * 100

    global totalLongest
    global totalLongestLen
    global checkLongestLock

    for start in searchRange:
        for end in searchRange:

            if exitFlag:
                threadName.exit()

            if start != end and (start,end) not in seenPairs:

                if maxThreads == 1:
                    print(start,end,totalLongestLen,percentComplete)
                    sys.stdout.write('\x1b[1A\x1b[2K')

                seenPairs.add((start,end))
                seenPairs.add((start,end))

                path = astar_range(start,end,newSearchSet)
                pathLen = len(path)

                if pathLen > 1:
                    for firstP in range(0,pathLen-1):
                        for secondP in range(1,pathLen):
                            first = path[firstP]
                            second = path[secondP]
                            seenPairs.add((first,second))
                            seenPairs.add((second,first))

                #if maxThreads != 1:
                #    checkLongestLock.acquire()

                if pathLen > totalLongestLen:
                    totalLongest = path
                    totalLongestLen = len(path)
                    print(start,end,totalLongestLen)

                #if maxThreads != 1:
                #    checkLongestLock.release()

        percentComplete += percentChange

    print(" -> ".join(totalLongest),totalLongestLen)
    #return totalLongest

#Find the longest path from one word to the other using DFS
def dfs_totalLongest_path(start, end):
    startLen = len(start)
    newSearchSet = set([word for word in wordList if len(word)==startLen])

    frontier = [(-1-distance_to_goal(start,end),-1,start)]
    hq.heapify(frontier)
    longestDict = dict()
    longestDict[start] = 1

    totalLongest = []
    totalLongestLen = 0

    timesEndFound = 0
    deadEnds = 0

    while len(frontier):

        current = hq.heappop(frontier)
        path = current[2:]
        pathLen = current[1]
        last = path[-1]

        print(len(frontier),totalLongestLen,timesEndFound,deadEnds)
        sys.stdout.write('\x1b[1A\x1b[2K')

        if last == end:
            timesEndFound += 1
            if pathLen <= totalLongestLen:
                totalLongest = list(path)
                totalLongestLen = pathLen
        if last not in longestDict or pathLen <= longestDict[last]:
            longestDict[last] = pathLen
            for successor in find_word_successors(newSearchSet,last):
                if successor not in path:
                    new = list(path)
                    new.append(successor)
                    distToGoal = -distance_to_goal(successor,end)
                    distFromStart = pathLen - 1
                    new.insert(0,distFromStart)
                    new.insert(0,distFromStart+distToGoal)
                    hq.heappush(frontier,tuple(new))

    return totalLongest

#Find the longest path possible given a specific word length
def dfs_totalLongest_sequence(threadName, searchRange, wordLen):

    totalLongest = []
    totalLongestLen = 1

    for start in searchRange:
        if len(start) == wordLen:

            frontier = [[start]]
            totalLongestToWord = dict()

            if maxThreads == 1:
                print(start,totalLongestLen)
                sys.stdout.write('\x1b[1A\x1b[2K') 

            while len(frontier):

                if exitFlag:
                    threadName.exit()

                current = frontier.pop()
                last = current[-1]
                currentLen = len(current)

                if last not in totalLongestToWord or currentLen > totalLongestToWord[last]:

                    successors = find_word_successors(wordSet,last)
                    totalLongestToWord[last] = currentLen

                    if len(successors):
                        allSuccessorsAlreadyFound = 1
                        for successor in successors:
                            if successor not in current:
                                allSuccessorsAlreadyFound = 0
                                new = current[:]
                                new.append(successor)
                                frontier.append(new)

                        if allSuccessorsAlreadyFound and currentLen > totalLongestLen:
                            totalLongest = current
                            totalLongestLen = currentLen

                    elif len(current) > totalLongestLen:
                        totalLongest = current
                        totalLongestLen = currentLen

    return totalLongest


if __name__ == "__main__":

    start = "head"
    end = "tail"

    #otherPair = [["head","tail"],["five","four"],["like","flip"],["drive","sleep"]]
    pairs = []
    for word in wordDict.readlines():
        splitWord = word.split()[0]
        wordSet.append(splitWord)
        wordList.append(splitWord)

    wordSet = set(wordSet)

    if len(sys.argv) > 2:

        start = str(sys.argv[1])
        end = str(sys.argv[2])

        print(" -> ".join(astar_len(start,end,len(start))))

        """totalLongest_path = dfs_totalLongest_path(start, end)
        print(" -> ".join(totalLongest_path))
        print(len(totalLongest_path))"""

        """totalLongest_path_len = dfs_totalLongest_sequence(5)
        #print(" -> ".join(totalLongest_path_len))
        #print(len(totalLongest_path_len))"""

    elif len(sys.argv) > 1:

        threads = []

        gWordLen = int(sys.argv[1])

        wordList = [word for word in wordList if len(word) == gWordLen]
        wordSet = set(wordList)

        for x in range(0,maxThreads):
            threads.append(searchThread(x, "thread-"+str(x), gWordLen))

        """thread0 = searchThread(0, "thread-0", gWordLen)
        thread1 = searchThread(1, "thread-1", gWordLen)
        thread2 = searchThread(2, "thread-2", gWordLen)
        thread3 = searchThread(3, "thread-3", gWordLen)
        thread4 = searchThread(4, "thread-4", gWordLen)
        thread5 = searchThread(5, "thread-5", gWordLen)
        thread6 = searchThread(6, "thread-6", gWordLen)
        thread7 = searchThread(7, "thread-7", gWordLen)"""

        for thread in threads:
            thread.start()

        """thread0.start()
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        thread5.start()
        thread6.start()
        thread7.start()"""

        #longest = astar_longest_shortest_path_simple(searchRange,gWordLen)
        #print(" -> ".join(longest))
        #print(len(longest))
    else:

        for line in inputFile.readlines():
            pairs.append(line.split("\n")[0].split(","))
        for x in range(len(pairs)):
            outFile.write("=== A* Search ===\n")
            outFile.writelines(" -> ".join(astar_len(pairs[x][0],pairs[x][1],len(pairs[x][0]))))
            outFile.write("\n")
            outFile.write("\n")

        outFile.read()
        wordDict.close()
        inputFile.close()
        outFile.close()
    
