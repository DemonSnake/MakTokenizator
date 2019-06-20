"""
Module for searching some query in a database
"""
import os
import shelve
import tokenizer
import indexator
from indexator import Indexator


class ContextWindow():
    """
    Class representing a context window
    Remembers the boundaries, number and string representation of a line,
    filename, positions of target tokens and
    string representation of the context
    """

    def __init__(self):
        """
        Method for initializing of an empty context window
        """
        self.lineString = ""
        self.targetTokensPositions = []
        self.rightBoundary = 0
        self.leftBoundary = 0
        self.string = ""
        self.filename = ""
        self.lineNumber = -1

    @staticmethod
    def initWithData(lineString, tokenPositions, right, left, string, filename, lineNumber):
        """
        Method for creating a context window from preproccessored data
        @param lineString: string representation of the line
        @param tokenPositions: list of positions of target tokens
        @param right: the right boundary
        @param left: the left boundary
        @param string: string representation of the context
        @param filename: path to the source file
        @param lineNumber: number of the line in the file
        @return: ContextWindow
        """
        contextWindow = ContextWindow()
        contextWindow.lineString = lineString
        contextWindow.targetTokensPositions = tokenPositions
        contextWindow.rightBoundary = right
        contextWindow.leftBoundary = left
        contextWindow.string = string
        contextWindow.filename = filename
        contextWindow.lineNumber = lineNumber
        return contextWindow

    @staticmethod
    def makeWindowGreatAgain(size, filename, position):
        """
        Method for creating a context window using the source file and token position
        @param size: size of the context window
        @param filename: path to the source file
        @param position: position of the target token
        """
        contextWindow = ContextWindow()
        contextWindow.filename = filename
        contextWindow.lineNumber = position.posLine
        contextWindow.lineString = ""
        flag = False
        with open(filename, 'r') as f:
            for i, l in enumerate(f):
                if i+1 == position.posLine:
                    contextWindow.lineString = l
                    flag = True
        if flag == False:
            raise ValueError
        contextWindow.targetToken = contextWindow.lineString[position.posBegin:position.posEnd]
        contextWindow.targetTokensPositions = []
        contextWindow.targetTokensPositions.append(indexator.Position(
            position.posBegin, position.posEnd, position.posLine))
        right = ""
        # rightArray = []
        left = ""
        # leftArray = []
        rawTokens = tokenizer.Tokenizer().genclasstokenize(
            contextWindow.lineString[position.posEnd:])
        
        i = 0
        temp = ""  # buffer against wrong tokens
        # tempT = []
        for rawToken in rawTokens:
            if i < size:
                if '\n' in rawToken.string:
                    break
                temp += rawToken.string  # buffer updates till alpha/digit token
                # tempT.append(rawToken)
                # rightArray.append(rawToken)
                if (rawToken.category == 'alpha') or (rawToken.category == 'digit'):
                    right += temp  # buffer flushes to other context
                    temp = ""
                    # rightArray += tempT
                    # tempT = []
                    i += 1
            else:
                break
        contextWindow.rightBoundary = position.posEnd + len(right)
        rawTokensLeft = tokenizer.Tokenizer().genclasstokenize(
            contextWindow.lineString[position.posBegin - 1::-1])
        
        i = 0
        temp = ""
        # tempT = []
        for rawToken in rawTokensLeft:
            if i < size:
                if '\n' in rawToken.string:
                    break
                # print("token: '" + rawToken.string + "'")
                temp = rawToken.string[::-1] + temp
                # tempT.append(tokenizer.ClassifiedToken(
                    # rawToken.position, rawToken.string[::-1], rawToken.category))
                # leftArray.append(tokenizer.ClassifiedToken(
                #     rawToken.position, rawToken.string[::-1], rawToken.category))
                if (rawToken.category == 'alpha') or (rawToken.category == 'digit'):
                    left = temp + left
                    temp = ""
                    # leftArray += tempT
                    # tempT = []
                    i += 1
            else:
                break
        # leftArray = leftArray[::-1]
        contextWindow.leftBoundary = position.posBegin - len(left)
        contextWindow.string = left + contextWindow.targetToken + right
        return contextWindow

    def __eq__(self, someshit):
        """
        Method for comparison of two windows
        @param someshit: to what it should compare
        @return: True if positions are equel, False otherwise
        """
        return (self.targetTokensPositions == someshit.targetTokensPositions
                and self.lineString == someshit.lineString
                and self.rightBoundary == someshit.rightBoundary
                and self.leftBoundary == someshit.leftBoundary
                and self.string == someshit.string
                and self.filename == someshit.filename
                and self.lineNumber == someshit.lineNumber)

    def __repr__(self):
        """
        Method for representation a context window
        @return: string representation
        """
        return self.string

    def intersectWindows(self, windowB):
        """
        Method for intersecting two neighbouring context windows
        @param windowB: the right window to be intersected
        @return: combined ContextWindow
        """
        resultWindow = ContextWindow()
        resultWindow.lineString = self.lineString
        resultWindow.rightBoundary = windowB.rightBoundary
        resultWindow.leftBoundary = self.leftBoundary
        resultWindow.lineNumber = self.lineNumber
        resultWindow.filename = self.filename
        resultWindow.targetTokensPositions = []
        resultWindow.targetTokensPositions += self.targetTokensPositions
        resultWindow.targetTokensPositions += windowB.targetTokensPositions
        resultWindow.string = resultWindow.lineString[self.leftBoundary:windowB.rightBoundary]
        return resultWindow

    @staticmethod
    def unionWindows(windows):
        """
        Method for uniting a list of windows if there are some windows that need intersecting
        @param windows: the list of windows
        @return: list of combined ContextWindows
        """
        windowsUnited = []
        i = 0
        while i < len(windows):
            if  (i < len(windows) - 1) and (
                windows[i].filename == windows[i + 1].filename) and (
                windows[i].lineNumber == windows[i + 1].lineNumber) and (((
                windows[i].leftBoundary < windows[i + 1].rightBoundary) and (
                windows[i + 1].leftBoundary < windows[i].rightBoundary)) or ((
                windows[i + 1].leftBoundary == windows[i].rightBoundary) or (
                windows[i + 1].leftBoundary == windows[i].rightBoundary + 2) or (
                windows[i + 1].leftBoundary == windows[i].rightBoundary - 2))):
                    windowsUnited.append(windows[i].intersectWindows(windows[i + 1]))
                    i += 2
            else:
                windowsUnited.append(windows[i])
                i += 1
        return windowsUnited

    def expandToSentence(self):
        """
        Method for expanding a window to match sentence boundaries
        """
        i = 0
        str = self.lineString[self.rightBoundary:]
        while i < len(str):
            if ((str[i] == '.') or (str[i] == '?') or (str[i] == '!') and (
                str[i + 1] == " ") and (str[i + 2].isupper())):
                self.rightBoundary += i + 1
                self.string = self.lineString[self.leftBoundary:self.rightBoundary]
                break
            i += 1
        i = self.leftBoundary
        str = self.lineString[:self.leftBoundary]
        while i > 1:
            if ((str[i - 2] == '.') or (str[i - 2] == '?') or (str[i - 2] == '!') and (
                str[i - 1] == " ") and (str[i].isupper())):
                self.leftBoundary = i
                self.string = self.lineString[self.leftBoundary:self.rightBoundary]
                break
            i -= 1

    def markTarget(self):
        """
        Method for marking target tokens with bold formatting in a context window
        @return: string with bold formatting of target tokens
        """
        markedString = self.string
        print(markedString)
        for pos in self.targetTokensPositions:
            targetToken = self.lineString[pos.posBegin:pos.posEnd]
            print(targetToken)
            markedString = markedString.replace(targetToken, "<b>" + targetToken + "</b>")
            print(markedString)
        return markedString

