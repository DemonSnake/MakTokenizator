import unittest
import os
import shelve
import indexator
from indexator import Indexator


class Test(unittest.TestCase):
    def setUp(self):
        self.Indexator = Indexator("TestDatabase")

    #unittests for indexize method
    def test_input_type_number(self):
        with self.assertRaises(ValueError):
            self.Indexator.indexize(13)
        
    def test_input_type_not_exists(self):
        with self.assertRaises(ValueError):
            self.Indexator.indexize('magsorcsareop.txt')

    def test_result_one_file_one_word(self):
        filename = open('test.txt', 'w')
        filename.write('word')
        filename.close()
        self.Indexator.indexize('test.txt')
        flag = False
        files = os.listdir(path=".")
        if os.name == 'nt':
            for file in files:
                if file.startswith('TestDatabase.'):
                    flag = True
        else:
            for file in files:
                if file == 'TestDatabase':
                    flag = True
        self.assertEqual(flag, True)
        dbdict = dict(self.Indexator.database)
        expected = {'word':{'test.txt': [indexator.Position(0,4)]}}
        self.assertEqual(dbdict, expected)

    def test_result_one_file_many_words(self):
        filename = open('test.txt', 'w')
        filename.write('BRP arena is easy')
        filename.close()
        self.Indexator.indexize('test.txt')
        dbdict = dict(self.Indexator.database)
        expected = {'BRP': {'test.txt': [indexator.Position(0,3)]},
                    'arena': {'test.txt': [indexator.Position(4,9)]},
                    'is': {'test.txt': [indexator.Position(10,12)]},
                    'easy': {'test.txt': [indexator.Position(13,17)]}}
        self.assertEqual(dbdict, expected)

    def test_result_two_files_one_word(self):
        filename = open('firstrun.txt', 'w')
        filename.write('easy')
        filename.close()
        self.Indexator.indexize('firstrun.txt')
        filename = open('secondrun.txt', 'w')
        filename.write('easy')
        filename.close()
        self.Indexator.indexize('secondrun.txt')
        dbdict = dict(self.Indexator.database)
        expected = {'easy': {'firstrun.txt': [indexator.Position(0,4)], 
                             'secondrun.txt': [indexator.Position(0,4)]}}
        self.assertEqual(dbdict, expected)

    def test_result_two_files_many_words(self):
        filename = open('firstrun.txt', 'w')
        filename.write('too easy')
        filename.close()
        self.Indexator.indexize('firstrun.txt')
        filename = open('secondrun.txt', 'w')
        filename.write('not so easy')
        filename.close()
        self.Indexator.indexize('secondrun.txt')
        dbdict = dict(self.Indexator.database)
        expected = {'too': {'firstrun.txt': [indexator.Position(0,3)]}, 
                    'not': {'secondrun.txt': [indexator.Position(0,3)]}, 
                    'so': {'secondrun.txt': [indexator.Position(4,6)]}, 
                    'easy': {'firstrun.txt': [indexator.Position(4,8)], 
                             'secondrun.txt': [indexator.Position(7,11)]}}
        self.assertEqual(dbdict, expected)
    
    def tearDown(self):
        try:
            self.Indexator.database.close()
        except Exception:
            a = 5
        
        files = os.listdir(path=".")
        for file in files:
            if file == 'test.txt':
                os.remove(file)
            if file == 'firstrun.txt':
                os.remove(file)
            if file == 'secondrun.txt':
                os.remove(file)
            if file.startswith('TestDatabase.'):
                os.remove(file)
            if file == 'TestDatabase':
                os.remove(file)
        

if __name__ == '__main__':
    unittest.main()
