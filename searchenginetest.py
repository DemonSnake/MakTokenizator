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
        indexer = Indexator('TestDatabase')
        indexer.indexize('test0.txt')
        indexer.indexize('test1.txt')
        indexer.indexize('test2.txt')
        self.searchEngine = SearchEngine("TestDatabase")

    #unittests for search
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
