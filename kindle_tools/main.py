import sys

from lib.project import Project
from lib.options import Options

def run_project(args):
    options = Options()
    options.parse(args[1:])

    project = Project(options)

    print('Printing date:'+project.date().decode('utf-8'))
    print('Printing example arg:'+project.print_example_arg())

if __name__ == '__main__':
    run_project(sys.argv)