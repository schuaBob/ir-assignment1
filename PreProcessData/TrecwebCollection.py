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
        """Get the next document info then extract the content given the position info of the doc.
        Use the HTMLParser to remove HTML tags in the content
        """
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
        """Extract content given a starting Tag and ending Tag. Can be surrounded by <>."""
        openTag = f"<{startTag}>" if not endTag else startTag
        closeTag = endTag if endTag else f"</{startTag}>"
        return doc[
            (start := doc.find(openTag) + len(openTag)) : doc.rfind(closeTag, start)
        ]


class TrecHTMLParser(HTMLParser):
    """SubClass of HTMLParser to remove HTML tags in the content.
    Store extracted content in a temp file instead of memory to avoid string concatenation or join operation.
    Read and write operations is handled by I/O, so CPU can continue to work on the next task.
    """
    def __init__(self):
        super().__init__()
        self.__tmpDir = mkdtemp(dir=os.path.dirname(__file__))
        self.__tmpFile = self.__new_tmp_file(self.__tmpDir)

    def handle_data(self, data: str):
        """Will be triggered automatically when content is found between html tags"""
        self.__tmpFile.write(data)

    def get_content(self):
        """Jump to the beginning of the file and read the content.
        Close the file and return the content.
        """
        self.__tmpFile.seek(0)
        content = self.__tmpFile.read()
        self.__tmpFile.close()
        self.__tmpFile = self.__new_tmp_file(self.__tmpDir)
        return content

    def __new_tmp_file(self, dir):
        """Create a temp file to store data extracted in a document. Temp file will be auto deleted when closed"""
        return NamedTemporaryFile(mode="w+", dir=dir, suffix=".tmp", prefix="")

    def __del__(self):
        """Remove latest temp file and the temp directory"""
        self.__tmpFile.close()
        shutil.rmtree(self.__tmpDir)
