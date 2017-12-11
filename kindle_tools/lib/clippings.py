# External
from lib.kindle import Kindle

class Clippings:

    kindle_device = None

    def __init__(self):
         self.kindle_device = Kindle()

    #Date Format: %A, %d %B %y %H:%M:%S
    #Notes Pattern: ^(?P<Book>.*?)(\s*\((?P<Author>[^\(]*)\))?$\s*-\s*Your\ (?P<Type>(Highlight|Note|Bookmark))(\s*on\ [Pp]age\ (?P<Page>[\d-]*))?\ \|(\s*(Location|Loc\.)\ (?P<Location>[\d-]*))?\s*\|\s*Added\ on\ (?P<Date>([^\r\n]*))$\s*(?P<Text>.*?)$\s*=+$
    def split(self):
        delimiter = '=========='
        chunks = []
        current_chunk = []

        for line in open(self.kindle_device.clippings_file).readlines():
            if line.startswith(delimiter) and current_chunk:
                chunks.append(current_chunk[:]) #  add not empty chunk to chunks
                current_chunk = [] #  make current chunk blank
            # just append a line to the current chunk on each iteration
            current_chunk.append(line)

        chunks.append(current_chunk)  #  append the last chunk outside the loop
        return chunks