class SearchEngine(object):
    """
    Tool for searching in a database
    """

    def __init__(self, dbName):
        """
        Method for initialization a search engine
        @param dbName: path of the database
        """
        self.db = shelve.open(dbName)

    def __del__(self):
        """
        Method for the end of the work with the search engine
        """
        try:
            self.db.close()
        except Exception:
            return

    def search(self, token):
        """
        Method for searching one word in the database
        @param token: a string (word) to be found
        @return: dictionary of filenames as keys and positions of tokens as values
        """   
        if isinstance(token, str):
            return self.db.get(token, {})
        else:
            raise ValueError

    def searchQuery(self, query):
        """
        Method for searching a query in the database
        Returns dictionary with filenames and positions of all tokens from the query
        @param query: a string of tokens to be found
        @return: dictionary of filenames as keys and positions of tokens as values
        """   
        if not(isinstance(query, str)):
            raise ValueError

        rawTokens = tokenizer.Tokenizer().genclasstokenize(query)
        tokens = indexator.Indexator.relevancyFilter(rawTokens)
        responds = []  # list of responds of search function for each token in the query
        for token in tokens:
            responds.append(self.search(token.string))
        files = set(responds[0].keys())  # set of filenames from first respond
        for d in responds[1:]:  # intersection of all filenames in all responds
            files.intersection_update(set(d.keys()))
        resultDict = {}
        for file in files:
            resultDict[file] = []  # for every file in intersection of files
            for d in responds:  # write as values all positions from intersection of files
                resultDict[file] += d.get(file, [])
        return resultDict

    # def searchQueryWindow(self, query, windowSize):
    #     """
    #     Method for searching a query in the database which returns windows
    #     @param query: a string of tokens to be found
    #     @return: dictionary of filenames as keys and context windows of tokens as values
    #     """
    #     positionDict = self.searchQuery(query)
    #     contextDict = {}
    #     for k in positionDict.keys():
    #         print(k)
    #         contexts = []
    #         for i in positionDict[k]:
    #             print(i)
    #             contexts.append(ContextWindow.makeWindowGreatAgain(
    #                 windowSize, k, i))
    #         contextDict[k] = ContextWindow().unionWindows(contexts)
    #     return contextDict


