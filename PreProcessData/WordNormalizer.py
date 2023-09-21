import Classes.Path as Path
from nltk.stem import PorterStemmer

# Efficiency and memory cost should be paid with extra attention.
# Essential private methods or variables can be added.
# Please add comments along with your code.
class WordNormalizer:

    def __init__(self):
        self.__stemmer = PorterStemmer()
        return

    def lowercase(self, word:str):
        # Transform the word uppercase characters into lowercase.
        return word.lower()

    def stem(self, word:str):
        # Return the stemmed word with PorterStemmer imported previously.
        return self.__stemmer.stem(word, to_lowercase=False)
