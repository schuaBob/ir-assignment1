import Classes.Path as Path
from tokenize import tokenize, NAME, STRING, generate_tokens
from io import BytesIO, StringIO
import string
import re
# Efficiency and memory cost should be paid with extra attention.
# Essential private methods or variables can be added.
# Please add comments along with your code.
class WordTokenizer:

    def __init__(self, content:str):
        # Tokenize the input texts.
        self.__tokens = self.__prepare_tokens(content)
        # next(self.__tokens)
        return
    
    def __prepare_tokens(self, content: str):
        # bytes = content.strip().translate(str.maketrans("", "", string.punctuation)).encode()
        # print(repr(content))
        for tk in re.split(r"\s+|\W+", content):
            yield tk
        # try:
        #     for tkInfo in tokenize(BytesIO(content.encode()).readline):
        #         if tkInfo.type in [STRING, NAME]:
        #             yield tkInfo.string
        # except Exception as e:
        #     print(tkInfo.string)
        #     print(e)

    def nextWord(self):
        # Return the next word in the document.
        # Return null, if it is the end of the document.
        word = next(self.__tokens, None)
        return word