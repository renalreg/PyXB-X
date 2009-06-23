import pyxb.binding.generate
import pyxb.binding.datatypes as xsd
import pyxb.utils.domutils
from xml.dom import Node

import os.path
schema_path = '%s/../schemas/test-ctd-simple.xsd' % (os.path.dirname(__file__),)
code = pyxb.binding.generate.GeneratePython(schema_file=schema_path)
rv = compile(code, 'test', 'exec')
eval(rv)

from pyxb.exceptions_ import *

import unittest

class TestCTDSimple (unittest.TestCase):

    def testClause4 (self):
        self.assertTrue(clause4._IsSimpleTypeContent())
        self.assertTrue(clause4._TypeDefinition == xsd.string)
        self.assertEqual(None, clause4._TypeDefinition._CF_length.value())

    def testClause3 (self):
        self.assertTrue(clause3._IsSimpleTypeContent())
        self.assertTrue(issubclass(clause3, clause4))
        self.assertTrue(clause3._TypeDefinition == xsd.string)

    def testClause2 (self):
        self.assertTrue(clause2._IsSimpleTypeContent())
        self.assertTrue(issubclass(clause2, ctype))
        self.assertTrue(issubclass(clause2._TypeDefinition, xsd.string))
        self.assertEqual(6, clause2._TypeDefinition._CF_length.value())

    def testClause1_1 (self):
        self.assertTrue(clause1_1._IsSimpleTypeContent())
        self.assertTrue(issubclass(clause1_1, clause4))
        self.assertTrue(issubclass(clause1_1._TypeDefinition, xsd.string))
        self.assertEqual(6, clause1_1._TypeDefinition._CF_length.value())

if __name__ == '__main__':
    unittest.main()
    
        
