import Classes.Path as Path
from html.parser import HTMLParser
from tempfile import NamedTemporaryFile, mkdtemp
import shutil
import os


# Efficiency and memory cost should be paid with extra attention.
# Essential private methods or variables can be added.
# Please add comments along with your code.
class TrecwebCollection:
    def __init__(self):
        # 1. Open the file in Path.DataWebDir.
        # 2. Make preparation for function nextDocument().
        # NT: you cannot load the whole corpus into memory!!
        self.__file = open(Path.DataWebDir, "r")
        self.__docInfo = self.__prepare_file()
        self.__htmlParser = TrecHTMLParser()
        return

    def __prepare_file(self):
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
        # 1. When called, this API processes one document from corpus, and returns its doc number and content.
        # 2. When no document left, return null, and close the file.
        # 3. the HTML tags should be removed in document content.
        if docInfo := next(self.__docInfo, None):
            offset, endbyte = docInfo
            self.__file.seek(offset)
            doc = self.__file.read(endbyte - offset)
            docNo = self.__extract_content(doc, "DOCNO").strip()
            self.__htmlParser.feed(self.__extract_content(doc, "</DOCHDR>", "</DOC>"))
            content = self.__htmlParser.get_content()
            return [docNo, content]
        else:
            self.__file.close()
            return docInfo

    def __extract_content(self, doc: str, startTag: str, endTag: str = None):
        openTag = f"<{startTag}>" if not endTag else startTag
        closeTag = endTag if endTag else f"</{startTag}>"
        return doc[
            (start := doc.find(openTag) + len(openTag)) : doc.find(closeTag, start)
        ]


class TrecHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.__tmpDir = mkdtemp(dir=os.path.dirname(__file__))
        self.__tmpFile = self.__new_tmp_file(self.__tmpDir)

    def handle_data(self, data: str):
        self.__tmpFile.write(data)

    def get_content(self):
        self.__tmpFile.seek(0)
        content = self.__tmpFile.read()
        self.__tmpFile.close()
        self.__tmpFile = self.__new_tmp_file(self.__tmpDir)
        return content

    def __new_tmp_file(self, dir):
        return NamedTemporaryFile(mode="w+", dir=dir, suffix=".tmp", prefix="")

    def __del__(self):
        shutil.rmtree(self.__tmpDir)