if __name__ == "__main__":
    with open('test.txt', 'w') as f:
        f.write('All we need is, all we need is, all we need is')
        # f.write('And he said yes. All we need is blood. How much pain it is')
    with open('testtest.txt', 'w') as f:
        f.write('Blood, blood, blood')
    with open('testtesttest.txt', 'w') as f:
        f.write('All we need is, all we need is,\n all we need is')
    with open('test.txt', 'r') as f:
        for i, l in enumerate(f):
            if i == 0:
                lineString = l
    targetToken = lineString[20:22]
    right = ""
    rightArray = []
    left = ""
    leftArray = []
    rawTokens = tokenizer.Tokenizer().genclasstokenize(lineString[22:])
    i = 0
    for rawToken in rawTokens:
        if i < 3:
            right += rawToken.string
            rightArray.append(rawToken)
            if (rawToken.category == 'alpha') or (rawToken.category == 'digit'):
                i += 1
    rawTokensLeft = tokenizer.Tokenizer().genclasstokenize(lineString[19::-1])
    i = 0
    for rawToken in rawTokensLeft:
        if i < 3:
            left = rawToken.string[::-1] + left
            leftArray.append(rawToken)
            if (rawToken.category == 'alpha') or (rawToken.category == 'digit'):
                i += 1
    # print(targetToken)
    # print(right)
    # print(left)
    # print(left + targetToken + right)
    
    pos2 = indexator.Position(20, 22, 1)
    pos1 = indexator.Position(23, 27, 1)
    context1 = ContextWindow.makeWindowGreatAgain(5, 'test.txt', pos1)
    context2 = ContextWindow.makeWindowGreatAgain(3, 'test.txt', pos2)
    contexts = []
    contexts.append(context1)
    contexts.append(context2)
    unionContexts = ContextWindow().unionWindows(contexts)
    # context1.expandToSentence()
    # print(context1.string)

    # string = "all we need is, all we need is"
    print(unionContexts[0].markTarget())
    
    # pos1 = indexator.Position(20, 22, 0)
    # pos2 = indexator.Position(32, 35, 0)
    # pos3 = indexator.Position(7, 12, 0)
    # pos4 = indexator.Position(20, 22, 0)
    # pos5 = indexator.Position(28, 30, 0)
    # pos6 = indexator.Position(1, 4, 1)
    # context1 = ContextWindow.makeWindowGreatAgain(2, 'test.txt', pos1)
    # context2 = ContextWindow.makeWindowGreatAgain(2, 'test.txt', pos2)
    # context3 = ContextWindow.makeWindowGreatAgain(1, 'testtest.txt', pos3)
    # context4 = ContextWindow.makeWindowGreatAgain(8, 'testtesttest.txt', pos4)
    # context5 = ContextWindow.makeWindowGreatAgain(2, 'testtesttest.txt', pos5)
    # context6 = ContextWindow.makeWindowGreatAgain(2, 'testtesttest.txt', pos6)
    # print("'" + context1.string + "'")
    # print("'" + context2.string + "'")
    # print("'" + context3.string + "'")
    # print("'" + context4.string + "'")
    # print("'" + context5.string + "'")
    # print("'" + context6.string + "'")
    # print("=======")
    # contexts = []
    # contexts.append(context1)
    # contexts.append(context2)
    # contexts.append(context3)
    # contexts.append(context4)
    # contexts.append(context5)
    # contexts.append(context6)
    # unionContexts = ContextWindow().unionWindows(contexts)
    # for u in unionContexts:
    #     print(u)
    # print("====================")
    # print(context.right)
    # print(context.left)
    # print(context.targetToken)
    # print(context.string)
    # print(context.leftBoundary)
    # print(context.rightBoundary)

    # string = "\n "
    # strings = tokenizer.Tokenizer().genclasstokenize(string)
    # for s in strings:
    #     print(s)

    files = os.listdir(path=".")
    for file in files:
        if file.startswith('test'):
            os.remove(file)