# External
import sys
from argparse import ArgumentParser, FileType

class Options:

    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage = './bin/kindle-tool'
        self.parser = ArgumentParser(usage=usage, description='Extracts information from Kindle devices and apps')
        self.parser.add_argument('-c', '--clippings', dest='do_clippings', help='Parses the Kindle device clippings file', action='store_true')
        self.parser.add_argument('--version', action='version', version='kindle-tool 0.1.0')

    def check_flags(self):
        return not self.known.do_clippings

    def parse(self, args=None):
        self.known, self.unknown = self.parser.parse_known_args(args)[:]
        if (len(self.unknown) == 1 and self.unknown[0] == args[0] and self.check_flags()) or (len(self.unknown) > 1):
            msg = '*WARN* Unknown args received: '+repr(self.unknown)+'\n'
            if len(self.unknown) == 1 and self.unknown[0] != args[0]:
                print(msg)
            self.parser.print_help()
            sys.exit(-2)

