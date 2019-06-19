"""
Module for searching some query in a database
"""
import shelve
import tokenizer
import indexator
from indexator import Indexator


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


# if __name__ == "__main__":
    # searchEngine = SearchEngine("TestDatabase")
    # with open('test0.txt', 'w') as f:
    #     f.write('All we need is,\n all we need is,\n all we need is')
    # with open('test1.txt', 'w') as f:
    #     f.write('Blood, blood,\n blood')
    # with open('test2.txt', 'w') as f:
    #     f.write('All we need is, all we need is,\n all we need is')
    # index = indexator.Indexator('TestDatabase')
    # index.indexize('test0.txt')
    # index.indexize('test1.txt')
    # index.indexize('test2.txt')
    # index.__del__()
    # print(searchEngine.search("blood"))