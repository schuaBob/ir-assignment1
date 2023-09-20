import Classes.Path as Path


# Efficiency and memory cost should be paid with extra attention.
# Essential private methods or variables can be added.
# Please add comments along with your code.
class TrectextCollection:
    def __init__(self):
        # 1. Open the file in Path.DataTextDir.
        # 2. Make preparation for function nextDocument().
        # NT: you cannot load the whole corpus into memory!!
        self.__file = open(Path.DataTextDir, "r")
        self.docInfo = self.__prepare_file()
        return

    def __prepare_file(self):
        contentStart, contentLines = 0, 0
        i = 0
        while line := self.__file.readline():
            if "<DOC>" in line:
                contentStart = self.__file.tell()
                continue

            if "</DOC>" in line:
                yield (contentStart, contentLines)
                contentLines = 0
                i+=1
            else:
                contentLines += 1


    def nextDocument(self):
        # 1. When called, this API processes one document from corpus, and returns its doc number and content.
        # 2. When no document left, return null, and close the file.
        
        docNo = ""
        content = ""
        return [docNo, content]

    def __del__(self):
        self.__file.close()
