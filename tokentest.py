import unittest
from tokenizator import Tokenizator

class Test(unittest.TestCase):
    def setUp(self):
        self.Tokenizator = Tokenizator()

    #unittests for tokenize method
    def test_list_type_output(self):
        result = self.Tokenizator.tokenize('some string')
        self.assertIsInstance(result, list)
        
    def test_list_type_number(self):
        with self.assertRaises(ValueError):
            self.Tokenizator.tokenize(13)
            
    def test_list_type_notlist(self):
        with self.assertRaises(ValueError):
            self.Tokenizator.tokenize([15, 'abc', 'stream'])

    def test_list_result_both_alpha(self):
        result = self.Tokenizator.tokenize('test !!!111some ,.,. string')
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].string, 'test')
        self.assertEqual(result[0].position, 0)
        self.assertEqual(result[2].string, 'string')
        self.assertEqual(result[2].position, 21)
        
    def test_list_result_both_notalpha(self):
        result = self.Tokenizator.tokenize(':)test !!!111some ,.,. string**')
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].string, 'test')
        self.assertEqual(result[0].position, 2)
        self.assertEqual(result[2].string, 'string')
        self.assertEqual(result[2].position, 23)
        
    def test_list_result_alpha_nonalpha(self):
        result = self.Tokenizator.tokenize('test !!!111some ,.,. string$^)')
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].string, 'test')
        self.assertEqual(result[0].position, 0)
        self.assertEqual(result[2].string, 'string')
        self.assertEqual(result[2].position, 21)
        
    def test_list_result_nonalpha_alpha(self):
        result = self.Tokenizator.tokenize('{test !!!111some ,.,. string')
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].string, 'test')
        self.assertEqual(result[0].position, 1)
        self.assertEqual(result[2].string, 'string')
        self.assertEqual(result[2].position, 22)

    #unittests for gentokenize method        
    def test_gen_type_number(self):
        with self.assertRaises(ValueError):
            self.Tokenizator.gentokenize(13)
            
    def test_gen_type_notlist(self):
        with self.assertRaises(ValueError):
            self.Tokenizator.gentokenize([15, 'abc', 'stream'])

    def test_gen_result_both_alpha(self):
        result = self.Tokenizator.gentokenize('test !!!111some ,.,. string')
        resultlist = list(result)
        self.assertEqual(len(resultlist), 3)
        self.assertEqual(resultlist[0].string, 'test')
        self.assertEqual(resultlist[0].position, 0)
        self.assertEqual(resultlist[2].string, 'string')
        self.assertEqual(resultlist[2].position, 21)
        
    def test_gen_result_both_notalpha(self):
        result = self.Tokenizator.gentokenize(':)test !!!111some ,.,. string**')
        resultlist = list(result)
        self.assertEqual(len(resultlist), 3)
        self.assertEqual(resultlist[0].string, 'test')
        self.assertEqual(resultlist[0].position, 2)
        self.assertEqual(resultlist[2].string, 'string')
        self.assertEqual(resultlist[2].position, 23)
        
    def test_gen_result_alpha_nonalpha(self):
        result = self.Tokenizator.gentokenize('test !!!111some ,.,. string$^)')
        resultlist = list(result)
        self.assertEqual(len(resultlist), 3)
        self.assertEqual(resultlist[0].string, 'test')
        self.assertEqual(resultlist[0].position, 0)
        self.assertEqual(resultlist[2].string, 'string')
        self.assertEqual(resultlist[2].position, 21)
        
    def test_gen_result_nonalpha_alpha(self):
        result = self.Tokenizator.gentokenize('{test !!!111some ,.,. string')
        resultlist = list(result)
        self.assertEqual(len(resultlist), 3)
        self.assertEqual(resultlist[0].string, 'test')
        self.assertEqual(resultlist[0].position, 1)
        self.assertEqual(resultlist[2].string, 'string')
        self.assertEqual(resultlist[2].position, 22)


if __name__ == '__main__':
    unittest.main()
