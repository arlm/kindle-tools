import sys
import pandas
import time
from io import StringIO
import prettytable
from datetime import datetime, date
from lib.kindle import Kindle

class Clippings:

    kindle_device = None
    entries = []

    def __init__(self, directory):
        self.kindle_device = Kindle(directory)

        if not self.kindle_device.device_detected and not directory:
            print('No Kindle device detected !')
            sys.exit(-100)

    def __split(self):
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

    def __process_data(self):
        start = time.time()
        print("Importing data...")
        data = pandas.DataFrame.from_dict(self.entries, 'columns')
        end = time.time()
        print("Finished importing data ", end - start)
        start = time.time()
        print("Processing data...")
        
        summary = data.loc[:,('book','author', 'date', 'type')]
        summary['date'] = summary['date'].apply(lambda x: x.year)
        summary = summary.drop_duplicates().groupby(['date', 'book', 'author']).count().rename(columns={'type':'count'})


        yearly_summary = summary.groupby('date').count().rename(columns={'count':'books read'})

        output = StringIO()
        yearly_summary.to_csv(output, header = True)
        output.seek(0)
        print(prettytable.from_csv(output))

        notes = data.sort_values(by = ['date', 'book', 'page', 'location', 'type'])

        print('\nFound ' + str(notes['text'].count()) + ' notes and highlights...\n')

        end = time.time()
        print("Finished processing data ", end - start)
        start = time.time()
        print("Exporting to Excel...")

        writer = pandas.ExcelWriter("kindle-clippings.xlsx",
            engine='xlsxwriter',
            datetime_format='mmm d yyyy hh:mm:ss',
            date_format='mmmm dd yyyy')

        summary.to_excel(writer, sheet_name='Summary')
        notes.to_excel(writer, sheet_name='Clippings')

        row = len(summary.index) + 3
        yearly_summary.to_excel(writer, startrow=row, sheet_name='Summary')

        workbook  = writer.book
        str_format = workbook.add_format({'align': 'right', 'valign': 'vcenter', 'bold': False, 'text_wrap': True})       
        txt_format = workbook.add_format({'align': 'justify', 'valign': 'vcenter', 'bold': False, 'text_wrap': True})       
        head_format = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'bold': True})
        
        worksheet = writer.sheets['Summary']

        book_len = data['book'].astype(str).apply(lambda x: len(x)).max().max() * 0.85
        author_len = data['author'].astype(str).apply(lambda x: len(x)).max().max() * 0.85
        
        worksheet.set_column(0, 0, 4.5, head_format)
        worksheet.set_row(0, None, head_format)
        
        worksheet.set_column(1, 1, book_len, str_format)
        worksheet.set_column(2, 2, author_len, str_format)

        worksheet = writer.sheets['Clippings']

        worksheet.set_column(0, 0, 4.5, head_format)
        worksheet.set_row(0, None, head_format)

        worksheet.set_column(1, 1, author_len * 0.50, str_format)
        worksheet.set_column(2, 2, book_len * 0.50, str_format)
        worksheet.set_column(3, 3, 18, str_format)

        location_len = data['location'].astype(str).apply(lambda x: len(x)).max().max()
        worksheet.set_column(4, 4, location_len, str_format)
        worksheet.set_column(5, 5, location_len * 0.60, str_format)
        worksheet.set_column(6, 6, 75, txt_format)
        worksheet.set_column(7, 7, 8, str_format)

        writer.save()

        end = time.time()
        print("Finished exporting data to Excel", end - start)

    def parse(self):
        import re

        chunks = self.__split()

        for chunk in chunks:
            if not chunk:
                continue

            line1 = re.search('^(?P<Book>.*?)(\\s*\\((?P<Author>[^\\(]*)\\))?$', chunk[0])
            line2 = re.search('^\\s*-\\s*Your (?P<Type>(Highlight|Note|Bookmark))\\s*on(\\s*[Pp]age (?P<Page>[xivlcm\\d-]*))?(\\s*\\|)?(\\s*([Ll]ocation|[Ll]oc\\.) (?P<Location>[xivlcm\\d-]*))?\\s*\\|\\s*Added on (?P<Date>([^\r\n]*))$', chunk[1])
            timestamp = (datetime.min, datetime.strptime(line2.group('Date'), '%A, %B %d, %Y %I:%M:%S %p').date())[line2 != None]

            if len(chunk) >= 3:
                line3 = re.search('^\\s*(?P<Text>.*?)$', chunk[2])

            entry = {
                'book': line1.group('Book'),
                'author': line1.group('Author'),
                'type': ('', line2.group('Type'))[line2 != None],
                'page': ('', line2.group('Page'))[line2 != None],
                'location': ('', line2.group('Location'))[line2 != None],
                'date': timestamp,
                'text': ('', line3.group('Text'))[line3 != None]
            }

            self.entries.append(entry)
        
        self.__process_data()

