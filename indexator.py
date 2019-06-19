"""
Module for creating a database of tokens from a text file
"""
import os
import shelve
from tokenizer import Tokenizer


class Position(object):
    """
    Class for representation of a token's position
    Remembers the beginning, the end and the line of a token
    """
    # def __init__ (self, posBegin, posEnd):
    #     self.posBegin = posBegin
    #     self.posEnd = posEnd

    def __init__ (self, posBegin, posEnd, posLine):
        """
        Method for initialization position
        @param posBegin: position of a token in the string
        @param posEnd: string representation of a token
        @param posLine: string representation of a token
        """
        self.posBegin = posBegin
        self.posEnd = posEnd
        self.posLine = posLine

    # def __eq__(self, someshit):
    #     return (self.posBegin == someshit.posBegin
    #             and self.posEnd == someshit.posEnd)

    def __eq__(self, someshit):
        """
        Method for comparison of two positions
        @param someshit: to what it should compare
        @return: True if positions are equel, False otherwise
        """
        return (self.posBegin == someshit.posBegin
                and self.posEnd == someshit.posEnd
                and self.posLine == someshit.posLine)

    # def __repr__(self):
    #     return str(self.posBegin) + ', ' + str(self.posEnd)

    def __repr__(self):
        """
        Method for representation a position of a token
        @return: string representation
        """
        return '(' + str(self.posBegin) + ', ' + str(self.posEnd) + ', ' + str(self.posLine) + ')' 


class Indexator(object):
    """
    Tool for indexizing text files
    """
    def __init__(self, filename):
        """
        Method for initialization an indexator
        @param filename: path of the database to be created
        """
        self.database = shelve.open(filename, writeback=True)

    def __del__(self):
        """
        Method for the end of the work with the database
        """
        try:
            self.database.close()
        except Exception:
            return

    @staticmethod
    def relevancyFilter(tokens):
        """
        Method for extraction of tokens of type alpha or digit
        @param tokens: collection of ClassifiedTokens
        @return: generator of tokens of type alpha or digit
        """
        for token in tokens:
            if token.category == "alpha" or token.category == "digit":
                yield token
    
    def indexize(self, filename):
        """
        Method for indexizing a file
        Modifies the database of the indexator
        @param filename: path to a file that needs indexizing
        """       
        try:
            file = open(filename)       
        except Exception:
            raise ValueError

        lineNumber = 1
        # file0 = [i for i in file]
        # file.close()
        for line in file:
            # print(lineNumber, '/', len(file0))
            tokens = Tokenizer().genclasstokenize(line)
            usefulTokens = Indexator.relevancyFilter(tokens)
            for token in usefulTokens:
                self.database.setdefault(
                    token.string, {}).setdefault(
                        filename, []).append(
                            Position(
                                token.position,
                                token.position + len(token.string),
                                lineNumber))
            lineNumber = lineNumber + 1
        self.database.sync()
        file.close()
        return

    # @classmethod
    # def _coveredRetreat(self):
    #     files = os.listdir(path=".")
    #     for file in files:
    #         if file == 'test.txt':
    #             os.remove(file)
    #         if file.startswith('TestDatabase.'):
    #             os.remove(file)
    #         if file == 'TestDatabase':
    #             os.remove(file)
    #     return


if __name__ == "__main__":
    """     Indexator._coveredRetreat()
    sIndexator = Indexator("TestDatabase")

    filename = open('test.txt', 'w')
    filename.write('BRP arena\nis very\nvery easy')
    filename.close()
    sIndexator.indexize('test.txt')
    dbdict = dict(sIndexator.database)
    expected = {'BRP': {'test.txt': [Position(0,3,1)]},
                'arena': {'test.txt': [Position(4,9,1)]},
                'is': {'test.txt': [Position(0,2,2)]},
                'easy': {'test.txt': [Position(5,9,3)]},
                'very': {'test.txt': [Position(3,7,2)],
                         'test.txt': [Position(0,4,3)]}}

    print(dbdict)
    print(expected)
    Indexator._coveredRetreat() """

    """ sIndexator = Indexator("ViMDatabase")
    print('1st:')
    sIndexator.indexize('tolstoy1.txt')
    print('2nd:')
    sIndexator.indexize('tolstoy2.txt')
    print('3rd:')
    sIndexator.indexize('tolstoy3.txt')
    print('4th:')
    sIndexator.indexize('tolstoy4.txt')
    dbdict = dict(sIndexator.database) """

    db = shelve.open('ViMDataBase')
    print(db['дуб'])