import sys
from lib.options import Options
from lib.clippings import Clippings

def run_project(args):
    options = Options()
    options.parse(args)

    if options.known.do_clippings:
        clip = Clippings()
        

if __name__ == '__main__':
    run_project(sys.argv)