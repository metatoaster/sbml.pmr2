from os.path import dirname, join
import unittest

from sbml.pmr2.annotator import *

testroot = dirname(__file__)
input_dir = join(testroot, 'input')

def read_file(fn):
    f = open(join(input_dir, fn))
    result = f.read()
    f.close()
    return result


class SimpleSBMLNoteAnnotator(SBMLNoteAnnotator):
    """
    Since we are skipping the whole registration of components 
    altogether here, we instantiate the annotator directly with the
    input changed to whatever we are trying to parse, so the context in
    our case is the actual content, thus the input property need to be 
    adjusted.
    """

    @property
    def input(self):
        return self.context


class SBMLNoteAnnotatorTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_0000_complete_data(self):
        fn = 'BIOMD0000000064.xml'
        f = read_file(fn)
        a = SimpleSBMLNoteAnnotator(f)
        results = a.generate()
        # mangle results such that answers are predictable.
        self.assertEqual(len(results[0][1]), 10011)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SBMLNoteAnnotatorTestCase))
    return suite

if __name__ == '__main__':
    unittest.main()

