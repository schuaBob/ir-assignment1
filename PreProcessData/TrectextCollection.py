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
        self.__docInfo = self.__prepare_file()
        return

    def __prepare_file(self):
        offset, totalLines = 0, 0
        offset2 = 0
        # to be removed
        i = 0
        while line := self.__file.readline():
            # to be removed
            if i == 3:
                break
            if "<DOC>" in line:
                offset = self.__file.tell()
                continue

            if "</DOC>" in line:
                i += 1
                offset2 = self.__file.tell()
                yield (offset, offset2 - len(line))
                totalLines = 0
                self.__file.seek(offset2)
                # to be removed
            else:
                totalLines += 1

    def nextDocument(self):
        # 1. When called, this API processes one document from corpus, and returns its doc number and content.
        # 2. When no document left, return null, and close the file.
        if docInfo := next(self.__docInfo, None):
            offset, endbyte = docInfo
            self.__file.seek(offset)
            doc = self.__file.read(endbyte - offset)
            docNo = self.__get_tag_content("DOCNO", doc)
            content = self.__get_tag_content("TEXT", doc)
            return [docNo, content]
        else:
            self.__file.close()
            return docInfo

    def __get_tag_content(self, tag: str, doc: str):
        openTag, closeTag = f"<{tag}>", f"</{tag}>"
        return doc[
            (start := doc.find(openTag) + len(openTag)) : doc.find(closeTag, start)
        ].strip()
