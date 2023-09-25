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
        """A generator function that reads one line at a time.
        Yields a tuple of <DOC>'s and </DOC>'s postion until EOF"""
        offset, endByte = 0, 0

        while line := self.__file.readline():
            if "<DOC>" in line:
                offset = self.__file.tell()
                continue

            if "</DOC>" in line:
                endByte = self.__file.tell()
                yield (offset, endByte)
                self.__file.seek(endByte)

    def nextDocument(self):
        """Get the next document info.
        Extract the content given the position info of the doc
        """
        # 1. When called, this API processes one document from corpus, and returns its doc number and content.
        # 2. When no document left, return null, and close the file.
        if docInfo := next(self.__docInfo, None):
            offset, endbyte = docInfo

            # Jump to offset
            self.__file.seek(offset)
            # Read content of size (endbyte - offset)
            doc = self.__file.read(endbyte - offset)
            docNo = self.__extract_content(doc, "DOCNO").strip()
            content = self.__extract_content(doc, "TEXT")
            return [docNo, content]
        else:
            self.__file.close()
            return docInfo

    def __extract_content(self, doc: str, tag: str):
        """Given the doc string and tag name, extract the content between the open tag and close tag."""
        openTag, closeTag = f"<{tag}>", f"</{tag}>"
        return doc[
            (start := doc.find(openTag) + len(openTag)) : doc.rfind(closeTag, start)
        ]
