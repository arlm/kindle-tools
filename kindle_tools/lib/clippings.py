import sys
from lib.kindle import Kindle

class Clippings:

    kindle_device = None
    entries = []

    def __init__(self):
        self.kindle_device = Kindle()

        if not self.kindle_device.device_detected:
            print('No Kindle device detected !')
            sys.exit(-100)

    #Date Format: %A, %d %B %y %H:%M:%S
    def split(self):
        delimiter = '=========='
        chunks = []
        current_chunk = []

        for line in open(self.kindle_device.clippings_file, 'r').readlines():
            if line.startswith(delimiter) and current_chunk:
                chunks.append(current_chunk[:])
                current_chunk = []

            if not line.startswith(delimiter) and not line == '\n':
                current_chunk.append(line)

        chunks.append(current_chunk)
        return chunks

    def parse(self, chunks):
        import re

        for chunk in chunks:
            if not chunk:
                continue

            line1 = re.search('^(?P<Book>.*?)(\\s*\\((?P<Author>[^\\(]*)\\))?$', chunk[0])
            line2 = re.search('^\\s*-\\s*Your\\ (?P<Type>(Highlight|Note|Bookmark))(\\s*on\\ [Pp]age\\ (?P<Page>[\\d-]*))? |(\\s*([Ll]ocation|[Ll]oc\\.)\\ (?P<Location>[\\d-]*))?\\s*\\|\\s*Added\\ on\\ (?P<Date>([^\r\n]*))$', chunk[1])
            
            if len(chunk) >= 3:
                line3 = re.search('^\\s*(?P<Text>.*?)$', chunk[2])

            entry = {
                'book': line1.group('Book'),
                'author': line1.group('Author'),
                'type': ('', line2.group('Type'))[line2 != None],
                'page': ('', line2.group('Page'))[line2 != None],
                'location': ('', line2.group('Location'))[line2 != None],
                'date': ('', line2.group('Date'))[line2 != None],
                'text': ('', line3.group('Text'))[line3 != None]
            }

            self.entries.append(entry)
