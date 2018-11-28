import unittest
import os
import shelve
from indexator import Indexator


class Test(unittest.TestCase):
    def setUp(self):
        self.Indexator = Indexator()

    #unittests for indexize method
    def test_input_type_number(self):
        with self.assertRaises(ValueError):
            self.Indexator.indexize(13)
        
    def test_input_type_not_exists(self):
        with self.assertRaises(ValueError):
            self.Indexator.indexize('magsorcsareop.txt')

    def test_result_one_file(self):
        filename = open('test.txt', 'w')
        filename.write('word')
        filename.close()
        self.Indexator.indexize('test.txt')
        flag = False
        files = os.listdir(path = ".")
        if os.name == 'nt':
            for file in files:
                if file.startswith('database.'):
                    flag = True
        else:
            for file in files:
                if file == 'database':
                    flag = True
        self.assertEqual(flag, True)
        dbdict = dict(database)
        expected = {'word':{'test.txt':[Position(0,4)]}}
        self.assertEqual(dbdict, expected)

    def test_result_another_file(self):
        filename = open('bloodytest.txt', 'w')
        filename.write('word')
        filename.close()
        self.Indexator.indexize('bloodytest.txt')
        dbdict = dict(database)
        expected = {'word':{'test.txt': Position(0,4),
                            'bloodytest.txt': Position(0,4)}}
        self.assertEqual(dbdict, expected)

    def test_result_another_word(self):
        filename = open('goddamntest.txt', 'w')
        filename.write('arena')
        filename.close()
        self.Indexator.indexize('goddamntest.txt')
        dbdict = dict(database)
        expected = {'word': {'test.txt': Position(0,4),
                            'bloodytest.txt': Position(0,4)},
                    'arena': {'goddamntest.txt': Position(0,5)}}
        self.assertEqual(dbdict, expected)

    def test_result_many_words(self):
        filename = open('longlongtest.txt', 'w')
        filename.write('BRP arena is easy')
        filename.close()
        self.Indexator.indexize('longlongtest.txt')
        dbdict = dict(database)
        expected = {'word': {'test.txt': Position(0,4),
                            'bloodytest.txt': Position(0,4)},
                    'arena': {'goddamntest.txt': Position(0,5),
                              'longlongtest.txt': Position(4,9)},
                    'BRP': {'longlongtest.txt': Position(0,3)},
                    'is': {'longlongtest.txt': Position(10,12)},
                    'easy': {'longlongtest.txt': Position(13,17)}}
        self.assertEqual(dbdict, expected)

    def test_result_two_files(self):
        filename = open('firstrun.txt', 'w')
        filename.write('easy')
        filename.close()
        self.Indexator.indexize('firstrun.txt')
        dbdict = dict(database)
        expected = {'word': {'test.txt': Position(0,4),
                            'bloodytest.txt': Position(0,4)},
                    'arena': {'goddamntest.txt': Position(0,5),
                              'longlongtest.txt': Position(4,9)},
                    'BRP': {'longlongtest.txt': Position(0,3)},
                    'is': {'longlongtest.txt': Position(10,12)},
                    'easy': {'longlongtest.txt': Position(13,17),
                             'firstrun.txt': Position(0,4)}}
        self.assertEqual(dbdict, expected)
        filename = open('secondrun.txt', 'w')
        filename.write('too easy')
        filename.close()
        self.Indexator.indexize('secondrun.txt')
        dbdict = dict(database)
        expected = {'word': {'test.txt': Position(0,4), 
                            'bloodytest.txt': Position(0,4)}, 
                    'arena': {'goddamntest.txt': Position(0,5), 
                              'longlongtest.txt': Position(4,9)}, 
                    'BRP': {'longlongtest.txt': Position(0,3)}, 
                    'is': {'longlongtest.txt': Position(10,12)}, 
                    'easy': {'longlongtest.txt': Position(13,17), 
                             'firstrun.txt': Position(0,4), 
                             'secondrun.txt': Position(4,8)},
                    'too': {'secondrun.txt': Position(0,3)}}
        self.assertEqual(dbdict, expected)

    def tearDown(self):
        files = os.listdir(path = ".")
        for file in files:
            if file == 'test.txt':
                os.remove(file)
            if file == 'bloodytest.txt':
                os.remove(file)
            if file == 'goddamntest.txt':
                os.remove(file)
            if file == 'longlongtest.txt':
                os.remove(file)
            if file == 'firstrun.txt':
                os.remove(file)
            if file == 'secondrun.txt':
                os.remove(file)

if __name__ == '__main__':
    unittest.main()
