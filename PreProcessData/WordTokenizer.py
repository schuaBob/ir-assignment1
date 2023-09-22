import re


# Efficiency and memory cost should be paid with extra attention.
# Essential private methods or variables can be added.
# Please add comments along with your code.
class WordTokenizer:
    def __init__(self, content: str):
        # Tokenize the input texts.
        self.__tokens = self.__prepare_tokens(content)
        # next(self.__tokens)
        return

    def __prepare_tokens(self, content: str):
        for tk in re.split(r"\s+|\W+|\d+", content.strip()):
            if tk:
                yield tk

    def nextWord(self):
        # Return the next word in the document.
        # Return null, if it is the end of the document.
        word = next(self.__tokens, None)
        return word
