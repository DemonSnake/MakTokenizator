import os
import shelve
from tokenizer import Tokenizer


class Position(object):
    def __init__ (self, posBegin, posEnd):
        self.posBegin = posBegin
        self.posEnd = posEnd

    def __eq__(self, someshit):
        return (self.posBegin == someshit.posBegin
                and self.posEnd == someshit.posEnd)

    def __repr__(self):
        return str(self.posBegin) + ', ' + str(self.posEnd)

class Indexator(object):
    def __init__(self, filename):
        self.database = shelve.open(filename, writeback=True)

    def __del__(self):
        try:
            self.database.close()
        except Exception:
            return

    def relevancyFilter(self, tokens):
        for token in tokens:
            if token.category == "alpha" or token.category == "digit":
                yield token
    
    def indexize(self, filename):       
        try:
            file = open(filename)       
        except Exception:
            raise ValueError
        
        stream = file.read()
        file.close()
        tokens = Tokenizer().genclasstokenize(stream)
        usefulTokens = self.relevancyFilter(tokens)
        for token in usefulTokens:
            self.database.setdefault(token.string,
                                {}).setdefault(filename,
                                               []).append(Position(token.position,
                                                                       token.position
                                                                       + len(token.string)))
        self.database.sync()
        return

    @classmethod
    def _coveredRetreat(self):
        files = os.listdir(path=".")
        for file in files:
            if file == 'test.txt':
                os.remove(file)
            if file.startswith('TestDatabase.'):
                os.remove(file)
            if file == 'TestDatabase':
                os.remove(file)
        return
    

if __name__ == "__main__":
    Indexator._coveredRetreat()
    sIndexator = Indexator("TestDatabase")

    filename = open('test.txt', 'w')
    filename.write('BRP arena is easy')
    filename.close()
    sIndexator.indexize('test.txt')
    dbdict = dict(sIndexator.database)
    expected = {'BRP': {'test.txt': [Position(0,3)]},
                'arena': {'test.txt': [Position(4,9)]},
                'is': {'test.txt': [Position(10,12)]},
                'easy': {'test.txt': [Position(13,17)]}}
    flag = dbdict == expected
    print(flag)
    print(dbdict)
    print(expected)
    Indexator._coveredRetreat()
