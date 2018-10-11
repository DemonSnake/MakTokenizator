"""
Module for parsing a string to tokens
"""
class Token(object):
    """
    Class representing a word.
    Remembers position in the stream and string representation
    """
    def __init__(self, position, string):
        self.position = position
        self.string = string
    def __repr__(self):
        return self.string + '_' + str(self.position)

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

if __name__ == '__main__':
    stream = "   12мама мыла3   раму!!"
    words = Tokenizator().tokenize(stream)
    print(words)
    words = Tokenizator().gentokenize(stream)
    wordlist = list(words)
    print(wordlist)
