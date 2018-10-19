"""
Module for parsing a string to tokens
"""
import unicodedata


class Token(object):
    """
    Class representing a word.
    Remembers position in the stream and string representation
    """
    def __init__(self, position, string):
        """
        Method for initialization a simple token
        @param position: position of a token in the string
        @param string: string representation of a token
        """
        self.position = position
        self.string = string
        
    def __repr__(self):
        """
        Method for representation an exemplar of the Token class
        @return: string representation
        """
        return self.string + '_' + str(self.position)


class ClassifiedToken(Token):
    """
    Class representing a word.
    Remembers position in the stream, string representation
    and the type of the token - string/digit/punct/space/other
    """
    def __init__(self, position, string, category):
        """
        Method for initialization a simple token
        @param position: position of a token in the string
        @param string: string representation of a token
        @param category: type of a token - string/digit/punct/space/other
        """
        self.position = position
        self.string = string
        self.category = category
        
    def __repr__(self):
        """
        Method for representation an exemplar of the Token class
        @return: string representation
        """
        return self.string + ' ' + str(self.category) + ' ' + str(self.position)

    @staticmethod
    def _categorize_(sym):
        """
        Method for parsing, returns generator
        @param stream: string that needs parsing
        @return: generator
        """
        if sym.isalpha():
            return "alpha"
        else:
            if sym.isspace():
                return "space"
            else:
                if unicodedata.category(sym)[0] == 'P':
                    return "punct"
                else:
                    if sym.isdigit():
                        return "digit"
                    else:
                        return "other"


class Tokenizator(object):
    """
    Tool for tokenization using methods tokenize or gentokenize
    """
    def tokenize(self, stream):
        """
        Method for parsing, returns a list of Tokens
        @param stream: string that needs parsing
        @return: list of tokens
        """
        if not type(stream) is str:
            raise ValueError
        
        tokens = []
        index = -1 # -1 means previous symbol is not alpha
        for i, char in enumerate(stream):
            if index > -1 and not char.isalpha():  # end of a word
                word = Token(index, stream[index:i])
                tokens.append(word)
                index = -1
            if index == -1 and char.isalpha():  # beginning of a word
                index = i
        if char.isalpha():  # last word in the stream
            word = Token(index, stream[index:i+1])
            tokens.append(word)
        return tokens

    def gentokenize(self, stream):
        """
        Method for parsing, returns generator
        @param stream: string that needs parsing
        @return: generator
        """
        if not type(stream) is str:
            raise ValueError
        
        index = -1 # -1 means previous symbol is not alpha
        for i, char in enumerate(stream):
            if index > -1 and not char.isalpha():  # end of a word
                word = Token(index, stream[index:i])
                yield word
                index = -1
            if index == -1 and char.isalpha():  # beginning of a word
                index = i
        if char.isalpha():  # last word in the stream
            word = Token(index, stream[index:i+1])
            yield word

    def genclasstokenize(self, stream):
        """
        Method for parsing
        Returns Tokens of string/digit/punct/space/other classes
        @param stream: string that needs parsing
        @return: generator
        """
        if not type(stream) is str:
            raise ValueError

        index = 0 # beginning of a token
        precat = ClassifiedToken._categorize_(stream[0]) # category of the previous token
        for i, char in enumerate(stream):
            if ClassifiedToken._categorize_(char) != precat:
                word = ClassifiedToken(index, stream[index:i], precat)
                index = i
                precat = ClassifiedToken._categorize_(char)
                yield word
        word = ClassifiedToken(index, stream[index:i+1], precat)   # last token
        yield word

if __name__ == '__main__':
    stream = "!!some bloody string 123**"
    #stream = "   12мама мыла3   раму!!"
    #words = Tokenizator().tokenize(stream)
    #print(words)
    #words = Tokenizator().gentokenize(stream)
    #wordlist = list(words)
    #print(wordlist)
    wordclasses = Tokenizator().genclasstokenize(stream)
    wordclasseslist = list(wordclasses)
    print(wordclasseslist)
