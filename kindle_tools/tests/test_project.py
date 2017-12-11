import sys
import unittest
from mockito import mock, when, verify
from lib.options import Options
from lib.project import Project


class TestProject(unittest.TestCase):
    
    def _default_options(self):
        options = Options()
        options.parse()
        return options

    def setUp(self):
        self.project = Project(self._default_options())
        mocked_process = mock() 
        result = self.project.process.execute("date").strip(b'\n')
        when(mocked_process).execute('date').thenReturn("The date might be: "+result.decode('utf-8')+"\nbut we could also overwrite it to be the 1st of April instead.")
        # overwriting project's process.execute('date') with the mock function above
        # just an example of overwriting a dependency when testing
        self.project.process = mocked_process 

    def test_project_should_get_date(self):
        self.assertTrue('1st of April' in self.project.process.execute('date'))
        verify(self.project.process).execute('date')

if __name__ == '__main__':
    unittest.main()