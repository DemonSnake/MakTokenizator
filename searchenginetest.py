import unittest
import os
import shelve
import indexator
import searchEngine
from indexator import Indexator
from searchEngine import SearchEngine


class Test(unittest.TestCase):

    def setUp(self):
        with open('test0.txt', 'w') as f:
            f.write('All we need is,\n all we need is,\n all we need is')
        with open('test1.txt', 'w') as f:
            f.write('Blood, blood,\n blood')
        with open('test2.txt', 'w') as f:
            f.write('All we need is, all we need is,\n all we need is')
        with open('test.txt', 'w') as f:
            f.write('All we need is, all we need is, all we need is')
        with open('testtest.txt', 'w') as f:
            f.write('Blood, blood, blood')
        with open('testtesttest.txt', 'w') as f:
            f.write('All we need is, all we need is,\n all we need is')
        with open('testSentence.txt', 'w') as f:
            f.write('What do we need? All we need is blood. Pain pain pain pain')
        indexer = Indexator('TestDatabase')
        indexer.indexize('test0.txt')
        indexer.indexize('test1.txt')
        indexer.indexize('test2.txt')
        self.searchEngine = SearchEngine("TestDatabase")

    # unittests for search
    def test_input_type_number(self):
        with self.assertRaises(ValueError):
            self.searchEngine.search(13)
        
    def test_input_type_not_exists(self):
        self.assertEqual(self.searchEngine.search('вискас'), {})

    def test_we(self):
        expected = {
            'test0.txt': [
                indexator.Position(4, 6, 1), 
                indexator.Position(5, 7, 2), 
                indexator.Position(5, 7, 3)], 
            'test2.txt': [
                indexator.Position(4, 6, 1), 
                indexator.Position(20, 22, 1), 
                indexator.Position(5, 7, 2)]}
        self.assertEqual(self.searchEngine.search('we'), expected)

    def test_blood(self):
        expected = {
            'test1.txt': [
                indexator.Position(7, 12, 1), 
                indexator.Position(1, 6, 2)]}
        self.assertEqual(self.searchEngine.search("blood"), expected)

    # unittests for searchQuery
    def test__query_input_type_number(self):
        with self.assertRaises(ValueError):
            self.searchEngine.searchQuery(13)
        
    def test_query_input_type_not_exists(self):
        self.assertEqual(self.searchEngine.searchQuery('вискас'), {})

    def test_we_is(self):
        expected = {
            'test0.txt': [
                indexator.Position(4, 6, 1),
                indexator.Position(5, 7, 2),
                indexator.Position(5, 7, 3),
                indexator.Position(12, 14, 1),
                indexator.Position(13, 15, 2),
                indexator.Position(13, 15, 3)],
            'test2.txt': [
                indexator.Position(4, 6, 1),
                indexator.Position(20, 22, 1),
                indexator.Position(5, 7, 2),
                indexator.Position(12, 14, 1),
                indexator.Position(28, 30, 1),
                indexator.Position(13, 15, 2)]}
        self.assertEqual(self.searchEngine.searchQuery('we is'), expected)

    def test_need(self):
        expected = {
            'test0.txt': [
                indexator.Position(7, 11, 1), 
                indexator.Position(8, 12, 2), 
                indexator.Position(8, 12, 3)],
            'test2.txt': [
                indexator.Position(7, 11, 1), 
                indexator.Position(23, 27, 1), 
                indexator.Position(8, 12, 2)]}
        self.assertEqual(self.searchEngine.searchQuery('need'), expected)  

    # unittests for contexts
    def test_context(self):
        pos = indexator.Position(20, 22, 1)
        context = searchEngine.ContextWindow.makeWindowGreatAgain(2, 'test.txt', pos)
        self.assertEqual(context.string, "is, all we need is")

    def test_context_line_not_exists(self):
        pos = indexator.Position(20, 22, 2)
        with self.assertRaises(ValueError):
            searchEngine.ContextWindow.makeWindowGreatAgain(2, 'test.txt', pos)

    def test_context_large_size(self):
        pos = indexator.Position(20, 22, 1)
        context = searchEngine.ContextWindow.makeWindowGreatAgain(8, 'test.txt', pos)
        self.assertEqual(context.string, "All we need is, all we need is, all we need is")

    def test_context_zero_size(self):
        pos = indexator.Position(20, 22, 1)
        context = searchEngine.ContextWindow.makeWindowGreatAgain(0, 'test.txt', pos)
        self.assertEqual(context.string, "we")

    def test_context_two_windows(self):
        poss = [indexator.Position(20, 22, 1),
                indexator.Position(32, 35, 1)]
        contexts = [searchEngine.ContextWindow.makeWindowGreatAgain(2, 'test.txt', poss[0]), 
                    searchEngine.ContextWindow.makeWindowGreatAgain(2, 'test.txt', poss[1])]
        contextUnion = searchEngine.ContextWindow().unionWindows(contexts)
        targetTokensPositions = [indexator.Position(20, 22, 1),
                                 indexator.Position(32, 35, 1)]
        expected = searchEngine.ContextWindow.initWithData(
            "All we need is, all we need is, all we need is", 
            targetTokensPositions, 
            43, 12, "is, all we need is, all we need", "test.txt", 1)
        expectedList = []
        expectedList.append(expected)
        self.assertEqual(contextUnion, expectedList)

    def test_context_many_windows(self):
        poss = [indexator.Position(20, 22, 1),
                indexator.Position(32, 35, 1),
                indexator.Position(7, 12, 1),
                indexator.Position(20, 22, 1), 
                indexator.Position(28, 30, 1),
                indexator.Position(1, 4, 2)]
        contexts = [searchEngine.ContextWindow.makeWindowGreatAgain(2, 'test.txt', poss[0]), 
                    searchEngine.ContextWindow.makeWindowGreatAgain(2, 'test.txt', poss[1]), 
                    searchEngine.ContextWindow.makeWindowGreatAgain(1, 'testtest.txt', poss[2]), 
                    searchEngine.ContextWindow.makeWindowGreatAgain(8, 'testtesttest.txt', poss[3]), 
                    searchEngine.ContextWindow.makeWindowGreatAgain(2, 'testtesttest.txt', poss[4]),
                    searchEngine.ContextWindow.makeWindowGreatAgain(2, 'testtesttest.txt', poss[5])]
        contextUnion = searchEngine.ContextWindow().unionWindows(contexts)

        targetTokensPositions1 = [indexator.Position(20, 22, 1),
                                  indexator.Position(32, 35, 1)]
        expected1 = searchEngine.ContextWindow.initWithData(
            "All we need is, all we need is, all we need is", 
            targetTokensPositions1, 
            43, 12, "is, all we need is, all we need", "test.txt", 1)

        targetTokensPositions2 = [indexator.Position(7, 12, 1)]
        expected2 = searchEngine.ContextWindow.initWithData(
            "Blood, blood, blood", 
            targetTokensPositions2, 
            19, 0, "Blood, blood, blood", "testtest.txt", 1)

        targetTokensPositions3 = [indexator.Position(20, 22, 1),
                                  indexator.Position(28, 30, 1)]
        expected3 = searchEngine.ContextWindow.initWithData(
            "All we need is, all we need is,\n", 
            targetTokensPositions3, 
            30, 0, "All we need is, all we need is", "testtesttest.txt", 1)

        targetTokensPositions4 = [indexator.Position(1, 4, 2)]
        expected4 = searchEngine.ContextWindow.initWithData(
            " all we need is", 
            targetTokensPositions4, 
            12, 1, "all we need", "testtesttest.txt", 2)

        expectedList = []
        expectedList.append(expected1)
        expectedList.append(expected2)
        expectedList.append(expected3)
        expectedList.append(expected4)
        self.assertEqual(contextUnion, expectedList)

    def test_context_expand_to_sentence(self):
        pos = indexator.Position(24, 28, 1)
        context = searchEngine.ContextWindow.makeWindowGreatAgain(1, 'testSentence.txt', pos)
        context.expandToSentence()
        targetTokensPositions = [indexator.Position(24, 28, 1)]
        expected = searchEngine.ContextWindow.initWithData(
            "What do we need? All we need is blood. Pain pain pain pain", 
            targetTokensPositions, 
            38, 17, "All we need is blood.", "testSentence.txt", 1)
        self.assertEqual(context, expected)
        
    def test_context_expand_to_sentence_two_tokens(self):
        poss = [indexator.Position(21, 23, 1),
                indexator.Position(24, 28, 1)]
        contexts = [searchEngine.ContextWindow.makeWindowGreatAgain(1, 'testSentence.txt', poss[0]), 
                    searchEngine.ContextWindow.makeWindowGreatAgain(1, 'testSentence.txt', poss[1])]
        contextUnion = searchEngine.ContextWindow().unionWindows(contexts)
        contextUnion[0].expandToSentence()
        context = contextUnion[0]
        targetTokensPositions = [indexator.Position(21, 23, 1),
                                 indexator.Position(24, 28, 1)]
        expected = searchEngine.ContextWindow.initWithData(
            "What do we need? All we need is blood. Pain pain pain pain", 
            targetTokensPositions, 
            38, 17, "All we need is blood.", "testSentence.txt", 1)
        self.assertEqual(context, expected)

    # def test_query_context(self):
    #     expected = {
    #         'test.txt': [
    #             indexator.Position(4, 6, 1),
    #             indexator.Position(5, 7, 2),
    #             indexator.Position(5, 7, 3),
    #             indexator.Position(12, 14, 1),
    #             indexator.Position(13, 15, 2),
    #             indexator.Position(13, 15, 3)],
    #         'test2.txt': [
    #             indexator.Position(4, 6, 1),
    #             indexator.Position(20, 22, 1),
    #             indexator.Position(5, 7, 2),
    #             indexator.Position(12, 14, 1),
    #             indexator.Position(28, 30, 1),
    #             indexator.Position(13, 15, 2)]}
    #     print(searchEngine.ContextWindow.makeWindowGreatAgain(
    #         3, 'test0.txt', indexator.Position(12, 14, 1),))
    #     self.assertEqual(self.searchEngine.searchQueryWindow('blood pain', 3), expected)

    def tearDown(self):
        self.searchEngine.__del__()
        files = os.listdir(path=".")
        for file in files:
            if file.startswith('TestDatabase'):
                os.remove(file)
            if file.startswith('test'):
                os.remove(file)

if __name__ == '__main__':
    unittest.main()
